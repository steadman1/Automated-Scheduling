import csv
import os
import json
import sys
sys.path.append('./tools')

from tools.day import Day
from tools.exceptions import NoFileFoundException
from tools.read_csv import get_availability_csv_file
from tools.lessons_instructor import LessonsInstructor, LessonsInstructors
from tools.lessons_class import LessonsClass

def handle_swimmer_count_by_level():
    swimmer_count_by_level = []
    for level in range(json.load(open("settings.json"))["highest_level"]):
        count = int(input(f"Enter the number of swimmers for level {level + 1}: "))
        swimmer_count_by_level.append(count)
    
    return swimmer_count_by_level

def handle_scheduling(instructors, session_dates):
    """
    builds a schedule of availability for
    given instructors based on a given
    count of lessons classes sold for 
    each given level
    """
    
    swimmer_counts_by_level_with_time = []
    for time in json.load(open("settings.json"))["session_times"]:
        print(f"Enter the number of swimmers for {time['start']} - {time['end']}")
        swimmer_counts_by_level_with_time.append({
            "time": time,
            "swimmer_counts_by_level": handle_swimmer_count_by_level()
        })
    
    lessons_classes = LessonsClass.get_lessons_classes_from_levels(swimmer_counts_by_level_with_time[0]["swimmer_counts_by_level"])
    
    print("\n".join([str(lessons_class) for lessons_class in lessons_classes]))

def handle_instructors():
    output = get_availability_csv_file()
    
    if not os.path.isfile(output):
        raise NoFileFoundException(f"The *.csv file at {output} does not exist or is corrupted.")
        
    with open(output, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        return LessonsInstructors.from_csv(reader, skip=1)

if __name__ in "__main__":
    start_date = input("Enter start date of session (ex. June 3): ")
    end_date = input("Enter start date of session (ex. June 13): ")
    session_dates = Day.generate_days_between(Day.interpret(start_date), Day.interpret(end_date))
    
    instructors = handle_instructors()
    instructors.set_session_dates(session_dates)
    
    print(instructors)
    
    schedule = handle_scheduling(instructors, session_dates)
    
    print(schedule)