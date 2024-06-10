import csv
import os
from pathlib import Path

from exceptions import NoFileFoundException

CSV_DIRECTORY_NAME = "Availability"
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
PARENT_DIRECTORY = Path(CURRENT_DIRECTORY).parent
CSV_DIRECTORY = (PARENT_DIRECTORY).joinpath(CSV_DIRECTORY_NAME)

def get_availability():
    """
    Walks all files in the Availability directory, 
    asks user to select desired file if more than one, 
    returns the file path of the selected file.
    """
    csv_files = []
    desired_index = 0
    
    for root, dirs, files in os.walk(CSV_DIRECTORY):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(file)
    
    if len(csv_files) > 1:
        for index, csv_file in enumerate(csv_files):
            print(f"[ {index + 1} ] - {csv_file}")
            
        input("Enter the index of the desired file: ")
        
    if len(csv_files) < 1:
       raise NoFileFoundException(f"No \"*.csv\" files were found in the {CSV_DIRECTORY_NAME} folder. Please add one.") 
    
    return (CSV_DIRECTORY).joinpath(csv_files[desired_index])

if __name__ == "__main__":
    availability = get_availability()
    print(availability)