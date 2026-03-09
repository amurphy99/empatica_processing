"""
Print info about a directory and it's contents (file sizes, etc.)
--------------------------------------------------------------------------------
`src.utils.logging.file_info`

Somtimes helpful to have when generating new files; just nice to get feedback.

"""
import os
from .logging import RESET, BOLD, BLUE


# --------------------------------------------------------------------------------
# Auto format the file size 
# --------------------------------------------------------------------------------
def get_file_size(file_bytes=0, file_path=None):
    # File size in bytes
    if file_path is not None: file_bytes = os.path.getsize(file_path)
    
    # Get the units to use
    i = 0
    sizes = [" B", "KB", "MB", "GB"]
    while (i < (len(sizes)-1)) and ((file_bytes / (1e3**i)) > 1e3): 
        i += 1
    
    # Now we have the file size
    file_str =  f"{BLUE} {(file_bytes / (1e3**i)):5,.1f} {sizes[i]}{RESET}"
    return file_str


# ================================================================================
# Print the files of a directory with their sizes
# ================================================================================
# (Change it so the size is done dynamically based on size of the folder contents?)
def print_directory_info(dir_path):
    # Get the directory contents
    dir_contents = [file for file in os.listdir(dir_path) if file != ".DS_Store"]
    dir_contents.sort()

    # Get the name of the longest file and the sizes of each file
    name_lengths, file_sizes = [], []
    for file in dir_contents:
        name_lengths.append(len(file))
        file_sizes  .append(os.path.getsize(f"{dir_path}/{file}"))
    
    # Print a line for the directory itself
    dir_size = get_file_size(file_bytes=sum(file_sizes))
    print(f"{BOLD}{dir_path}{RESET} {dir_size}")
    
    # --------------------------------------------------------------------------------
    # Print the save directory contents
    # --------------------------------------------------------------------------------
    longest_file_name = max(name_lengths)
    
    # Format strings for all files in the directory
    for i, file in enumerate(dir_contents):
        lead_char = "└──" if (i == len(dir_contents)-1) else "├──"
        spaces    = " " * (longest_file_name - len(file))
        file_size = get_file_size(file_path=f"{dir_path}/{file}")
        
        # Print the line for this file
        print(f" {lead_char} {file}{spaces} {file_size}")

