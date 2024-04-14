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
        self.total_questions = 5
        self.start_time = None
        self.answer_given_time = None

        self.create_widgets()

    def create_widgets(self):
        self.question_label = ttk.Label(self.root, text="", font=("Arial", 16))
        self.question_label.pack(pady=10)

        self.answer_entry = ttk.Entry(self.root, width=20, font=("Arial", 16))
        self.answer_entry.pack(pady=5)

        self.submit_button = ttk.Button(self.root, text="Submit Answer", command=self.submit_answer, width=30)
        self.submit_button.pack(pady=5)

        self.timer_label = ttk.Label(self.root, text="", font=("Arial", 14))
        self.timer_label.pack(pady=5)

        self.person_label = ttk.Label(self.root, text="Select Person:", font=("Arial", 14))
        self.person_label.pack(pady=5)

        self.person_var = tk.StringVar()
        self.person_combobox = ttk.Combobox(self.root, textvariable=self.person_var, values=["Zara", "Jasmin", "Aria"], font=("Arial", 14))
        self.person_combobox.pack(pady=5)

        self.load_questions()

    def load_questions(self):
        for _ in range(self.total_questions):
            operand1 = random.randint(10, 99)
            operand2 = random.randint(10, 99)
            question = f"What is {operand1} + {operand2}?"
            correct_answer = operand1 + operand2
            self.questions.append((question, correct_answer))
        self.show_question()

    def show_question(self):
        self.question_label.config(text=self.questions[self.current_question_index][0])
        self.answer_entry.delete(0, tk.END)
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        self.timer_label.config(text=f"Time: {elapsed_time:.1f} seconds")
        self.root.after(100, self.update_timer)

    def submit_answer(self):
        answer = self.answer_entry.get().strip()
        correct_answer = str(self.questions[self.current_question_index][1])
        if answer == correct_answer:
            self.correct_answers += 1
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showerror("Result", f"Incorrect! The correct answer is {correct_answer}")
        self.next_question()

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
            cursor.execute("CREATE TABLE IF NOT EXISTS QuizResults (CompletionTime TIMESTAMP, Duration REAL, Grade REAL, Person TEXT)")
            completion_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            cursor.execute("INSERT INTO QuizResults (CompletionTime, Duration, Grade, Person) VALUES (?, ?, ?, ?)", (completion_time, duration, grade, person))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error saving to database: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuiz(root)
    root.mainloop()
