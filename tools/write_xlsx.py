import pandas as pd
from tools.day import Day

def write_schedule(schedule, session_dates, session_index):
    """
    Write the schedule to a .xlsx file with the given session_dates
    in a single sheet, and add headers for each new class time.
    Each LessonsClass object details will be written in separate columns.
    Time share classes will be distinguished.
    """
    writer = pd.ExcelWriter('schedule.xlsx', engine='xlsxwriter')
    
    # Create a single worksheet for all session dates
    worksheet = writer.book.add_worksheet(f'Session #{session_index + 1}')
    
    # Format for headers
    header_format = writer.book.add_format({'bold': True, 'bg_color': '#D3D3D3', 'text_wrap': True})
    time_header_format = writer.book.add_format({'bold': True, 'bg_color': '#D8E4BC', 'text_wrap': True, 'font_size': 18})
    wrap_format = writer.book.add_format({'text_wrap': True})
    
    # Add headers for class details
    headers = ["Class Time", "Instructor Name(s)", "Is Time Share", "Level", "Class Swimmer Count", "Start and End Dates"]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    
    row = 1  # Start populating data from row 2 (index 1)
    
    # Group schedule by time
    classes_by_time = {}
    for lesson_class in schedule:
        time_key = str(lesson_class.time)
        if time_key not in classes_by_time:
            classes_by_time[time_key] = []
        classes_by_time[time_key].append(lesson_class)
    
    # Iterate through grouped classes by time
    for class_time, lessons in classes_by_time.items():
        worksheet.write(row, 0, str(class_time), time_header_format)
        row += 1  # Move to the next row for class details
        
        for lesson_class in lessons:
            # Write the lesson details
            instructor_names = ", ".join([instructor.name for instructor in lesson_class.instructors])
            requires_time_share = "Yes" if lesson_class.is_time_share() else "No"
            
            worksheet.write(row, 0, class_time, wrap_format)  # Class Time
            worksheet.write(row, 1, instructor_names, wrap_format)  # Instructor Names
            worksheet.write(row, 2, requires_time_share, wrap_format)  # Time Share
            worksheet.write(row, 3, ", ".join(map(str, lesson_class.levels)), wrap_format)  # Levels
            worksheet.write(row, 4, lesson_class.swimmer_count, wrap_format)  # Swimmer Count
            worksheet.write(row, 5, Day.condense_days_between(lesson_class.session_dates), wrap_format)  # Dates
            
            row += 1
        
        row += 1  # Add a blank row between class times for readability
    
    writer.close()
