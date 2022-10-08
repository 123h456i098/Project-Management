import json
from PySide6 import QtWidgets as qw, QtCore as qc
import random

level_questions = ["australia", "england", "japan", "new_zealand"]


class Ask_Question:
    def __init__(
        self, level, back_to_main_screen=None, correct=None, wrong=None
    ):
        self.correct = correct
        self.wrong = wrong
        self.back_to_main_screen = back_to_main_screen
        file_name = f"questions/{level_questions[level-1]}_questions.json"
        with open(file_name, "r") as read_file:
            self.questions = json.load(read_file)
        print(self.questions)

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
        self.question.setWordWrap(True)
        self.question.setFixedWidth(350)
        # self.question.setFixedHeight(40)
        self.vbox2.addWidget(self.question, 0, qc.Qt.AlignCenter)
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
