import random
from main_files.ask_question import Ask_Question
from PySide6 import QtWidgets as qw


class Question(qw.QMainWindow):
    def __init__(self, end_function: callable, level: int):
        super().__init__()
        self.question_machine = Ask_Question(
            level,
            self.back_to_main_screen,
            self.get_question_right,
            self.take_damage,
        )
        self.end_function = end_function
        self.setWindowTitle("Question")
        self.setFixedSize(400, 300)
        self.question_machine.ask_question()
        self.setCentralWidget(self.question_machine.question_view)
        self.setStyleSheet(
            f"""
QMainWindow {{
border-image: url("Images/backgrounds/question{random.randint(1, 2)}.png");
background-repeat: no-repeat;
background-position: center;
}}
QLabel {{
color: white;
}}
"""
        )

    def get_question_right(self) -> None:
        self.answer_status = True

    def take_damage(self) -> None:
        self.answer_status = False

    def back_to_main_screen(self) -> None:
        self.end_function(self.answer_status)
