import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import webbrowser
import os

class AdminGUI:
    def __init__(self, root, association_value=None):
        self.root = root
        self.root.title("Administrator Panel")
        self.root.geometry("600x400")
        self.root.config(bg="#ffffff")
        
        # Store the association value
        self.association_value = association_value

        # Set up icon
        if os.path.exists("data/icon.ico"):
            self.root.wm_iconbitmap("data/icon.ico")
        else:
            print("icon.ico not found.")

        # Loading the image and keeping a reference to it
        if os.path.exists("data/GUI.png"):
            self.img = tk.PhotoImage(file="data/GUI.png")
            labelicon = tk.Label(root, image=self.img, bg="#ffffff")
            labelicon.grid(row=0, column=0, rowspan=5, padx=20, pady=10)
        else:
            print("GUI.png not found.")

        # Title label
        self.title_label = tk.Label(root, text="Administrator Panel", font=("Arial", 16), bg="#ffffff")
        self.title_label.grid(row=0, column=1, pady=5)

        # Ambulance Service System heading
        self.headlabel = tk.Label(root, text="Ambulance Service System", font=("Times Roman", 16, "bold"), bg="#ffffff", fg="#ce3847")
        self.headlabel.grid(row=1, column=1, pady=(5, 0))

        # Buttons with red background
        self.user_map_button = tk.Button(root, text="View Map", command=self.map_view, bg="red", fg="white")
        self.user_map_button.grid(row=2, column=1, pady=5)

        self.view_logs_button = tk.Button(root, text="View Logs", command=self.view_logs, bg="red", fg="white")
        self.view_logs_button.grid(row=3, column=1, pady=5)

        self.association_button = tk.Button(root, text="Analyze Association", command=self.analyze_association, bg="red", fg="white")
        self.association_button.grid(row=4, column=1, pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app, bg="red", fg="white")
        self.exit_button.grid(row=5, column=1, pady=5)

        # Treeview for logs with scrollbar
        self.tree = ttk.Treeview(root)
        self.tree.grid(row=6, column=0, columnspan=2, pady=10, sticky='nsew')
        self.tree_scroll = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.grid(row=6, column=2, sticky='ns')

        # Configure grid weights
        root.grid_rowconfigure(6, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def map_view(self):
        if os.path.exists("Map.html"):
            try:
                webbrowser.open("Map.html")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open the map: {e}")
        else:
            messagebox.showerror("Error", "Map.html not found.")

    def view_logs(self):
        excel_file = "data/AmbulanceServiceData.xlsx"
        if os.path.exists(excel_file):
            try:
                df = pd.read_excel(excel_file)
                self.populate_treeview(df)
            except Exception as e:
                messagebox.showerror("Error", f"Could not read the logs: {e}")
        else:
            messagebox.showerror("Error", "AmbulanceServiceData.xlsx not found.")

    def populate_treeview(self, df):
        # Clear the Treeview
        self.tree.delete(*self.tree.get_children())
        
        # Setup columns and headings
        self.tree["columns"] = list(df.columns)
        self.tree["show"] = "headings"
        
        for column in df.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor="center", width=max(100, int(df[column].astype(str).map(len).max() * 7)))

        # Insert rows
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def exit_app(self):
        self.root.destroy()
        
    def analyze_association(self):
        if self.association_value is None:
            messagebox.showwarning("Warning", "No association value provided.")
            return
        
        # Determine the association strength
        strength = self.get_association_strength(self.association_value)
        messagebox.showinfo("Association Analysis", f"The association strength is: {strength} (Value: {self.association_value:0.4f})")

    def get_association_strength(self, value):
        """Determines the strength of the association based on the value."""
        if 0.00 <= value < 0.10:
            return "Very weak association"
        elif 0.10 <= value < 0.30:
            return "Weak association"
        elif 0.30 <= value < 0.50:
            return "Moderate association"
        elif 0.50 <= value < 0.70:
            return "Strong association"
        elif 0.70 <= value <= 1.00:
            return "Very strong association"
        else:
            return "Invalid value"
    
    def set_association_value(self, value):
        """Updates the association value if it changes externally."""
        self.association_value = value

def gui(association_value=None):
    root = tk.Tk()
    app = AdminGUI(root, association_value=association_value)
    root.mainloop()
