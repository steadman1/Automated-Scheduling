from tools.daily_availability import DailyAvailability
from unix_time import to_unix_time
from time_availability import TimeAvailability

class LessonsInstructors():
    def __init__(self) -> None:
        self.instructors = []
    
    def add_instructor(self, instructor):
        if any(instructor.time_availability.availability):
            self.instructors.append(instructor)
            
    def set_session_dates(self, session_dates):
        for instructor in self.instructors:
            instructor.set_daily_availability(session_dates)
            
    def get_available_instructors(self, date, time):
        return [instructor for instructor in self.instructors if instructor.is_available(date, time)]
    
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
        perferred_levels,
        time_availability,
    ) -> None:
        self.row = row
        self.date = date
        self.first_name = first_name
        self.last_name = last_name
        self.seniority = seniority
        self.perferred_levels = perferred_levels
        self.time_availability = time_availability
    
    def set_daily_availability(self, session_dates):
        self.daily_availability = DailyAvailability(session_dates, self.row[6])
        
    def is_available(self, date, time):
        return self.daily_availability.days_available[date.weekday()] and self.time_availability.is_available(time)
    
    def __str__(self) -> str:
        string = f"{self.first_name} {self.last_name} of {self.seniority} year(s) is available {self.time_availability}"
        days_off = self.daily_availability.get_days_off()
        if len(days_off) > 0:
            string += f" and is off on {", ".join(days_off)}"
        else:
            string += " and is available every day"
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
            perferred_levels=row[4].split(";"),
            time_availability=TimeAvailability(row[5])
        )