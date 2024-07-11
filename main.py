import csv
import os
import json
import sys

from tools.time_availability import TimeBlock
from tools.write_xlsx import write_schedule
sys.path.append('./tools')

from tools.gui import setup_date_gui, setup_file_gui
from tools.day import Day
from tools.exceptions import NoFileFoundException
from tools.read_csv import get_availability_csv_file, get_session_count
from tools.lessons_instructor import LessonsInstructor, LessonsInstructors
from tools.lessons_class import LessonsClass

def handle_swimmer_count_by_level():
    swimmer_count_by_level = []
    for level in range(json.load(open("settings.json"))["highest_level"]):
        count = int(input(f"Enter the number of swimmers for level {level + 1}: "))
        swimmer_count_by_level.append(count)
    
    return swimmer_count_by_level
    
    
def handle_classes(session_dates, swimmer_counts_by_level):
    """
    Takes 2D array of swimmer counts by level
    and returns a dict with cooresponding time
    """
    swimmer_counts_by_level_with_time = []
    for index, time in enumerate(json.load(open("settings.json"))["session_times"]):
        print(f"Enter the number of swimmers for {time['start']} - {time['end']}")
        swimmer_counts_by_level_with_time.append({
            "time": TimeBlock.from_json(time),
            "swimmer_counts_by_level": swimmer_counts_by_level[index]
        })
    
    # lessons_classes = LessonsClass.get_lessons_classes_from_levels(
    #     swimmer_counts_by_level_with_time[0]["swimmer_counts_by_level"],
    #     swimmer_counts_by_level_with_time[0]["time"],
    #     session_dates
    # )
    
    # print(lessons_classes)
    
    lessons_classes = []
    for swimmer_counts_by_level_with_time in swimmer_counts_by_level_with_time:
        lessons_classes += LessonsClass.get_lessons_classes_from_levels(
                            swimmer_counts_by_level_with_time["swimmer_counts_by_level"],
                            swimmer_counts_by_level_with_time["time"], 
                            session_dates
                        )
    
    return lessons_classes
    

def handle_scheduling(instructors, session_dates, swimmer_counts_by_level):
    """
    builds a schedule of availability for
    given instructors based on a given
    count of lessons classes sold for 
    each given level
    """
    lessons_classes = handle_classes(session_dates, swimmer_counts_by_level)
    
    return instructors.place_classes(lessons_classes)
    

def handle_availability(session_index, output=None):
    if output is None:
        output = get_availability_csv_file()
    
    if not os.path.isfile(output):
        raise NoFileFoundException(f"The *.csv file at {output} does not exist or is corrupted.")
        
    with open(output, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        return LessonsInstructors.from_csv(reader, session_index, skip=1)
        

if __name__ in "__main__":
    file = setup_file_gui()
    
    session_count = get_session_count(file)

    for session_index in range(session_count):
        instructors = handle_availability(session_index, file)
        
        start_date, end_date, swimmer_counts_by_level = setup_date_gui(session_index)
        
        session_dates = Day.generate_days_between(start_date, end_date)
        
        instructors.set_session_dates(session_dates, session_index)
        
        schedule = handle_scheduling(instructors, session_dates, swimmer_counts_by_level)
        
        write_schedule(schedule, session_dates, session_index)
        
        print("\n".join([str(lessons_class) for lessons_class in schedule]))