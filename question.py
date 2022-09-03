from ask_question import Ask_Question
from PySide6 import QtWidgets as qw


class Question(qw.QMainWindow):
    def __init__(self, end_function):
        super().__init__()
        self.question_machine = Ask_Question(
            self.back_to_main_screen, self.get_question_right, self.take_damage
        )
        self.end_function = end_function
        self.setWindowTitle("Question")
        self.setFixedSize(400, 300)
        self.question_machine.ask_question()
        self.setCentralWidget(self.question_machine.question_view)
        self.setStyleSheet(
            """
QMainWindow {
border-image: url("Images/img2.jpg");
background-repeat: no-repeat;
background-position: center;
}
QLabel {
color: white;
}
"""
        )

    def get_question_right(self):
        self.answer_status = True

    def take_damage(self):
        self.answer_status = False

    def back_to_main_screen(self):
        self.end_function(self.answer_status)
