class DailyAvailability:
    def __init__(self, session_dates, text) -> None:
        """
        takes a text arg from a *.csv row,
        parses row looking for dates
        corresponding to the given days
        of each session,
        sets index of day in 8 length array
        as false if found
        """
        self.session_dates = session_dates
        
        # list of bool values for each day of the week
        self.days_available = [not day.short_string() in text.lower() for day in session_dates]

    def __str__(self):
        return f"{self.days_available}"
        
    def get_days_off(self):
        """
        returns a list of days off
        """
        return [str(self.session_dates[i]) for i, day in enumerate(self.days_available) if not day]