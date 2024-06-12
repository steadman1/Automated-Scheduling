class TimeAvailability:
    def __init__(self, text) -> None:
        """
        takes a text arg from a *.csv row,
        parses it looking for a specific string
        within the text,
        sets time as true for object
        """
        
        text = text.lower().replace(" ", "")
        
        self._1000a = "10:00-10:45am" in text
        self._1045a = "10:45-11:30am" in text
        self._1130a = "11:30-12:15pm" in text
        self._1215p = "12:15-1:00pm" in text
        self._100p = "1:00-2:30pm" in text
        self._230p = "2:30-3:15pm" in text
        self._315p = "3:15-4:00pm" in text
        self._400p = "4:00-4:45pm" in text
        self._445p = "4:45-5:30pm" in text
        self._530p = "5:30-6:15pm" in text
        self._615p = "6:15-7:00pm" in text
        
    def get_availability(self):
        """
        returns a list of 11 bool values
        that equate to the instructors
        availability during the given time slots
        """
        return [
            self._1000a,
            self._1045a,
            self._1130a,
            self._1215p,
            self._100p,
            self._230p,
            self._315p,
            self._400p,
            self._445p,
            self._530p,
            self._615p,
        ]