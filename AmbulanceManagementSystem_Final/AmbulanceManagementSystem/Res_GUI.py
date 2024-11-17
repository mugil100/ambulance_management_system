import tkinter as tk
from tkinter import messagebox, PhotoImage
import webbrowser
import os
import Shortest_path as py

def GUI(hn, hd, an, ad):
    driver_points = {
        "A": {"coordinates": [10.6600, 77.0050], "name": "Alice", "contact": "+91 98765 43210", "ambulance_id": "AMB001"},
        "B": {"coordinates": [10.66327, 77.01779], "name": "Bob", "contact": "+91 98765 43211", "ambulance_id": "AMB002"},
        "C": {"coordinates": [10.6670, 77.0125], "name": "Charlie", "contact": "+91 98765 43212", "ambulance_id": "AMB003"},
        "D": {"coordinates": [10.6685, 77.0070], "name": "David", "contact": "+91 98765 43213", "ambulance_id": "AMB004"},
        "E": {"coordinates": [10.6555, 77.0100], "name": "Eve", "contact": "+91 98765 43214", "ambulance_id": "AMB005"},
        "F": {"coordinates": [10.6615, 77.0070], "name": "Frank", "contact": "+91 98765 43215", "ambulance_id": "AMB006"}
    }

    ambulance_driver = driver_points.get(an, {"name": "Unknown", "contact": "N/A", "ambulance_id": "N/A"})
    
    hospital_details = {
        "name": hn,
        "distance": f"{hd} K.m."
    }

    def show_map():
        py.map_show()
        map_file_path = "Map.html"
        if os.path.exists(map_file_path):
            webbrowser.open(map_file_path)
        else:
            messagebox.showerror("Error", "Map file not found.")

    def exit_app():
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            root.destroy()

    root = tk.Tk()
    root.title("Ambulance Service System")
    root.geometry("925x500+300+200")
    root.config(bg="#ffffff")
    root.wm_iconbitmap(r"data/icon.ico")  

    # Load and display the image
    img = PhotoImage(file=r"data/GUI.png")
    labelicon = tk.Label(root, image=img, bg='#ffffff')
    labelicon.grid(row=0, column=0, rowspan=5, padx=20, pady=200)

    # Create a frame for the content
    frame = tk.Frame(root, width=350, height=350, bg="white")
    frame.grid(row=0, column=1, padx=10, pady=10)

    # Header label
    headlabel = tk.Label(frame, text="Ambulance Service System", font=("Times Roman", 24, "bold"), bg="#ffffff", fg="#ce3847")
    headlabel.grid(row=0, column=0, columnspan=2, pady=20)

    driver_frame = tk.LabelFrame(frame, text="Ambulance Driver Details", font=("Helvetica", 14), bg="white", fg="black", padx=10, pady=10)
    driver_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    driver_name = tk.Label(driver_frame, text=f"Driver Name: {ambulance_driver['name']}", font=("Helvetica", 12), bg="white")
    driver_name.grid(row=0, column=0, sticky="w", padx=5, pady=2)

    driver_contact = tk.Label(driver_frame, text=f"Contact: {ambulance_driver['contact']}", font=("Helvetica", 12), bg="white")
    driver_contact.grid(row=1, column=0, sticky="w", padx=5, pady=2)

    driver_id = tk.Label(driver_frame, text=f"Ambulance ID: {ambulance_driver['ambulance_id']}", font=("Helvetica", 12), bg="white")
    driver_id.grid(row=2, column=0, sticky="w", padx=5, pady=2)
    
    driver_distance = tk.Label(driver_frame, text=f"Ambulance Distance: {ad}", font=("Helvetica", 12), bg="white")
    driver_distance.grid(row=3, column=0, sticky="w", padx=5, pady=2)
    
    hospital_frame = tk.LabelFrame(frame, text="Hospital Details", font=("Helvetica", 14), bg="white", fg="black", padx=10, pady=10)
    hospital_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    hospital_name = tk.Label(hospital_frame, text=f"Hospital Name: {hospital_details['name']}", font=("Helvetica", 12), bg="white")
    hospital_name.grid(row=0, column=0, sticky="w", padx=5, pady=2)

    hospital_distance = tk.Label(hospital_frame, text=f"Distance: {hospital_details['distance']}", font=("Helvetica", 12), bg="white")
    hospital_distance.grid(row=1, column=0, sticky="w", padx=5, pady=2)

    button_frame = tk.Frame(frame, bg="white")
    button_frame.grid(row=4, column=0, columnspan=2, pady=20)

    show_map_button = tk.Button(button_frame, text="Show Map", font=("Helvetica", 14), bg="#4CAF50", fg="white", command=show_map)
    show_map_button.grid(row=0, column=0, padx=20)

    exit_button = tk.Button(button_frame, text="Exit", font=("Helvetica", 14), bg="#f44336", fg="white", command=exit_app)
    exit_button.grid(row=0, column=1, padx=20)

    root.mainloop()


def main(hn, hd, an, ad):
    GUI(hn, hd, an, ad)