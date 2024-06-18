import csv
import os
import sys
sys.path.append('./tools')

from tools.exceptions import NoFileFoundException
from tools.read_csv import get_availability_csv_file
from tools.lessons_instructor import LessonsInstructor, LessonsInstructors

def handle_swimmer_count_by_level():
    swimmer_count_by_level = []
    for level in range(5):
        count = int(input(f"Enter the number of swimmers for level {level + 1}: "))
        swimmer_count_by_level.append(count)
    
    return swimmer_count_by_level

def handle_scheduling(instructors, swimmer_count_by_level):
    """
    builds a schedule of availability for
    given instructors based on a given
    count of lessons classes sold for 
    each given level
    """
    
    

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
    
    swimmer_count_by_level = handle_swimmer_count_by_level()
    
    handle_scheduling(instructors, swimmer_count_by_level)
    