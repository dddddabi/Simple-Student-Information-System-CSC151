import csv
import tkinter as tk
from tkinter import ttk

class CollegeManager:
    def __init__(self, parent, csv_file):
        self.parent = parent
        self.csv_file = csv_file
        self.colleges = self.load_colleges()
        self.create_interface()

    def load_colleges(self):
        try:
            with open(self.csv_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                colleges = {}
                for row in reader:
                    college = row['College']
                    program = row['Program']
                    if college in colleges:
                        colleges[college].append(program)
                    else:
                        colleges[college] = [program]
                return colleges
        except FileNotFoundError:
            return {}

    def create_interface(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("College Manager")
        self.window.geometry("400x400")
        
        ttk.Label(self.window, text="College Name:").pack()
        self.college_entry = ttk.Entry(self.window)
        self.college_entry.pack()
        
        self.add_college_button = ttk.Button(self.window, text="Add College", command=self.add_college)
        self.add_college_button.pack()
        
        ttk.Label(self.window, text="Program Name:").pack()
        self.program_entry = ttk.Entry(self.window)
        self.program_entry.pack()
        
        self.college_dropdown = ttk.Combobox(self.window, values=list(self.colleges.keys()), state="readonly")
        self.college_dropdown.pack()
        
        self.add_program_button = ttk.Button(self.window, text="Add Program", command=self.add_program)
        self.add_program_button.pack()
        
        self.delete_college_button = ttk.Button(self.window, text="Delete College", command=self.delete_college)
        self.delete_college_button.pack()
        
        self.delete_program_button = ttk.Button(self.window, text="Delete Program", command=self.delete_program)
        self.delete_program_button.pack()
        
        self.status_label = ttk.Label(self.window, text="")
        self.status_label.pack()

    def add_college(self):
        college_name = self.college_entry.get().strip()
        if college_name:
            if college_name not in self.colleges:
                self.colleges[college_name] = []
                self.save_colleges()
                self.status_label.config(text=f"College '{college_name}' added successfully.")
                self.college_dropdown['values'] = list(self.colleges.keys())
            else:
                self.status_label.config(text="College already exists.")
        else:
            self.status_label.config(text="Please enter a college name.")

    def add_program(self):
        program_name = self.program_entry.get().strip()
        selected_college = self.college_dropdown.get()
        if program_name and selected_college:
            if program_name not in self.colleges[selected_college]:
                self.colleges[selected_college].append(program_name)
                self.save_colleges()
                self.status_label.config(text=f"Program '{program_name}' added to '{selected_college}'.")
            else:
                self.status_label.config(text="Program already exists in this college.")
        else:
            self.status_label.config(text="Please select a college and enter a program name.")

    def delete_college(self):
        selected_college = self.college_dropdown.get()
        if selected_college:
            if selected_college in self.colleges:
                del self.colleges[selected_college]
                self.save_colleges()
                self.status_label.config(text=f"College '{selected_college}' deleted.")
                self.college_dropdown['values'] = list(self.colleges.keys())
            else:
                self.status_label.config(text="Selected college does not exist.")
        else:
            self.status_label.config(text="Please select a college to delete.")

    def delete_program(self):
        selected_college = self.college_dropdown.get()
        program_name = self.program_entry.get().strip()
        if selected_college and program_name:
            if selected_college in self.colleges and program_name in self.colleges[selected_college]:
                self.colleges[selected_college].remove(program_name)
                self.save_colleges()
                self.status_label.config(text=f"Program '{program_name}' deleted from '{selected_college}'.")
            else:
                self.status_label.config(text="Program not found in the selected college.")
        else:
            self.status_label.config(text="Please select a college and enter a program name to delete.")

    def save_colleges(self):
        with open(self.csv_file, 'w', newline='') as csvfile:
            fieldnames = ['College', 'Program']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for college, programs in self.colleges.items():
                for program in programs:
                    writer.writerow({'College': college, 'Program': program})
