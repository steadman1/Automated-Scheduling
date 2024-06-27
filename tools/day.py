from datetime import date, datetime, timedelta

class Day:
    def __init__(self, year, month, day):
        """
        takes a year, month, and day in form
        of integers, sets them as attributes
        starting at 1 to avoid confusion
        """
        self.year = year
        self.month = month
        self.day = day
        
        self.months = [
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "june",
            "july",
            "aug",
            "nov",
            "oct",
            "dec"
        ]
        
    def short_string(self):
        """
        returns a string in the form of
        'Month' 'Day'
        """
        return f"{self.months[self.month - 1]} {self.day}"

    def __str__(self):
        return f"{self.year}/{self.month}/{self.day}"
        
    @classmethod
    def interpret(cls, text):   
        """
        takes a string in the form of
        'Month' 'Day', 'Year' (optional)
        and returns a Day object
        """
        # Define the current year
        current_year = datetime.now().year
    
        # Try to parse the string with and without the year
        try:
            # Try parsing with the year
            parsed_date = datetime.strptime(text, "%B %d %Y")
        except ValueError:
            # If it fails, try parsing without the year and use the current year
            parsed_date = datetime.strptime(text, "%B %d")
            parsed_date = parsed_date.replace(year=current_year)
    
        return cls(parsed_date.year, parsed_date.month, parsed_date.day)
    
    @staticmethod
    def next_day(day):
        """
        Takes a Day object and returns a new Day object representing the next day.
        """
        current_date = date(day.year, day.month, day.day)
        next_date = current_date + timedelta(days=1)
        return Day(next_date.year, next_date.month, next_date.day)
    
    @staticmethod
    def generate_days_between(start_date, end_date):
        """
        takes two Day objects,
        returns a list of Day objects
        between the two
        """
        current_date = start_date
        days = []
        while current_date.day <= end_date.day and current_date.month <= end_date.month and current_date.year <= end_date.year:
            days.append(Day(current_date.year, current_date.month, current_date.day))
            current_date = Day.next_day(current_date)
        return days
        
    @staticmethod
    def condense_days_between(days):
        """
        takes a list of Day objects,
        returns a string representing
        a range of days
        """
        if len(days) == 0:
            return ""
        elif len(days) == 1:
            return str(days[0])
        else:
            return f"{days[0]} - {days[-1]}"