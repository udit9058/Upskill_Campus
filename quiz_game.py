import csv
import tkinter as tk
from tkinter import *

# Create the Tkinter root window
root = tk.Tk()
root.geometry("1000x1000")

background_image = PhotoImage(file="c.png")
background_label = Label(root, image=background_image)
background_label.place(x=0, y=100, relwidth=1, relheight=1)

class QuizInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")

        # Quiz data
        self.quiz_data = self.load_quiz_data("quiz_data.csv")

        self.current_question = 0
        self.score = 0

        self.question_label = tk.Label(root, text="", font=("Arial", 12))
        self.question_label.pack(pady=10)

        self.answer_options = []
        for i in range(4):
            option = tk.Button(root, text="", font=("Arial", 10), command=lambda idx=i: self.select_option(idx))
            option.pack(pady=5)
            self.answer_options.append(option)

        self.next_button = tk.Button(root, text="Next", font=("Arial", 12), state=tk.DISABLED, command=self.next_question)
        self.next_button.pack(pady=10)

        self.display_question()

    def load_quiz_data(self, filename):
        quiz_data = []
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                question = row["question"]
                options = [row[f"option{i}"] for i in range(1, 5)]
                answer = row["answer"]
                quiz_data.append({"question": question, "options": options, "answer": answer})
        return quiz_data

    def display_question(self):
        question_data = self.quiz_data[self.current_question]
        self.question_label.config(text=question_data["question"])

        options = question_data["options"]
        for i in range(4):
            self.answer_options[i].config(text=options[i], state="normal", relief=tk.RAISED)

    def select_option(self, option_index):
        question_data = self.quiz_data[self.current_question]
        correct_answer = question_data["answer"]

        selected_option = option_index

        for i in range(4):
            if i == selected_option:
                self.answer_options[i].config(relief=tk.SUNKEN)
            else:
                self.answer_options[i].config(relief=tk.RAISED)

        self.next_button.config(state=tk.NORMAL)

        if selected_option == question_data["options"].index(correct_answer):
            print("Correct answer!")
            self.score += 1
        else:
            print("Incorrect answer!")

    def next_question(self):
        self.current_question += 1

        if self.current_question < len(self.quiz_data):
            self.display_question()
            self.next_button.config(state=tk.DISABLED)
        else:
            self.display_score()
            print("Quiz completed!")

            # Disable answer options after quiz completion
            for i in range(4):
                self.answer_options[i].config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)

    def display_score(self):
        score_label = tk.Label(self.root, text=f"Final Score: {self.score}/{len(self.quiz_data)}", font=("Arial", 12))
        score_label.pack(pady=10)



# Create an instance of the QuizInterface class
quiz_interface = QuizInterface(root)

# Run the main event loop
root.mainloop()
