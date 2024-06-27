import json
from day import Day

class LessonsClass:
    def __init__(self, level, swimmer_count):
        self.levels = [level]
        self.swimmer_count = swimmer_count
        self.requires_time_share = False
        self.instructors = []

    def set_timing(self, time, session_dates):
        self.time = time
        self.session_dates = session_dates

    def add_level(self, level):
        if level > self.levels[-1]:
            self.levels.append(level)
        else:
            self.levels.insert(0, level)
    
    def is_mixed_level(self):
        return len(self.levels) > 1

    def add_instructor(self, instructor):
        self.instructors.append(instructor)
        
    def is_time_share(self):
        return len(self.instructors) > 1
    
    def __str__(self):
        return f"Levels: {self.levels}, Size: {self.swimmer_count} Instructors: {[instructor.name for instructor in self.instructors]} Time: [{self.time}] Dates: {Day.condense_days_between(self.session_dates)} Unfilled Time Share: {self.requires_time_share}"
        
    @staticmethod
    def _place_classes(swimmer_counts_by_level, time, session_dates):
        swimmer_count_per_class = json.load(open("settings.json"))["swimmer_count_per_class"]
        lessons_classes = []
        for index, swimmer_count_by_level in enumerate(swimmer_counts_by_level):
            level = index + 1

            overflow = swimmer_count_by_level % swimmer_count_per_class
            
            for n in range(int(swimmer_count_by_level // swimmer_count_per_class)):
                lesson_class = LessonsClass(level, swimmer_count_per_class)
                lesson_class.set_timing(time, session_dates)
                lessons_classes.append(lesson_class)
                
            if overflow > 0:
                lesson_class = LessonsClass(level, overflow)
                lesson_class.set_timing(time, session_dates)
                lessons_classes.append(lesson_class)
                continue
                
        return lessons_classes


    @staticmethod
    def _relevel_classes(lessons_classes):
        """
        takes a list of lessons classes and
        balances the classes to relevel the
        classes allowing students of adjacent
        levels to be combined
        """
        swimmer_count_per_class = json.load(open("settings.json"))["swimmer_count_per_class"]
        
        for index, lessons_class in enumerate(lessons_classes):
            if lessons_class.swimmer_count < swimmer_count_per_class:
                for next_index in range(index + 1, len(lessons_classes)):
                    next_class = lessons_classes[next_index]
                    if (next_class.levels[0] - lessons_class.levels[0] == 1 and 
                        next_class.swimmer_count < swimmer_count_per_class):
                        
                        combined_swimmer_count = lessons_class.swimmer_count + next_class.swimmer_count
                        if combined_swimmer_count <= swimmer_count_per_class:
                            # Combine classes
                            lessons_class.swimmer_count = combined_swimmer_count
                            lessons_class.add_level(next_class.levels[0])
                            lessons_classes.pop(next_index)
                            break
        
        return lessons_classes
        
    @staticmethod
    def _balance_classes(lessons_classes):
        """
        takes a list of lessons classes and
        balances the classes to have no more
        that abs(n + 1) difference in swimmer_counts
        by averaging the swimmer_counts
        """
        swimmer_count_per_class = json.load(open("settings.json"))["swimmer_count_per_class"]
        
        for index, lessons_class in enumerate(lessons_classes):
            for next_index in range(index + 1, len(lessons_classes)):
                next_class = lessons_classes[next_index]
                
                mixed_contains = lessons_class.is_mixed_level() and next_class.levels[0] in lessons_class.levels
                non_mixed_can_contain = not lessons_class.is_mixed_level() and abs(next_class.levels[0] - lessons_class.levels[0]) == 1
                if (mixed_contains or non_mixed_can_contain) and \
                    abs(lessons_class.swimmer_count - next_class.swimmer_count) > 1:
                        
                    total_swimmer_count = lessons_class.swimmer_count + next_class.swimmer_count
                    average_swimmer_count = total_swimmer_count // 2
                    difference = total_swimmer_count % 2
                    
                    lessons_class.swimmer_count = average_swimmer_count + difference
                    next_class.swimmer_count = average_swimmer_count
                    
                    # add level of the other class if different
                    if next_class.levels[0] not in lessons_class.levels:
                        lessons_class.add_level(next_class.levels[0])
                    if lessons_class.levels[0] not in next_class.levels:
                        next_class.add_level(lessons_class.levels[0])
                    
                    break
        
        return lessons_classes

    @staticmethod
    def get_lessons_classes_from_levels(swimmer_counts_by_level, time, session_dates):
        """
        takes a list of swimmers in level and
        determines the amount of classes needed
        to evenly distribute swimmers between
        levels—classes can contain swimmers of
        only one level or a combination of the 
        labeled level and level below it
        """     

        lessons_classes = LessonsClass._place_classes(swimmer_counts_by_level, time, session_dates)
        lessons_classes = LessonsClass._relevel_classes(lessons_classes)
        
        previous_lesssons_classes = []
        while previous_lesssons_classes != lessons_classes:
            previous_lesssons_classes = lessons_classes
            lessons_classes = LessonsClass._balance_classes(lessons_classes)
        
        return lessons_classes
