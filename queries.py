import os
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Function to list all database files in the current directory
def list_databases():
    databases = [file for file in os.listdir() if file.endswith(".db")]
    return databases

# Function to connect to the selected database
def connect_to_database(database_name):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        cursor.execute(query)
        tables = cursor.fetchall()
        conn.commit()
        conn.close()
        return [table[0] for table in tables]
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error connecting to database: {e}")
        return None

# Function to execute the query and display results
def execute_query():
    selected_database = selected_database_var.get()
    query = query_entry.get()
    try:
        conn = sqlite3.connect(selected_database)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            result_listbox.insert(tk.END, row)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error executing query: {e}")

# Main GUI
root = tk.Tk()
root.title("Database Viewer")

# List databases in current directory
databases = list_databases()

# Dropdown menu to select database
selected_database_var = tk.StringVar(root)
selected_database_var.set("Select Database")

database_menu = ttk.OptionMenu(root, selected_database_var, *databases)
database_menu.pack(pady=10)

# Connect to selected database
def connect_to_selected_database():
    selected_database = selected_database_var.get()
    if selected_database:
        tables = connect_to_database(selected_database)
        if tables:
            table_info_label.config(text=f"Tables in {selected_database}: {', '.join(tables)}")
        else:
            table_info_label.config(text=f"No tables found in {selected_database}")
    else:
        messagebox.showwarning("Warning", "Please select a database")

connect_button = ttk.Button(root, text="Connect to Database", command=connect_to_selected_database)
connect_button.pack(pady=5)

# Query entry field
query_entry = ttk.Entry(root, width=50)
query_entry.pack(pady=5)

# Query button
query_button = ttk.Button(root, text="Execute Query", command=execute_query)
query_button.pack(pady=5)

# Label to display database tables
table_info_label = ttk.Label(root, text="")
table_info_label.pack(pady=5)

# Listbox to display query results
result_listbox = tk.Listbox(root, width=80, height=20)
result_listbox.pack(pady=5)

root.mainloop()
