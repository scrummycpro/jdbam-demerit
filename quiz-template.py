import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
import pytz
import random

class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz App")
        self.geometry("400x350")

        self.current_question = 0
        self.questions = [
            {"question": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "4"},
            {"question": "What is the capital of France?", "options": ["London", "Berlin", "Paris", "Rome"], "answer": "Paris"},
            {"question": "What is the largest planet in our solar system?", "options": ["Jupiter", "Saturn", "Mars", "Venus"], "answer": "Jupiter"},
            {"question": "What is the chemical symbol for water?", "options": ["H2O", "CO2", "O2", "NaCl"], "answer": "H2O"},
            {"question": "Who painted the Mona Lisa?", "options": ["Michelangelo", "Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso"], "answer": "Leonardo da Vinci"}
        ]

        random.shuffle(self.questions)  # Shuffle the questions

        self.grade = 0
        self.duration = 0

        self.label_question = ttk.Label(self, text="")
        self.label_question.pack(pady=10)

        self.option_var = tk.StringVar()
        self.radio_buttons = []
        for i in range(4):
            radio_button = ttk.Radiobutton(self, text="", variable=self.option_var, value=i)
            radio_button.pack()
            self.radio_buttons.append(radio_button)

        self.label_person = ttk.Label(self, text="Select Person:")
        self.label_person.pack(pady=5)
        self.person_var = tk.StringVar()
        self.person_dropdown = ttk.Combobox(self, textvariable=self.person_var, values=["Zara", "Jasmin", "Aria"], state="readonly")
        self.person_dropdown.pack()

        self.button_next = ttk.Button(self, text="Next", command=self.next_question)
        self.button_next.pack(pady=10)

        self.label_timer = ttk.Label(self, text="")
        self.label_timer.pack(pady=5)

        self.conn = sqlite3.connect('quiz_results.db')
        self.create_table()

        self.start_timer()

        self.display_question()

    def create_table(self):
        try:
            c = self.conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS quiz_results
                         (id INTEGER PRIMARY KEY,
                         grade INTEGER,
                         person TEXT,
                         duration INTEGER,
                         date_added TEXT)''')
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error creating table:", e)

    def start_timer(self):
        self.start_time = datetime.now()

        def update_timer():
            current_time = datetime.now()
            elapsed_time = current_time - self.start_time
            self.label_timer.config(text=str(elapsed_time))
            self.after(1000, update_timer)

        update_timer()

    def next_question(self):
        selected_option = self.option_var.get()
        if selected_option != "":
            question_data = self.questions[self.current_question]
            selected_answer = question_data["options"][int(selected_option)]
            correct_answer = question_data["answer"]
            if selected_answer == correct_answer:
                self.grade += 20  # Each correct answer adds 20 points
                messagebox.showinfo("Correct", "Correct!")
            else:
                messagebox.showinfo("Incorrect", f"Incorrect. Correct answer: {correct_answer}")
            self.current_question += 1
            self.display_question()
        else:
            messagebox.showinfo("Error", "Please select an option")

    def display_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.label_question.config(text=question_data["question"])
            options = question_data["options"]
            self.option_var.set("")  # Clear selection
            for i in range(4):
                self.radio_buttons[i].config(text=options[i])
        else:
            self.button_next.config(state=tk.DISABLED)
            self.save_results()

    def save_results(self):
        self.duration = (datetime.now() - self.start_time).total_seconds()

        # Convert current time to PST
        pacific_tz = pytz.timezone('America/Los_Angeles')
        current_time = datetime.now(pacific_tz)
        date_added = current_time.strftime("%Y-%m-%d %H:%M:%S")
        person = self.person_var.get()

        c = self.conn.cursor()
        c.execute("INSERT INTO quiz_results (grade, person, duration, date_added) VALUES (?, ?, ?, ?)",
                  (self.grade, person, self.duration, date_added))
        self.conn.commit()
        self.conn.close()

        messagebox.showinfo("Quiz Finished", f"Your grade: {self.grade}")
        self.destroy()  # Close the quiz window

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
