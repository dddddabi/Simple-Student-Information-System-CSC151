import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from student import StudentForm
from college_manager import CollegeManager  

class StudentManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Manager")
        self.geometry("600x450")
        self.configure(bg="#E3F2FD")
        self.csv_file = "file.csv"
        self.df = None  
        self.welcome_screen()

    def welcome_screen(self):
        self.clear_screen()
        self.configure(bg="#E3F2FD")
        
        style = ttk.Style()
        style.configure("Big.TButton", font=("Arial", 14, "bold"), padding=10)
        
        tk.Label(self, text="STUDENT MANAGEMENT SYSTEM", font=("Arial", 20, "bold"), bg="#E3F2FD", fg="#0D47A1").pack(pady=10)
        ttk.Button(self, text="Student Management", command=self.load_student_interface, style="Big.TButton", width=50).pack(pady=20)
        ttk.Button(self, text="Manage Colleges & Programs", command=self.open_college_manager, style="Big.TButton", width=50).pack(pady=20)
        ttk.Button(self, text="Exit", command=self.quit, style="Big.TButton", width=20).pack(pady=5)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def load_student_interface(self):
        if self.df is None:
            file_path = filedialog.askopenfilename(title="Select Student CSV File", filetypes=[("CSV Files", "*.csv")])
            if not file_path:
                messagebox.showwarning("No File Selected", "Returning to main menu.")
                self.welcome_screen()
                return
            try:
                self.df = pd.read_csv(file_path, dtype=str)
                self.csv_file = file_path
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
                self.welcome_screen()
                return

        self.clear_screen()
        self.configure(bg="#E3F2FD")
        ttk.Label(self, text="Student Records", font=("Arial", 16, "bold"), background="#E3F2FD", foreground="#0D47A1").pack(pady=10)

        search_frame = ttk.Frame(self)
        search_frame.pack(pady=5, padx=10, fill="x")

        ttk.Label(search_frame, text="Search by:").pack(side="left", padx=5)
        self.search_category = ttk.Combobox(search_frame, values=["Name/ID", "Program", "College"], state="readonly")
        self.search_category.pack(side="left", padx=5)
        self.search_category.bind("<<ComboboxSelected>>", self.update_search_values)  # Add this line

        self.search_entry = ttk.Combobox(search_frame, values=[])
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)

        ttk.Button(search_frame, text="Find", command=self.search_students).pack(side="left", padx=5)

        columns = ["First Name", "Last Name", "ID Number", "Age", "Year Level", "Gender", "College", "College Code", "Program"]

        # for scrollbars
        table_frame = ttk.Frame(self)
        table_frame.pack(pady=5, fill="both", expand=True)
        # Vertical scrollbar
        v_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        # Horizontal scrollbar
        h_scroll = ttk.Scrollbar(table_frame, orient="horizontal")
        # Create the Treeview table with scrollbars
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings",
            yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

        # column headings and width
        for col in columns:
            if col == "College"or"College Code":
                self.tree.heading(col, text=col, anchor="center")  # Center header text
                self.tree.column(col, width=120, anchor="center")  # Center data
            else:
                self.tree.heading(col, text=col, anchor="w")  # Keep others left-aligned
                self.tree.column(col, width=120, anchor="w")

        self.tree.pack(fill="both", expand=True)

        self.load_data()
        #buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Add Student", command=self.add_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edit Student", command=self.edit_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Student", command=self.delete_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.welcome_screen).pack(side="left", padx=5)

    def update_search_values(self, event=None):
        category = self.search_category.get()
        
        self.search_entry.set("")  
        
        column_map = {
            "Name/ID": ["First Name", "Last Name", "ID Number"],
            "Program": ["Program"],
            "College": ["College"]
        }

        valid_columns = column_map.get(category, [])

        if not valid_columns:
            self.search_entry["values"] = []
            return

        # for sorting values from selected columns 
        unique_values = sorted(set(self.df[valid_columns].values.flatten().astype(str)))
        self.search_entry["values"] = unique_values

    def load_data(self, df=None):
        if df is None:
            df = self.df  

        for row in self.tree.get_children():
            self.tree.delete(row)

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))


    def search_students(self):
        query = self.search_entry.get().strip().lower()
        category = self.search_category.get()

        if not query:
            self.load_data()
            return

        column_map = {
            "Name/ID": ["First Name", "Last Name", "ID Number"],
            "Program": ["Program"],
            "College": ["College"]
        }
        
        columns = column_map.get(category, [])
        valid_columns = [col for col in columns if col in self.df.columns]

        if not valid_columns:
            messagebox.showerror("Error", "Search category does not match any columns in the dataset.")
            return

        filtered_df = self.df[self.df[valid_columns].apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)]
        
        self.load_data(filtered_df)


    def refresh_data(self):
        self.df = pd.read_csv(self.csv_file, dtype=str)
        self.load_data()

    def add_student(self):
        StudentForm(self, self.df, self.csv_file)

    def edit_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to edit.")
            return
        student_data = self.tree.item(selected_item)["values"]
        if not student_data:
            messagebox.showwarning("Error", "Failed to retrieve student data.")
            return
        StudentForm(self, self.df, self.csv_file, student_data)

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No student selected.")
            return
        student_id = self.tree.item(selected_item)["values"][2]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student {student_id}?"):
            self.df = self.df[self.df["ID Number"] != student_id]
            self.df.to_csv(self.csv_file, index=False)
            self.tree.delete(selected_item)
            messagebox.showinfo("Success", "Student deleted successfully.")

    def open_college_manager(self):
        if not hasattr(self, 'csv_file') or not self.csv_file:
            messagebox.showerror("Error", "Please open a student CSV first.")
            return
        
        self.college_manager = CollegeManager(self, self.csv_file)  

if __name__ == "__main__":
    app = StudentManagerApp()
    app.mainloop()
