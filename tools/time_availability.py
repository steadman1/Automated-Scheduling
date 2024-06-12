# parent class has longer name
# bc it should be used less often
# than the child "TimeBlock" class
class TimeBlockAMPM:
    def __init__(self, beginning, b_meridiem, end, e_meridiem) -> None:
        self.beginning = beginning
        self.b_meridiem = b_meridiem
        self.end = end
        self.e_meridiem = e_meridiem
        
    def __str__(self) -> str:
        return f"{self.beginning}{self.b_meridiem if self.b_meridiem != self.e_meridiem else ""}-{self.end}{self.e_meridiem}"
 
# child class of "TimeBlockSwitching"
class TimeBlock(TimeBlockAMPM):
    def __init__(self, beginning, end, meridiem) -> None:
        super().__init__(beginning, meridiem, end, meridiem)

class TimeAvailability:
    def __init__(self, text) -> None:
        """
        takes a text arg from a *.csv row,
        parses row looking for string
        mathching given time within text,
        sets time object as true if found
        """
        text = text.lower().replace(" ", "")
        
        self.time_table = [
            TimeBlock("10:00", "10:45", "am"),
            TimeBlock("10:45",  "11:30", "am"),
            TimeBlockAMPM("11:30", "am", "12:15", "pm"),
            TimeBlock("12:15", "1:00", "pm"),
            TimeBlock("1:00", "2:30", "pm"),
            TimeBlock("2:30", "3:15", "pm"),
            TimeBlock("3:15", "4:00", "pm"),
            TimeBlock("4:00", "4:45", "pm"),
            TimeBlock("4:45", "5:30", "pm"),
            TimeBlock("5:30", "6:15", "pm"),
            TimeBlock("6:15", "7:00", "pm"),
        ]
        self.availability = [str(time) in text for time in self.time_table]
        
    def __str__(self) -> str:
        """
        returns instructor availablity in
        natural language
        """
        indicies = [i for i, x in enumerate(self.availability) if x]

        string = ""
        
        def recursive_next_time(index):
            if len(indicies) > index + 1 and indicies[index + 1] == indicies[index] + 1:
                return recursive_next_time(index + 1)
            return index, self.time_table[indicies[index]]
        
        index = 0
        while len(indicies) > index:
            if not index == 0:
                string += "and "
            next_index, time_block = recursive_next_time(index)
            string += f"from {self.time_table[indicies[index]].beginning}{self.time_table[indicies[index]].b_meridiem} to {time_block.end}{time_block.e_meridiem} "
            index += next_index + 1
    
        return string