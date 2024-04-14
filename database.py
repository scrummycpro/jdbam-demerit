import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta

# Function to create the SQLite database and the 'demerits' table
def create_database():
    try:
        conn = sqlite3.connect('demerits.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS demerits
                     (id INTEGER PRIMARY KEY,
                     demerit_type TEXT,
                     person TEXT,
                     notes TEXT,
                     date_added TEXT)''')  # Using TEXT for date_added
        print("Table created successfully.")
        conn.commit()
    except sqlite3.Error as e:
        print("Error creating table:", e)
    finally:
        conn.close()

# Function to add demerit to the database
def add_demerit():
    demerit_type = demerit_var.get()
    person = person_var.get()
    notes = notes_entry.get("1.0", "end").strip()

    # Get current date and time
    current_time = datetime.now()

    # Format date_added
    date_added = current_time.strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('demerits.db')
    c = conn.cursor()
    c.execute("INSERT INTO demerits (demerit_type, person, notes, date_added) VALUES (?, ?, ?, ?)",
              (demerit_type, person, notes, date_added))
    conn.commit()
    conn.close()

    # Clearing the entry fields after adding the demerit
    demerit_var.set("")
    person_var.set("")
    notes_entry.delete("1.0", "end")

    # Display success message
    success_label.config(text="Demerit Successfully saved to database")

# Create the main application window
root = tk.Tk()
root.title("Demerits Database")

# Create SQLite database and table
create_database()

# Person dropdown
person_label = ttk.Label(root, text="Select Person:")
person_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
persons = ['Zara', 'Jasmin', 'Aria']
person_var = tk.StringVar()
person_dropdown = ttk.Combobox(root, textvariable=person_var, values=persons, state="readonly")
person_dropdown.grid(row=0, column=1, padx=10, pady=5)

# Demerit types dropdown
demerit_label = ttk.Label(root, text="Select Demerit:")
demerit_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
demerits = ['Theft', 'Insubordination', 'Negligence', 'Intemperance', 'Incompetence']
demerit_var = tk.StringVar()
demerit_dropdown = ttk.Combobox(root, textvariable=demerit_var, values=demerits, state="readonly")
demerit_dropdown.grid(row=1, column=1, padx=10, pady=5)

# Notes input
notes_label = ttk.Label(root, text="Notes:")
notes_label.grid(row=2, column=0, padx=10, pady=5, sticky="ne")
notes_entry = tk.Text(root, height=5, width=30)
notes_entry.grid(row=2, column=1, padx=10, pady=5)

# Add Demerit button
add_button = ttk.Button(root, text="Add Demerit", command=add_demerit)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

# Success message label
success_label = ttk.Label(root, text="")
success_label.grid(row=4, column=0, columnspan=2)

root.mainloop()
