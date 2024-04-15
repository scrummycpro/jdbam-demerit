# Appointment Scheduler Application

This is an Appointment Scheduler Application built with Python and Tkinter. It allows users to schedule appointments and stores them in a SQLite database.

## Files in this directory

- `tracing-board.py`: This is the main script for the Appointment Scheduler Application. It defines the GUI and the functions to schedule appointments.

## How the code works

The `tracing-board.py` script creates a Tkinter window with the Appointment Scheduler interface. The interface includes a calendar to select the appointment date, a dropdown menu to select the appointment time, and a text box to enter the appointment description.

The `generate_time_options` function generates a list of time options in 30-minute increments, which are used to populate the dropdown menu.

The `save_appointment` function gets the selected date, time, and description, connects to the SQLite database `appointments.db`, and saves the appointment in the `appointments` table.

## How to run the application

1. Ensure you have Python installed on your machine.
2. Run the `tracing-board.py` script in a Python environment.

```bash
python tracing-board.py