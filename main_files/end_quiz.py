from PySide6 import QtWidgets as qw
from main_files.ask_question import Ask_Question


class Quiz(qw.QMainWindow):
    def __init__(self, player, end_function, level):
        super().__init__()
        self.question_machine = Ask_Question(
            level,
            self.next_question,
            self.correct,
            self.take_damage,
        )
        self.end_function = end_function
        self.player = player
        self.setWindowTitle(f"Level {level} - Quiz")
        self.setFixedSize(400, 300)
        self.setCentralWidget(qw.QWidget())
        self.centralWidget().setObjectName("main_body")
        self.setStyleSheet(
            f"""
#main_body {{
border-image: url("Images/backgrounds/monster5.png");
background-repeat: no-repeat;
background-position: center;
}}

QLabel {{
color: white;
}}
"""
        )
        self.vbox = qw.QVBoxLayout()
        self.centralWidget().setLayout(self.vbox)
        self.question_num = 1
        (
            self.texts,
            self.corrects,
            self.answers,
        ) = self.question_machine.ask_quiz()
        self.display_question()

    def display_question(self):
        self.progress = qw.QLabel(f"Quiz progress: {self.question_num}/10")
        self.p_stamina = qw.QLabel(
            f"Your stamina: {self.player.stamina}/{self.player.max_stamina}"
        )
        self.question_machine.display_question(
            self.texts[self.question_num - 1],
            self.corrects[self.question_num - 1],
            self.answers[self.question_num - 1],
        )
        self.vbox.addWidget(self.progress)
        self.vbox.addWidget(self.question_machine.question_view)
        self.vbox.addWidget(self.p_stamina)

    def clear_layout(self):
        while self.vbox.count():
            child = self.vbox.takeAt(0)
            child.widget().deleteLater()

    def next_question(self):
        if self.question_num >= 11:
            self.end_function(True)
        else:
            self.clear_layout()
            self.display_question()

    def take_damage(self):
        self.player.stamina -= 1
        if self.player.stamina <= 0:
            self.end_function(False)

    def correct(self):
        self.question_num += 1
