import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from subprocess import Popen

# Function to launch database.py
def launch_database_program():
    try:
        Popen(["python", "database.py"])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to launch clockin.py
def launch_clockin_program():
    try:
        Popen(["python", "clockin.py"])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to launch tracing-board.py
def launch_tracing_board_program():
    try:
        Popen(["python", "tracing-board.py"])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Main Dashboard Program
root = tk.Tk()
root.title("Dashboard")

# Buttons to launch programs
database_button = ttk.Button(root, text="Launch Database Program", command=launch_database_program)
database_button.pack(pady=10)

clockin_button = ttk.Button(root, text="Launch Clockin Program", command=launch_clockin_program)
clockin_button.pack(pady=10)

tracing_board_button = ttk.Button(root, text="Launch Tracing Board Program", command=launch_tracing_board_program)
tracing_board_button.pack(pady=10)

root.mainloop()
