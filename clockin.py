import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta

class TaskTracker:
    def __init__(self, master):
        self.master = master
        master.title("Task Tracker")

        # Connect to SQLite database
        self.conn = sqlite3.connect("task_tracker.db")
        self.create_table()

        # Activities
        self.activities_label = tk.Label(master, text="Select Activity:")
        self.activities_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.activities_combobox = ttk.Combobox(master, values=[
            "Cleaned Bathroom",
            "Cleaned Kitchen",
            "Cleaned Bed Rooms",
            "Folded Blankets",
            "Brushed Teeth",
            "Nourishment",
            "Changed Child",
            "Recited Proficiency",
            "100 Pushups",
            "Six Miles - Elliptical/bike"
        ])
        self.activities_combobox.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.activities_combobox.current(0)

        # Participants
        self.participants_label = tk.Label(master, text="Select Participant:")
        self.participants_label.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        self.participants_combobox = ttk.Combobox(master, values=["Zara", "Jasmin", "Aria"])
        self.participants_combobox.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        self.participants_combobox.current(0)

        # Submit button
        self.submit_button = tk.Button(master, text="Submit", command=self.mark_task)
        self.submit_button.grid(row=2, columnspan=2, padx=10, pady=10)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            activity TEXT,
                            participant TEXT,
                            timestamp TEXT)''')
        self.conn.commit()

    def mark_task(self):
        activity = self.activities_combobox.get()
        participant = self.participants_combobox.get()
        timestamp = self.get_current_time()

        # Insert task into the database
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tasks (activity, participant, timestamp) VALUES (?, ?, ?)",
                       (activity, participant, timestamp))
        self.conn.commit()

        print("Task time marked for", participant)

    def get_current_time(self):
        # Get current UTC time
        utc_now = datetime.utcnow()
        # Convert UTC to PST (UTC - 8 hours)
        pst_now = utc_now - timedelta(hours=8)
        return pst_now.strftime('%Y-%m-%d %H:%M:%S')

def main():
    root = tk.Tk()
    app = TaskTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
