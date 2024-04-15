# Task Tracker Application

This is a Task Tracker Application built with Python and Tkinter. It allows users to track the time they spend on different tasks.

## Files in this directory

- `clockin.py`: This is the main script for the Task Tracker Application. It defines the GUI and the functions to track tasks.

## How the code works

The `clockin.py` script creates a Tkinter window with the Task Tracker interface. The TaskTracker class defines the layout of the interface and the functions to start, stop, and save tasks.

The `get_pst_time` function gets the current time in UTC, converts it to PST (Pacific Standard Time), and returns it as a string in the format 'YYYY-MM-DD HH:MM:SS'.

The `main` function creates a Tkinter root window, creates an instance of the TaskTracker class, and starts the Tkinter event loop.

## How to run the application

1. Ensure you have Python installed on your machine.
2. Run the `clockin.py` script in a Python environment.

```bash
python clockin.py