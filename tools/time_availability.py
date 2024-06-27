import json

class TimeBlock:
    def __init__(self, start, s_meridiem, end, e_meridiem) -> None:
        self.start = start
        self.s_meridiem = s_meridiem
        self.end = end
        self.e_meridiem = e_meridiem
        
    @classmethod
    def from_json(cls, json):
        start = json["start"].replace(" ", "")
        end = json["end"].replace(" ", "")
        
        s_meridiem = start[-2:].lower()
        e_meridiem = end[-2:].lower()
    
        return cls(start.replace(s_meridiem, ""), s_meridiem, end.replace(e_meridiem, ""), e_meridiem)
        
    def __str__(self) -> str:
        return f"{self.start}{self.s_meridiem if self.s_meridiem != self.e_meridiem else ""}-{self.end}{self.e_meridiem}"

    def __eq__(self, value) -> bool:
        if isinstance(value, TimeBlock):
            return self.start == value.start and \
                self.s_meridiem == value.s_meridiem and \
                self.end == value.end and \
                self.e_meridiem == value.e_meridiem
        return False

class TimeAvailability:
    def __init__(self, text) -> None:
        """
        takes a text arg from a *.csv row,
        parses row looking for string
        mathching given time within text,
        sets time object as true if found
        """
        text = text.lower().replace(" ", "")
        
        self.time_table = []
        for time in json.load(open("settings.json"))["session_times"]:
            self.time_table.append(TimeBlock.from_json(time))
        
        self.availability = [str(time) in text for time in self.time_table]
        
    def is_available(self, time):
        """
        returns true if instructor is available
        at the given time
        """
        return str(time) in [str(time_tab) for time_tab in self.time_table]
        
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
            string += f"from {self.time_table[indicies[index]].start}{self.time_table[indicies[index]].s_meridiem} to {time_block.end}{time_block.e_meridiem} "
            index += next_index + 1
    
        return string