from main_files.ask_question import Ask_Question
from PySide6 import QtWidgets as qw, QtGui as qg
import random


class Chest(qw.QMainWindow):
    def __init__(self, end_function):
        super().__init__()
        self.question_machine = Ask_Question()
        self.end_func = end_function
        self.setWindowTitle("Chest")
        self.setFixedSize(400, 300)
        possible_rewards = ["answer", "gold", "health", "hurt"]
        self.reward = random.choice(possible_rewards)
        self.setCentralWidget(qw.QWidget())
        self.centralWidget().setObjectName("main_body")
        self.setStyleSheet(
            """
#main_body {
border-image: url("Images/backgrounds/chest1.png");
background-repeat: no-repeat;
background-position: center;
}

QLabel {
color: black;
}
"""
        )
        self.make_reward()
        self.add_widgets()

    def make_reward(self):
        self.gold = 0
        self.health = 0
        match self.reward:
            case "answer":
                question, answer = self.question_machine.get_answer()
                self.text = f"Q: {question}\nA: {answer}"
            case "gold":
                self.gold = random.randint(1, 3)
                self.text = f"+${self.gold} gold"
            case "health":
                self.health = random.randint(1, 3)
                self.text = f"+{self.health} stamina"
            case "hurt":
                hurt = random.randint(1, 3)
                self.health = hurt * -1
                self.text = f"-{hurt} stamina"

    def add_widgets(self):
        self.grid = qw.QGridLayout()
        self.accept = qw.QPushButton("Open chest")
        self.accept.clicked.connect(self.accept_reward)
        self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(2, 1)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(self.accept, 3, 1)
        self.centralWidget().setLayout(self.grid)

    def accept_reward(self):
        reward = qw.QLabel(self.text)
        reward.setFont(qg.QFont("Consolas", 24))
        self.grid.addWidget(reward, 1, 1)
        self.accept.text = "Collect"
        self.accept.clicked.connect(
            lambda: self.end_func(self.gold, self.health)
        )
