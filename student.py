import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from database import extract_colleges_programs as load_colleges_programs

class StudentForm(tk.Toplevel):
    def __init__(self, parent, df, csv_file, student_data=None):
        super().__init__(parent)
        self.df = df
        self.csv_file = csv_file
        self.student_data = student_data
        self.title("Student Form")
        self.geometry("450x550")
        self.configure(bg="#E3F2FD")

        self.entries = {}
        self.colleges_programs, _ = load_colleges_programs(csv_file)

        # Define dropdown values
        gender_options = ["Male", "Female", "Other"]
        year_levels = ["1st Year", "2nd Year", "3rd Year", "4th Year", "4+ years"]

        # Labels and Entry fields
        fields = ["First Name", "Last Name", "ID Number", "Age"]
        for i, field in enumerate(fields):
            tk.Label(self, text=field + ":", bg="#E3F2FD").grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(self, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry  # Store only text fields in self.entries

        # Year Level Dropdown
        self.year_var = tk.StringVar()
        tk.Label(self, text="Year Level:", bg="#E3F2FD").grid(row=len(fields), column=0, padx=10, pady=5, sticky="e")
        self.year_dropdown = ttk.Combobox(self, textvariable=self.year_var, values=year_levels, state="readonly", width=27)
        self.year_dropdown.grid(row=len(fields), column=1, padx=10, pady=5)
        self.year_var.set("")  

        # Gender Dropdown
        self.gender_var = tk.StringVar()
        tk.Label(self, text="Gender:", bg="#E3F2FD").grid(row=len(fields) + 1, column=0, padx=10, pady=5, sticky="e")
        self.gender_dropdown = ttk.Combobox(self, textvariable=self.gender_var, values=gender_options, state="readonly", width=27)
        self.gender_dropdown.grid(row=len(fields) + 1, column=1, padx=10, pady=5)
        self.gender_var.set("")  

        # College Dropdown
        self.college_var = tk.StringVar()
        tk.Label(self, text="College:", bg="#E3F2FD").grid(row=len(fields) + 2, column=0, padx=10, pady=5, sticky="e")
        self.college_dropdown = ttk.Combobox(self, textvariable=self.college_var, 
                                             values=list(self.colleges_programs.keys()), state="readonly", width=27)
        self.college_dropdown.grid(row=len(fields) + 2, column=1, padx=10, pady=5)

        # Program Dropdown
        self.program_var = tk.StringVar()
        tk.Label(self, text="Program:", bg="#E3F2FD").grid(row=len(fields) + 3, column=0, padx=10, pady=5, sticky="e")
        self.program_dropdown = ttk.Combobox(self, textvariable=self.program_var, values=[], state="readonly", width=27)
        self.program_dropdown.grid(row=len(fields) + 3, column=1, padx=10, pady=5)

        # Bind college dropdown change to update programs
        self.college_dropdown.bind("<<ComboboxSelected>>", self.update_programs)

        # Pre-fill data if editing a student
        if self.student_data:
            self.fill_student_data()

        # Buttons
        ttk.Button(self, text="Save", command=self.save_student).grid(row=len(fields) + 4, column=0, columnspan=2, pady=10)

    def update_programs(self, event=None):
        """Update program dropdown based on selected college."""
        selected_college = self.college_var.get().strip()  
        if selected_college in self.colleges_programs:
            self.program_dropdown["values"] = self.colleges_programs[selected_college]
        else:
            self.program_dropdown["values"] = []  

        self.program_var.set("") 

    def fill_student_data(self):
        if self.student_data:
            # Convert list to dictionary using column names from DataFrame
            student_dict = dict(zip(self.df.columns, self.student_data))
            
            self.student_data = student_dict  # Now it's a dictionary

            # Fill entries
            for field in self.entries:
                self.entries[field].insert(0, student_dict[field])

            # Set dropdown values
            self.year_var.set(student_dict["Year Level"])
            self.gender_var.set(student_dict["Gender"])
            self.college_var.set(student_dict["College"])
            self.program_var.set(student_dict["Program"])


    def save_student(self):
        missing_fields = []

        # Check if all text entry fields are filled
        for field, entry in self.entries.items():
            if not entry.get().strip():
                missing_fields.append(field)

        # Check dropdown selections
        if not self.year_var.get().strip():
            missing_fields.append("Year Level")
        if not self.gender_var.get().strip():
            missing_fields.append("Gender")
        if not self.college_var.get().strip():
            missing_fields.append("College")
        if not self.program_var.get().strip():
            missing_fields.append("Program")

        if missing_fields:
            messagebox.showerror("Error", f"Please fill in the following fields: {', '.join(missing_fields)}")
            return  # Stop function if fields are missing

        selected_college = self.college_var.get().strip()
        college_code = next((code for code, name in self.colleges_programs.items() if name == selected_college), "Unknown")

        # Get entered data
        student_data = {
            "First Name": self.entries["First Name"].get().strip(),
            "Last Name": self.entries["Last Name"].get().strip(),
            "ID Number": self.entries["ID Number"].get().strip(),
            "Age": self.entries["Age"].get().strip(),
            "Year Level": self.year_var.get().strip(),
            "Gender": self.gender_var.get().strip(),
            "College": self.college_var.get().strip(),
            "College Code": college_code,
            "Program": self.program_var.get().strip(),
        }

        # **Check if student already exists (based on ID Number)**
        if self.student_data:
            student_id = self.student_data["ID Number"]  
            index = self.df.index[self.df["ID Number"] == student_id].tolist()

            if index:
                # Update the existing student record
                for key, value in student_data.items():
                    self.df.at[index[0], key] = value
            else:
                # If ID not found, add as a new student
                self.df = pd.concat([self.df, pd.DataFrame([student_data])], ignore_index=True)
        else:
            # If this is a new student, add them to the DataFrame
            self.df = pd.concat([self.df, pd.DataFrame([student_data])], ignore_index=True)

        # Save DataFrame to CSV
        self.df.to_csv(self.csv_file, index=False)

        messagebox.showinfo("Success", "Student details saved successfully!")
        self.destroy()  # Close form after saving
