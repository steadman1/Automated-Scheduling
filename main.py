import csv
import sys
sys.path.append('./tools')

from tools.read_csv import get_availability
from tools.lessons_instructor import LessonsInstructor, LessonsInstructors

instructors = []

def main():
    output = get_availability()
    
    with open(output, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        instructors = LessonsInstructors.from_csv(reader, skip=1)
    
    print(instructors)

if __name__ in "__main__":
    main()