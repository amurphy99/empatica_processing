"""
Parse AVRO files from Empatica recordings.
--------------------------------------------------------------------------------
`src.utils.avro_utils.empatica_avro`

"""
import csv, os

from datetime import datetime
from zoneinfo import ZoneInfo

# Project code
from .timestamps import get_timestamps_avro, get_file_timestamp


# ================================================================================
# Write AVRO data for a single sensor type to a csv
# ================================================================================
def empatica_sensor_avro_to_csv(
        sensor: str, 
        data, 
        output_directory, 
        *, 
        filename      : str  = "", 
        append_mode   : bool = True, 
        verbose       : bool = False
):
    """
    Data consists of:
        * timestampStart
        * samplingFrequency
        * values ([x,y,z] for accelerometer and gyroscope, just "values" for the others)
        * (also "imuParams" for accelerometer and gyroscope)
    """
    # Setup filename to save to if not specified
    if filename == "": filename = f"{sensor}.csv"

    # Some sensors have more than one value, check which type of sensor this is
    xyz_sensors = ["accelerometer", "gyroscope"]
    xyz_sensor  = sensor in xyz_sensors

    # Different key for the timestamps for the xyz sensors
    data_key = "x" if xyz_sensor else "values"

    # Get the timestamps (same for all sensors) - use the starting timestamp and the sampling frequency and extrapolate
    sensor_data        = data["rawData"][sensor]
    sampling_frequency = sensor_data["samplingFrequency"]
    timestamps         = get_timestamps_avro(sensor_data["timestampStart"], sampling_frequency, len(sensor_data[data_key]))

    # Print some info if desired 
    if verbose: print(f"    {sensor:14} {sampling_frequency:5.1f} {len(sensor_data[data_key]):>9,}  {float(sensor_data['timestampStart']/1e6):>17.6f}")

    # Additional formatting for accelerometer (maybe gyroscope too?) ("Convert ADC counts in g" - taken from empatica official documentation)
    if sensor == "accelerometer": 
        delta_physical = sensor_data["imuParams"]["physicalMax"] - sensor_data["imuParams"]["physicalMin"]
        delta_digital  = sensor_data["imuParams"][ "digitalMax"] - sensor_data["imuParams"][ "digitalMin"]
        x_g = [val * delta_physical / delta_digital for val in sensor_data["x"]]
        y_g = [val * delta_physical / delta_digital for val in sensor_data["y"]]
        z_g = [val * delta_physical / delta_digital for val in sensor_data["z"]]

    # (Not sure if this has to be done to gyroscope data too?)
    elif sensor == "gyroscope": x_g, y_g, z_g = sensor_data["x"], sensor_data["y"], sensor_data["z"]

    # Rewrite or append to .csv
    mode = "a" if append_mode else "w"

    # Format data rows
    with open(os.path.join(output_directory, filename), mode, newline='') as f:
        writer = csv.writer(f)

        # Slight difference between accelerometer and gyroscope sensors and the others
        if xyz_sensor:
            sensor_headers = [f"{axis}_{sensor[:3]}" for axis in ["x", "y", "z"]]
            data_rows      = [[ts, x, y, z] for ts, x, y, z in zip(timestamps, x_g, y_g, z_g)]
        
        # Other sensors only have one column to fill 
        else:
            sensor_headers = [sensor]
            data_rows      = [[ts, x] for ts, x in zip(timestamps, sensor_data["values"])]

        # Write to the csv file (do headers first if the file is empty)
        if f.tell() == 0: writer.writerow(["unix_timestamp"] + sensor_headers)
        writer.writerows(data_rows)



# --------------------------------------------------------------------------------
# Only convert files that have relevant data
# --------------------------------------------------------------------------------
def get_list_of_files_to_convert(raw_data_path, start_timestamp, end_timestamp, given_tz):
    """ Only convert files that are included the period we have other data for... """
    # First just get all the files there
    all_avro_files = [x for x in os.listdir(raw_data_path) if x[-5:] == ".avro"]
    print(f"Originally {len(all_avro_files)} .avro files")
    
    # Get a dictionary of timestamps: full filenames
    avro_dict = {get_file_timestamp(file): file for file in all_avro_files}
    
    # Sort the dictionary
    avro_timestamps = list(avro_dict.keys())
    avro_timestamps.sort()

    # Go through and get the files that were in the time period (probably a better way to do this....)
    use_timestamps = []
    for i, avro_ts in enumerate(avro_timestamps):
        add_file = False

        # If the recordings started before the end timestamp...
        if avro_ts < end_timestamp:    
            # If this is the last avro file and it is still before the start timestamp, add it
            if (i+1 == len(avro_timestamps)) and (avro_ts < start_timestamp): add_file = True

            # If this is the last file before the start timestamp
            elif (i+1 < len(avro_timestamps)) and (avro_timestamps[i+1] > start_timestamp): add_file = True

            # Or if this is before the end timestamp and after the start timestamp
            elif avro_ts > start_timestamp: add_file = True

            # Add the file
            if add_file: use_timestamps.append(avro_ts) 

    # Print
    print(f"Now only converting {len(use_timestamps)} files: {use_timestamps}")
    print("\n.avro file names being used:")
    for ts in use_timestamps:
        dt = datetime.fromtimestamp(ts, tz=given_tz)
        print(f"  {avro_dict[ts]} - (data starts at: {dt})")
        
    return use_timestamps, avro_dict

