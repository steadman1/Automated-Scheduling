import csv
import os
from pathlib import Path

from exceptions import NoFileFoundException

CSV_DIRECTORY_NAME = "Availability"

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
PARENT_DIRECTORY = Path(CURRENT_DIRECTORY).parent
CSV_DIRECTORY = (PARENT_DIRECTORY).joinpath(CSV_DIRECTORY_NAME)

def get_availability_csv_file():
    """
    Walks all files in the Availability directory, 
    asks user to select desired file if more than one, 
    returns the file path of the selected file as a str.
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
            
        desired_index = int(input("Enter the index of the desired file: ")) - 1
        
    if len(csv_files) < 1:
       raise NoFileFoundException(f"No \"*.csv\" files were found in the {CSV_DIRECTORY_NAME} folder. Please add one.") 
    
    return str((CSV_DIRECTORY).joinpath(csv_files[desired_index]))

def get_session_count(file_path):
    """
    Counts the number of rows in a given CSV file.
    """
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        row_count = sum(1 for row in csv_reader)
    return int((row_count - 6) / 2)

if __name__ == "__main__":
    availability = get_availability_csv_file()
    print(availability)