import csv
import os
import sys
sys.path.append('./tools')

from tools.exceptions import NoFileFoundException
from tools.read_csv import get_availability_csv_file
from tools.lessons_instructor import LessonsInstructor, LessonsInstructors

def handle_scheduling(instructors):
    pass

def handle_instructors():
    output = get_availability_csv_file()
    
    if not os.path.isfile(output):
        raise NoFileFoundException(f"The *.csv file at {output} does not exist or is corrupted.")
        
    with open(output, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        return LessonsInstructors.from_csv(reader, skip=1)

if __name__ in "__main__":
    session_dates = input("Enter all dates of session (ex. 11, 12, 13, 14): ")
    session_dates = session_dates.replace(" ", "").split(",")
    
    instructors = handle_instructors()
    instructors.set_session_dates(session_dates)
    
    handle_scheduling(instructors)
    
    print(instructors)
    