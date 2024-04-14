import tkinter as tk
from tkinter import ttk, filedialog
import sqlite3
from tkcalendar import Calendar
from ttkthemes import ThemedTk

# Function to generate time options in 30-minute increments
def generate_time_options():
    times = []
    for hour in range(0, 24):
        for minute in range(0, 60, 30):
            times.append(f"{hour % 12 or 12}:{'00' if minute == 0 else '30'} {'AM' if hour < 12 else 'PM'}")
    return times

# Function to save appointment to SQLite database
def save_appointment():
    appointment_date = cal.get_date()
    appointment_time = time_var.get()
    appointment_description = description_entry.get("1.0", tk.END)
    
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS appointments
                 (date text, time text, description text)''')
    c.execute("INSERT INTO appointments (date, time, description) VALUES (?, ?, ?)",
              (appointment_date, appointment_time, appointment_description))
    conn.commit()
    conn.close()

    clear_form()

# Function to clear the form fields
def clear_form():
    cal.clear()
    description_entry.delete("1.0", tk.END)

# Function to display saved appointments
def display_appointments():
    appointments_window = tk.Toplevel(root)
    appointments_window.title("Appointments")
    
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute("SELECT * FROM appointments")
    appointments = c.fetchall()
    conn.close()
    
    if not appointments:
        tk.Label(appointments_window, text="No appointments found.").pack()
    else:
        for appointment in appointments:
            tk.Label(appointments_window, text=f"Date: {appointment[0]}, Time: {appointment[1]}\nDescription: {appointment[2]}").pack()

# Function to export appointments to a text file using a file dialog
def export_appointments():
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute("SELECT * FROM appointments")
    appointments = c.fetchall()
    conn.close()
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    
    if file_path:
        with open(file_path, "w") as f:
            for appointment in appointments:
                f.write(f"Date: {appointment[0]}, Time: {appointment[1]}, Description: {appointment[2]}\n")

# Main GUI
root = ThemedTk(theme="radiance")
root.title("Appointment Scheduler")

# Calendar widget
cal = Calendar(root, selectmode='day', date_pattern='y-mm-dd')
cal.pack(pady=10)

# Time selection dropdown
times = generate_time_options()
time_var = tk.StringVar(root)
time_var.set(times[0])
time_label = ttk.Label(root, text="Time:")
time_label.pack()
time_menu = ttk.Combobox(root, textvariable=time_var, values=times, state="readonly")
time_menu.pack()

# Text widget for description
description_label = ttk.Label(root, text="Description:")
description_label.pack()
description_entry = tk.Text(root, height=5, width=30)
description_entry.pack()

# Save button
save_button = ttk.Button(root, text="Save Appointment", command=save_appointment)
save_button.pack()

# Display appointments button
display_button = ttk.Button(root, text="Display Appointments", command=display_appointments)
display_button.pack()

# Export appointments button
export_button = ttk.Button(root, text="Export Appointments", command=export_appointments)
export_button.pack()

root.mainloop()
