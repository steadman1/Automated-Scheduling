import csv
import sys
sys.path.append('./tools')

from tools.read_csv import get_availability
from tools.lessons_instructor import LessonsInstructor, LessonsInstructors

def main():
    output = get_availability()
    
    with open(output, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        session_dates = input("Enter all dates of session (ex. 11, 12, 13, 14): ")
        session_dates = session_dates.replace(" ", "").split(",")
        
        instructors = LessonsInstructors.from_csv(reader, skip=1)
        instructors.set_session_dates(session_dates)
    
    print(instructors)

if __name__ in "__main__":
    main()