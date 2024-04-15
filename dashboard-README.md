# Dashboard Application

This is a Dashboard Application built with Python and Tkinter. It provides a graphical user interface (GUI) to launch other Python programs.

## Files in this directory

- `dashboard.py`: This is the main script for the Dashboard Application. It defines the GUI and the functions to launch other Python programs.

## How the code works

The `dashboard.py` script creates a Tkinter window with the title "Dashboard". It then creates three buttons: "Launch Database Program", "Launch Clockin Program", and "Launch Tracing Board Program". Each button is associated with a function that launches a specific Python program when the button is clicked.

The `launch_tracing_board_program` function uses the `Popen` function from the `subprocess` module to launch the `tracing-board.py` script. If an error occurs while launching the script, a message box is displayed with the error message.

The script enters the Tkinter event loop with `root.mainloop()`, which waits for events (like button clicks) and responds to them as defined in the script.

## How to run the application

1. Ensure you have Python installed on your machine.
2. Run the `dashboard.py` script in a Python environment.

```bash
python dashboard.py