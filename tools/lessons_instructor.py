from unix_time import to_unix_time

class LessonsInstructor():
    def __init__(
        self,
        date,
        first_name,
        last_name,
        seniority,
        perferred_levels,
        time_availability,
    ) -> None:
        self.date = date
        self.first_name = first_name
        self.last_name = last_name
        self.seniority = seniority
        self.perferred_levels = perferred_levels
        self.time_availability = time_availability
        
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {self.seniority}y lvls {", ".join(self.perferred_levels)}"
    
    @staticmethod
    def from_csv(row):
        
        time_availability = [
            True,
            True,
            False,
        ]
        
        return LessonsInstructor(
            date=to_unix_time(row[0]),
            first_name=row[1],
            last_name=row[2],
            seniority=row[3],
            perferred_levels=row[4].split(";"),
            time_availability=time_availability
        )