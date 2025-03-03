import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import tkinter.font as tkFont
from tkinter import PhotoImage
from PIL import Image, ImageTk  

VALID_COLLEGES_PROGRAMS = {
    "CCS": ["BSCS", "BSIT", "BSIS", "BSCA"],
    "CSM": ["BSMarB", "BSBio", "BSCHEM", "BSMATH", "BSPHYS", "BSMicB"],
    "COE": ["BSCE", "BSME", "BSCpE", "BSECE", "BSPetE"],
    "CASS": ["BAEL", "BAFL", "BSPsy", "BSHis"]
}

COLLEGE_NAMES = {
    "CCS": "College of Computer Studies",
    "CSM": "College of Science and Mathematics",
    "COE": "College of Engineering",
    "CASS": "College of Arts and Social Sciences"
}

PROGRAM_NAMES = {
    "BSCS": "BS Computer Science",
    "BSIT": "BS Information Technology",
    "BSIS": "BS Information Systems",
    "BSCA": "BS Computer Applications",
    "BSMarB": "BS Marine Biology",
    "BSBio": "BS Biology",
    "BSCHEM": "BS Chemistry",
    "BSMATH": "BS Mathematics",
    "BSPHYS": "BS Physics",
    "BSMicB": "BS Microbiology",
    "BSCE": "BS Civil Engineering",
    "BSME": "BS Mechanical Engineering",
    "BSCpE": "BS Computer Engineering",
    "BSECE": "BS Electronics Engineering",
    "BSPetE": "BS Petroleum Engineering",
    "BAEL": "BA English Language",
    "BAFL": "BA Filipino Language",
    "BSPsy": "BS Psychology",
    "BSHis": "BS History"
}


class StudentForm(tk.Toplevel):
    PROGRAM_TO_CODE = {
            "BS Computer Science": "BSCS",
            "BS Information Technology": "BSIT",
            "BS Information Systems": "BSIS",
            "BS Computer Applications": "BSCA",
            "BS Marine Biology": "BSMarB",
            "BS Biology": "BSBio",
            "BS Chemistry": "BSCHEM",
            "BS Mathematics": "BSMATH",
            "BS Physics": "BSPHYS",
            "BS Microbiology": "BSMicB",
            "BS Civil Engineering": "BSCE",
            "BS Mechanical Engineering": "BSME",
            "BS Computer Engineering": "BSCpE",
            "BS Electronics Engineering": "BSECE",
            "BS Petroleum Engineering": "BSPetE",
            "BA English Language": "BAEL",
            "BA Filipino Language": "BAFL",
            "BS Psychology": "BSPsy",
            "BS History": "BSHis"
        }

    def __init__(self, parent, df, csv_file, student_data=None):
        self.VALID_COLLEGES_PROGRAMS = {
            "CCS": ["BSCS", "BSIT", "BSIS", "BSCA"],
            "CSM": ["BSMarB", "BSBio", "BSCHEM", "BSMATH", "BSPHYS", "BSMicB"],
            "COE": ["BSCE", "BSME", "BSCpE", "BSECE", "BSPetE"],
            "CASS": ["BAEL", "BAFL", "BSPsy", "BSHis"]
        }
        super().__init__(parent)
        self.df = df
        self.csv_file = csv_file
        self.student_data = student_data
        self.title("Student Form")
        self.geometry("450x550")
        self.resizable(False, False)
        self.configure(bg="#e3f2fd")

        self.entries = {}
        
        ttk.Label(self, text="Enter Student Details", font=("Arial", 16, "bold"), background="#e3f2fd").pack(pady=10)
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=20, pady=5, fill="both", expand=True)

        i = 0  

        fields = {
            'First Name': 'text', 'Last Name': 'text', 'ID Number': 'number', 'Age': 'number',
            'Year Level': ['1st Year', '2nd Year', '3rd Year', '4th Year'],
            'Gender': ['Male', 'Female', 'Other']
        }

        for field, field_type in fields.items():
            ttk.Label(form_frame, text=field + ":").grid(row=i, column=0, padx=5, pady=5, sticky="w")
            if isinstance(field_type, list):
                entry = ttk.Combobox(form_frame, values=field_type, state="readonly", width=27)
            else:
                entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[field] = entry
            i += 1  

        # College dropdown
        self.college_var = tk.StringVar()
        self.program_var = tk.StringVar()

        ttk.Label(form_frame, text="College:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.college_dropdown = ttk.Combobox(form_frame, textvariable=self.college_var, values=list(self.VALID_COLLEGES_PROGRAMS.keys()), state="readonly", width=27)
        self.college_dropdown.grid(row=6, column=1, padx=5, pady=5)
        self.college_dropdown.bind("<<ComboboxSelected>>", self.update_program_options)

        ttk.Label(form_frame, text="Program:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.program_dropdown = ttk.Combobox(form_frame, textvariable=self.program_var, state="readonly", width=27)
        self.program_dropdown.grid(row=7, column=1, padx=5, pady=5)

        if student_data:
            self.college_var.set(self.get_college_from_program(student_data["Program"]))
            self.update_program_options()  
            self.program_var.set(student_data["Program"])
        else:
            self.update_program_options()

        self.college_dropdown.bind("<<ComboboxSelected>>", self.update_program_options)

        if student_data:
            for field, value in student_data.items():
                if field in self.entries:
                    self.entries[field].insert(0, str(value))

            if "College" in student_data and "Program" in student_data:
                self.college_var.set(student_data["College"])
                self.update_program_options() 
                self.program_var.set(student_data["Program"])  

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save", command=self.save_student, style="Accent.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.destroy, style="Secondary.TButton").pack(side="right", padx=10)

    def update_program_options(self, event=None):
        selected_college = self.college_var.get()
        programs = self.VALID_COLLEGES_PROGRAMS.get(selected_college, [])

        self.program_dropdown["values"] = programs 

        if programs:
            self.program_var.set(programs[0])
        else:
            self.program_var.set("")  

    def update_college_from_program(self, event=None):
        selected_program = self.program_var.get()
        for college_code, programs in self.VALID_COLLEGES_PROGRAMS.items():
            if selected_program in programs:
                self.college_var.set(college_code)
                return  
    def setup_program_dropdown(self):
        programs = []
        for college_programs in self.VALID_COLLEGES_PROGRAMS.values():
            programs.extend(college_programs)
        self.program_var = tk.StringVar()
        self.program_dropdown = ttk.Combobox(self, textvariable=self.program_var, values=programs, state="readonly")
        self.program_dropdown.grid(row=7, column=1, padx=5, pady=5)
        self.program_dropdown.bind("<<ComboboxSelected>>", self.update_college_from_program)

    def update_program_dropdown(self, event=None):
        selected_college = self.college_var.get()
        programs = VALID_COLLEGES_PROGRAMS.get(selected_college, [])
        self.entries["Program"]["values"] = programs  
        if programs:
            self.program_var.set(programs[0])  
        else:
            self.program_var.set("")  
    def save_student(self):
        print("save_student() called")  # Debugging

        # Retrieve user inputs
        new_data = {
            "First Name": self.entries["First Name"].get(),
            "Last Name": self.entries["Last Name"].get(),
            "ID Number": self.entries["ID Number"].get(),
            "Age": self.entries["Age"].get(),
            "Year Level": self.entries["Year Level"].get(),
            "Gender": self.entries["Gender"].get(),
            "College": self.college_var.get(),
            "Program": self.program_var.get(),
            "College Code": self.get_college_code()  # Ensure this retrieves the correct code
        }

        print("New Data:", new_data)  # Debugging

        # Check if editing an existing record
        if hasattr(self, 'editing_index') and self.editing_index is not None:
            print(f"Updating existing record at index {self.editing_index}")  # Debugging
            self.df.loc[self.editing_index] = new_data  # Update existing row
        else:
            print("Appending new record")  # Debugging
            self.df = pd.concat([self.df, pd.DataFrame([new_data])], ignore_index=True)  # Append new row

        print("Saving DataFrame to CSV...")  # Debugging
        self.df.to_csv(self.csv_file, index=False)  # Save to CSV

        print("Data saved successfully.")  # Debugging

        self.clear_inputs()  # Clear inputs after saving
        self.destroy()  # Close the form


    def update_college_from_program(self, event=None):
        selected_program = self.program_var.get()
        for college, programs in self.VALID_COLLEGES_PROGRAMS.items(): 
            if selected_program in programs:
                self.college_var.set(college)
                return

    def update_program_options(self, event=None):
        selected_college_code = self.college_var.get()  # Get college code
        
        programs = self.VALID_COLLEGES_PROGRAMS.get(selected_college_code, [])
        
        program_names = [PROGRAM_NAMES.get(prog_code, prog_code) for prog_code in programs]
        
        self.program_dropdown["values"] = program_names

        if self.student_data and "Program" in self.student_data:
            full_program_name = PROGRAM_NAMES.get(self.student_data["Program"], self.student_data["Program"])
            self.program_var.set(full_program_name)
        elif program_names:
            self.program_var.set(program_names[0])  
        else:
            self.program_var.set("")

    def clear_inputs(self):
        for entry in self.entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, tk.END)
        
        self.college_var.set("")
        self.program_var.set("")

    def get_college_code(self):
            """Returns the college code based on the selected program."""
            program_name = self.program_var.get()
            college_code = self.PROGRAM_TO_CODE.get(program_name, "Unknown")

            print(f"get_college_code() -> Program: {program_name}, College Code: {college_code}")  # Debugging
            return college_code
    
class StudentManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Manager")
        self.geometry("600x450")
        self.configure(bg="#f5f5f5")  

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton", font=("Arial", 10, "bold"), background="#3498db", foreground="white", padding=6)
        style.map("TButton", background=[("active", "#2980b9")])
        
        self.welcome_screen()

    def clear_search_entry(self, event=None):
        """Clears the search entry and updates the suggestions based on the new category."""
        self.search_entry.set("")
        self.update_suggestions()

    def update_suggestions(self, event=None):
        """Updates the suggestions in the search entry combobox based on the selected category."""
        category = self.search_category.get()
        
        column_map = {
            "Name/ID": ["First Name", "Last Name", "ID Number"],
            "Program": ["Program"],
            "College": ["College"]
        }
        
        columns = column_map.get(category, [])
        if not columns:
            return
        
        suggestions = set()
        for col in columns:
            if col in self.df.columns:
                suggestions.update(self.df[col].dropna().astype(str).tolist())

        search_text = self.search_entry.get().lower()
        filtered_suggestions = [s for s in suggestions if search_text in s.lower()]
        
        self.search_entry["values"] = filtered_suggestions

    def search_students(self):
        query = self.search_entry.get().strip().lower()
        category = self.search_category.get()

        if not query:
            messagebox.showerror("Input Error", "Please enter a search term.")
            return

        column_map = {
            "Name/ID": ["First Name", "Last Name", "ID Number"],
            "Program": ["Program"],
            "College": ["College"]
        }

        columns = column_map.get(category, [])
        if not columns:
            messagebox.showerror("Error", "Invalid search category.")
            return

        filtered_df = self.df[
            self.df[columns].apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)
        ]

        if filtered_df.empty:
            messagebox.showinfo("Search Result", "No matching students found.")
        else:
            self.load_data(filtered_df)


    def welcome_screen(self):
        self.bg_image_path = file=r"D:\New folder\csc151 proj\proj8\proj8.2\CSC151_firstProj\background.jpg"  

        try:
            bg_image = Image.open(self.bg_image_path)
            bg_image = bg_image.resize((700, 500), Image.LANCZOS)  
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(relwidth=1, relheight=1)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")

        # Foreground Frame (Buttons, Labels)
        frame = ttk.Frame(self, padding=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Welcome to Student Manager", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Button(frame, text="Search Student", command=self.load_student_interface, style="TButton").pack(pady=5)

    def load_student_interface(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.csv_file = filedialog.askopenfilename(title="Select Student CSV File", filetypes=[["CSV Files", "*.csv"]])
        if not self.csv_file:
            messagebox.showerror("Error", "No file selected. Returning to main screen.")
            self.welcome_screen()
            return
        
        try:
            self.df = pd.read_csv(self.csv_file, dtype=str)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
            self.welcome_screen()
            return
        
        ttk.Label(self, text="Student Records", font=("Arial", 14, "bold")).pack(pady=10)
        
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=5, padx=10, fill="x")
        
        ttk.Label(search_frame, text="Search by:").pack(side="left", padx=5)
        self.search_category = ttk.Combobox(search_frame, values=["Name/ID", "Program", "College"], state="readonly")
        self.search_category.pack(side="left", padx=5)
        self.search_category.current(0)
        self.search_category.bind("<<ComboboxSelected>>", self.clear_search_entry)
        
        self.search_entry = ttk.Combobox(search_frame)
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.update_suggestions)
        
        ttk.Button(search_frame, text="Find", command=self.search_students).pack(side="left", padx=5)
        
        tree_frame = ttk.Frame(self)
        tree_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Scrollbars
        x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        y_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_frame, columns=self.df.columns.tolist(), show="headings", 
                                xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=tkFont.Font().measure(col) + 80, minwidth=120, stretch=True)

        self.tree.pack(fill="both", expand=True)

        x_scroll.config(command=self.tree.xview)
        y_scroll.config(command=self.tree.yview)
 
        self.tree.bind("<MouseWheel>", lambda event: self.tree.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        
        self.load_data()
        
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        add_button = ttk.Button(button_frame, text="Add Student", command=self.add_student)
        add_button.pack(side="left", padx=5, pady=5)

        edit_button = ttk.Button(button_frame, text="Edit Student", command=self.edit_student)
        edit_button.pack(side="left", padx=5, pady=5)

        delete_button = ttk.Button(button_frame, text="Delete Student", command=self.delete_student)
        delete_button.pack(side="left", padx=5, pady=5)

        # Refresh
        refresh_button = ttk.Button(button_frame, text="Refresh", command=self.refresh_data)
        refresh_button.pack(side="left", padx=5, pady=5)

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item) 

        self.df = pd.read_csv(self.csv_file)

        for _, row in self.df.iterrows():
            program_name = PROGRAM_NAMES.get(row["Program"], row["Program"])  
            
            self.tree.insert("", "end", values=(
                row["First Name"], row["Last Name"], row["ID Number"], row["Age"], 
                row["Year Level"], row["Gender"], row["College"], row["College Code"], program_name
            ))


    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No student selected.")
            return

        student_data = self.tree.item(selected_item)['values']
        student_id = student_data[2]  

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student {student_id}?")
        if confirm:
            self.df = self.df[self.df['ID Number'].astype(str) != str(student_id)]
            self.df.to_csv(self.csv_file, index=False)
            self.tree.delete(selected_item)
            messagebox.showinfo("Success", "Student deleted successfully.")

    def edit_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No student selected.")
            return

        item_values = self.tree.item(selected_item, "values")
        
        if len(item_values) != 9:
            messagebox.showerror("Error", "Unexpected data format.")
            return
        
        first_name, last_name, student_id, _, _, _, college, college_code, program_code = item_values

        name = f"{first_name} {last_name}"
        
        program_name = PROGRAM_NAMES.get(program_code, program_code)
        
        #debug
        print(f"Editing Student: {student_id}, {name}, {college_code}, {program_name}")

        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Student")

        ttk.Label(edit_window, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
        id_entry = ttk.Entry(edit_window)
        id_entry.grid(row=0, column=1, padx=5, pady=5)
        id_entry.insert(0, student_id)
        id_entry.config(state="disabled")

        ttk.Label(edit_window, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(edit_window)
        name_entry.grid(row=1, column=1, padx=5, pady=5)
        name_entry.insert(0, name)

        ttk.Label(edit_window, text="College:").grid(row=2, column=0, padx=5, pady=5)
        college_var = tk.StringVar()
        college_dropdown = ttk.Combobox(edit_window, textvariable=college_var, values=list(COLLEGE_NAMES.keys()), state="readonly")
        college_dropdown.grid(row=2, column=1, padx=5, pady=5)
        college_dropdown.set(next((key for key, value in COLLEGE_NAMES.items() if value == college), college))

        ttk.Label(edit_window, text="Program:").grid(row=3, column=0, padx=5, pady=5)
        program_var = tk.StringVar()
        
        def update_program_options(event=None):
            selected_college = college_var.get()
            program_dropdown["values"] = [PROGRAM_NAMES[code] for code in VALID_COLLEGES_PROGRAMS.get(selected_college, [])]

            if program_name in program_dropdown["values"]:
                program_var.set(program_name)  
            else:
                program_var.set("") 

        program_dropdown = ttk.Combobox(edit_window, textvariable=program_var, state="readonly")
        program_dropdown.grid(row=3, column=1, padx=5, pady=5)

        college_dropdown.bind("<<ComboboxSelected>>", update_program_options)

        update_program_options()

        # Save 
        def save_changes():
            new_name = name_entry.get()
            new_college_acronym = college_var.get()  # This should be the acronym like "CCS"
            new_program_name = program_var.get()

            if not new_name.strip() or not new_college_acronym or not new_program_name:
                messagebox.showerror("Error", "All fields must be filled.")
                return

            new_program_code = next((code for code, full_name in PROGRAM_NAMES.items() if full_name == new_program_name), new_program_name)

            new_college_code = None
            for college, programs in VALID_COLLEGES_PROGRAMS.items():
                if new_program_code in programs:
                    new_college_code = college  
                    break

            if not new_college_code:
                messagebox.showerror("Error", "Invalid College for the selected Program.")
                return

            self.df.loc[self.df["ID Number"] == student_id, ["First Name", "Last Name", "College", "College Code", "Program"]] = [
                new_name.split()[0], 
                new_name.split()[1] if " " in new_name else "", 
                new_college_code,  
                new_program_code,   
                new_program_name    
            ]

            self.df.to_csv(self.csv_file, index=False)
            self.refresh_data()
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def load_data(self, df=None): 
        if df is None:
            df = self.df  
  
        for row in self.tree.get_children():
            self.tree.delete(row)

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    
    def add_student(self):
        StudentForm(self, self.df, self.csv_file)

if __name__ == "__main__":
    app = StudentManagerApp()
    app.mainloop()
