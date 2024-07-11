import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
import json

from tools.time_availability import TimeBlock
from tools.day import Day

class FileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instructor Availability Entry")
        
        self.root.geometry("400x180")  # Fixed width and height

        self.file_label = tk.Label(self.root, text="Select desired SwimNOVA Instructor Availability .CSV file:")
        self.file_label.pack(pady=5)
        
        self.file_entry = tk.Entry(self.root)
        self.file_entry.pack(pady=5)
        
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(padx=10, pady=10)
        
        self.submit_button = tk.Button(self.root, text="Next", command=self.submit)
        self.submit_button.pack(pady=20)
        
        self.result = None
        
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)
    
    def submit(self):
        file = self.file_entry.get()
        self.result = file
        self.root.quit()
        self.root.destroy()
    
    def get_result(self):
        self.root.mainloop()
        return self.result

def setup_file_gui():
    root = tk.Tk()
    app = FileApp(root)
    result = app.get_result()
    return result


class DateApp:
    def __init__(self, root, session_index, session_times, level_count):
        self.root = root
        self.root.title("Session Date and Availability Input")
        self.root.geometry("400x600")  # Fixed width and height

        # Create main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Create canvas
        self.canvas = tk.Canvas(main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Add scrollbar to the canvas
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create another frame inside the canvas
        self.inner_frame = tk.Frame(self.canvas)

        # Add that frame to a window in the canvas
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.session_label = tk.Label(self.inner_frame, text=f"Session #{session_index + 1}", font=('Arial', 16))
        self.session_label.pack(pady=10)
        
        self.start_date_label = tk.Label(self.inner_frame, text="Select session start date:")
        self.start_date_label.pack(pady=5)
        
        self.start_date_entry = DateEntry(self.inner_frame)
        self.start_date_entry.pack(pady=5)
        
        self.end_date_label = tk.Label(self.inner_frame, text="Select session end date:")
        self.end_date_label.pack(pady=5)
        
        self.end_date_entry = DateEntry(self.inner_frame)
        self.end_date_entry.pack(pady=5)
        
        self.session_label = tk.Label(self.inner_frame, text="Enter Amount of Swimmers by Level", font=('Arial', 16))
        self.session_label.pack(pady=25)
        
        self.swimmer_counts_by_level = []
        for time in session_times:
            time_frame = tk.Frame(self.inner_frame)
            time_frame.pack(pady=10)
            
            tk.Label(time_frame, text=f"Time: {TimeBlock.from_json(time)}").pack()
            
            level_entries = []
            for level in range(level_count):
                level_frame = tk.Frame(time_frame)
                level_frame.pack()
                tk.Label(level_frame, text=f"Level {level+1}:").pack(side=tk.LEFT)
                entry = tk.Entry(level_frame, width=5)
                entry.pack(side=tk.LEFT)
                level_entries.append(entry)
            
            self.swimmer_counts_by_level.append(level_entries)
        
        self.submit_button = tk.Button(self.inner_frame, text="Next", command=self.submit)
        self.submit_button.pack(pady=20)
        
        self.start_date = None
        self.end_date = None
        self.swimmer_counts = None

        # Update the scrollregion after starting mainloop
        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def submit(self):
        self.start_date = date_entry_to_day(self.start_date_entry)
        self.end_date = date_entry_to_day(self.end_date_entry)
        self.swimmer_counts = self.get_swimmer_counts()
        self.root.quit()
        self.root.destroy()
    
    def get_result(self):
        self.root.mainloop()
        return self.start_date, self.end_date, self.swimmer_counts

    def get_swimmer_counts(self):
        swimmer_counts_by_level = []
        for time_entries in self.swimmer_counts_by_level:
            level_counts = []
            for entry in time_entries:
                try:
                    count = int(entry.get())
                except ValueError:
                    count = 0
                level_counts.append(count)
            swimmer_counts_by_level.append(level_counts)
        return swimmer_counts_by_level

def date_entry_to_day(date_entry):
    selected_date = date_entry.get_date()
    return Day(selected_date.year, selected_date.month, selected_date.day)

def setup_date_gui(session_index):
    root = tk.Tk()
    with open("settings.json") as f:
        settings = json.load(f)
    app = DateApp(root, session_index, settings["session_times"], settings["highest_level"])
    result = app.get_result()
    
    start_date, end_date, swimmer_counts_by_level = result
    
    return start_date, end_date, swimmer_counts_by_level