"""
Timestamp handling for the conversion processes.
--------------------------------------------------------------------------------
`src.utils.avro_utils.empatica_avro`

"""
from datetime import datetime
from zoneinfo import ZoneInfo


# --------------------------------------------------------------------------------
# Timestamp Formatting
# --------------------------------------------------------------------------------
def get_timestamps_avro(timestamp_start, sampling_frequency, len_data):
    """
    This is how it is done in the official empatica documentation/example code.
    Not sure how timestamp precision is usually handled...
        * 1729803446        -> second precision
        * 1729787475 876218 -> precision from this function

    *** Added in rounding for the sampling frequency because things weren't lining up... ***
    """
    timestamps = [round(timestamp_start + i * (1e6 / sampling_frequency)) for i in range(len_data)]
    return timestamps

# Organize the files by their timestamps
def get_file_timestamp(filename):
    """ The files are named using the first timestamp in the data """
    #                            input: 1-1-TEST3_1729798304.avro
    ts = filename.split("_")[-1] # now: 1729798304.avro
    ts = ts[:-5]                 # now: 1729798304
    return int(ts)


# --------------------------------------------------------------------------------
# Properly format manually given session start/end times
# --------------------------------------------------------------------------------
def get_start_end_stamps(day, session_number, start_end_dict, given_tz):
    """
    Properly format manually given session start/end timestamps.

    Using this method is better than just manually adding/subtracting 5 hours to get to UTC
    because of the difference from daylight savings (5 hour vs 6 hour difference from UTC
    depending on daylight savings in Chicago for example).
    """
    # Use day, video_num, and start_end_dict to get string format
    start_datetime_str = f"{day} {start_end_dict[session_number]['start']}"
    end_datetime_str   = f"{day} {start_end_dict[session_number]['end'  ]}"
    
    # Parse and localize using the provided time zone
    start_dt = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=given_tz)
    end_dt   = datetime.strptime(  end_datetime_str, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=given_tz)
    
    # Convert the datetime object to a Unix timestamp
    start_timestamp = int(start_dt.timestamp())
    end_timestamp   = int(  end_dt.timestamp())

    print(f"Start: {start_timestamp}  {datetime.fromtimestamp(start_timestamp, tz=given_tz)}")
    print(f"End:   {  end_timestamp}  {datetime.fromtimestamp(  end_timestamp, tz=given_tz)}")

    return start_timestamp, end_timestamp
