import json
from PySide6 import QtWidgets as qw
import random


class Ask_Question:
    def __init__(self, back_to_main_screen, correct, wrong):
        self.correct = correct
        self.wrong = wrong
        self.back_to_main_screen = back_to_main_screen
        with open("questions/england_questions.json", "r") as read_file:
            self.questions = json.load(read_file)

    def get_answer(self):
        question = random.choice(self.questions)
        text = question["question"]
        correct = question["correct"]
        return text, correct

    def ask_question(self):
        self.vbox2 = qw.QVBoxLayout()
        self.question_view = qw.QWidget()
        self.question_view.setLayout(self.vbox2)
        question = random.choice(self.questions)
        text = question["question"]
        correct = question["correct"]
        wrongs = [question["wrong1"], question["wrong2"], question["wrong3"]]
        answers = wrongs + [correct]
        self.question = qw.QLabel(text)
        self.vbox2.addWidget(self.question)
        self.vbox2.addStretch()
        random.shuffle(answers)
        self.buttons = []
        for i, each in enumerate(answers):
            button = qw.QPushButton(each)
            self.vbox2.addWidget(button)
            self.buttons.append(button)
            button.clicked.connect(
                lambda _=None, i=i, each=each: self.answer_question(
                    i, each, correct
                )
            )

    def answer_question(self, index, answer, correct):
        style = f"""
QPushButton {{
background-color: {"green" if answer == correct else "red"};
color: black
}}"""
        for each in self.buttons:
            each.setEnabled(False)
        self.buttons[index].setStyleSheet(style)

        if answer == correct:
            self.correct()
        else:
            self.wrong()
        submit_button = qw.QPushButton("Cool, got it")
        self.vbox2.addWidget(submit_button)
        submit_button.clicked.connect(self.back_to_main_screen)
