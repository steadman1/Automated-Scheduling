import csv
import sys
sys.path.append('./tools')

from tools.read_csv import get_availability
from tools.lessons_instructor import LessonsInstructor

def main():
    output = get_availability()
    
    with open(output, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for index, row in enumerate(reader):
            if index > 0:
                print(LessonsInstructor.from_csv(row))

if __name__ in "__main__":
    main()