import json
from tools.daily_availability import DailyAvailability
from tools.tools import intersection
from unix_time import to_unix_time
from time_availability import TimeAvailability
from tools import *

class LessonsInstructors():
    def __init__(self) -> None:
        self.instructors = []
    
    def add_instructor(self, instructor):
        if any(instructor.time_availability.availability):
            self.instructors.append(instructor)
            
    def set_session_dates(self, session_dates):
        for instructor in self.instructors:
            instructor.set_daily_availability(session_dates)
            
    def get_available_time_instructors(self, time):
        """
        returns a list of instructors available at the given time
        """
        return [instructor for instructor in self.instructors if instructor.time_availability.is_available(time) and instructor.is_time_available(time)]
    
    def place_classes(self, classes):
        """
        adds instructors to classes based on availability
        """

        for lessons_class in classes:
            level = max(lessons_class.levels)
            
            # print(lessons_class.time)
            # print([instructor.name for instructor in self.get_available_time_instructors(lessons_class.time)])
            for instructor in self.get_available_time_instructors(lessons_class.time):
                if level in instructor.preferred_levels or (max(instructor.preferred_levels) >= level \
                    and not json.load(open("settings.json"))["strict_instructor_levels"]):

                    if len(lessons_class.instructors) < 1 or \
                        (len(lessons_class.instructors) < 2 and lessons_class.is_time_share()):
                        
                        if instructor.is_time_available(lessons_class.time):
                            lessons_class.add_instructor(instructor)
                            instructor.add_class(lessons_class)
                            
                            intersect = intersection([str(day) for day in lessons_class.session_dates], instructor.daily_availability.get_days_off())
                            if len(intersect) > 0 and not lessons_class.is_time_share():
                                lessons_class.requires_time_share = True
        
        self._place_time_share(classes)
        
        return classes
    
    def _place_time_share(self, classes):
        for lessons_class in classes:
            if lessons_class.requires_time_share:
                for instructor in self.get_available_time_instructors(lessons_class.time):
                    if len(lessons_class.instructors) < 2 and instructor.is_time_available(lessons_class.time):
                        lessons_class.add_instructor(instructor)
                        instructor.add_class(lessons_class)
                        lessons_class.requires_time_share = False
    
    def sort(self):
        self._sort_by_unix_time()
        self._sort_by_seniority()
    
    def _sort_by_seniority(self):
        self.instructors.sort(key=lambda x: x.seniority, reverse=True)
    
    def _sort_by_unix_time(self):
        self.instructors.sort(key=lambda x: x.date)
    
    def __str__(self) -> str:
        return "\n".join([str(instructor) for instructor in self.instructors])
    
    @classmethod
    def from_csv(cls, reader, skip=1):
        """
        takes a full *.csv sheet in reader,
        iterates through rows and adds each
        row as a LessonsInstructor object,
        returns a LessonsInstructors object
        """
        
        instructors = cls()
        
        for index, row in enumerate(reader):
            if index >= skip:
                instructor = LessonsInstructor.from_csv(row)
                instructors.add_instructor(instructor)
                
        instructors.sort()
        return instructors

class LessonsInstructor():
    def __init__(
        self,
        row,
        date,
        first_name,
        last_name,
        seniority,
        preferred_levels,
        time_availability,
    ) -> None:
        self.row = row
        self.date = date
        self.first_name = first_name
        self.last_name = last_name
        self.name = f"{first_name} {last_name}"
        self.seniority = seniority
        self.preferred_levels = [int(level) for level in preferred_levels]
        self.time_availability = time_availability
        self.classes = []
    
    def set_daily_availability(self, session_dates):
        self.daily_availability = DailyAvailability(session_dates, self.row[6])
    
    def add_class(self, lessons_class):
        self.classes.append(lessons_class)
        
    def is_time_available(self, time):
        has_class = False
        
        for lessons_class in self.classes:
            if lessons_class.time == time:
                has_class = True
                break
        
        return self.time_availability.is_available(time) and not has_class
    
    def is_available(self, date, time):
        return not date in self.daily_availability.get_days_off() and self.time_availability.is_available(time)
    
    def __str__(self) -> str:
        string = f"{self.first_name} {self.last_name} of {self.seniority} year(s) is available {self.time_availability}"
        days_off = self.daily_availability.get_days_off()
        if len(days_off) > 0:
            string += f"and is off on {", ".join(days_off)}"
        else:
            string += "and is available every day"
        return string
    
    @classmethod
    def from_csv(cls, row):
        """
        takes a *.csv row,
        returns a LessonsInstructor object
        """
        return cls(
            row=row,
            date=to_unix_time(row[0]),
            last_name=row[1],
            first_name=row[2],
            seniority=row[3],
            preferred_levels=row[4].split(";"),
            time_availability=TimeAvailability(row[5])
        )