import tkinter as tk
from tkinter import ttk, messagebox
import random
import sqlite3
import time

class MathQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")

        self.questions = []
        self.current_question_index = 0
        self.correct_answers = 0
        self.total_questions = 20
        self.start_time = None

        self.create_widgets()

    def create_widgets(self):
        self.question_label = ttk.Label(self.root, text="")
        self.question_label.pack(pady=10)

        self.answer_entry = ttk.Entry(self.root, width=10)
        self.answer_entry.pack(pady=5)

        self.submit_button = ttk.Button(self.root, text="Submit Answer", command=self.submit_answer)
        self.submit_button.pack(pady=5)

        self.next_button = ttk.Button(self.root, text="Next Question", command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(pady=5)

        self.select_label = ttk.Label(self.root, text="Select Person:")
        self.select_label.pack(pady=5)

        self.person_var = tk.StringVar()
        self.person_combobox = ttk.Combobox(self.root, textvariable=self.person_var, values=["Zara", "Jasmin", "Aria"])
        self.person_combobox.pack(pady=5)

        self.load_questions()

    def load_questions(self):
        for _ in range(self.total_questions):
            operand1 = random.randint(10, 99)
            operand2 = random.randint(10, 99)
            operator = random.choice(["+", "-", "*", "/"])
            question = f"What is {operand1} {operator} {operand2}?"
            self.questions.append((question, self.calculate_answer(operand1, operand2, operator)))
        self.show_question()

    def calculate_answer(self, operand1, operand2, operator):
        if operator == "+":
            return operand1 + operand2
        elif operator == "-":
            return operand1 - operand2
        elif operator == "*":
            return operand1 * operand2
        elif operator == "/":
            return operand1 // operand2  # Integer division for simplicity

    def show_question(self):
        self.question_label.config(text=self.questions[self.current_question_index][0])
        self.answer_entry.delete(0, tk.END)
        self.submit_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)
        self.start_time = time.time()

    def submit_answer(self):
        answer = self.answer_entry.get().strip()
        correct_answer = str(self.questions[self.current_question_index][1])
        if answer == correct_answer:
            messagebox.showinfo("Result", "Correct!")
            self.correct_answers += 1
        else:
            messagebox.showerror("Result", f"Incorrect! The correct answer is {correct_answer}")
        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index < self.total_questions:
            self.show_question()
        else:
            self.finish_quiz()

    def finish_quiz(self):
        duration = time.time() - self.start_time
        grade = self.correct_answers / self.total_questions * 100
        person = self.person_var.get()
        self.save_to_database(duration, grade, person)
        messagebox.showinfo("Quiz Finished", f"Quiz completed!\nDuration: {duration:.2f} seconds\nGrade: {grade:.2f}%")
        self.root.destroy()

    def save_to_database(self, duration, grade, person):
        try:
            conn = sqlite3.connect("quiz_results.db")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS QuizResults (Duration REAL, Grade REAL, Person TEXT)")
            cursor.execute("INSERT INTO QuizResults (Duration, Grade, Person) VALUES (?, ?, ?)", (duration, grade, person))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error saving to database: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuiz(root)
    root.mainloop()
