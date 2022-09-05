from main_files.ask_question import Ask_Question
from PySide6 import QtWidgets as qw
import random

# needs to change to an open chest with no function once reward is picked


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
                self.text = f"${self.gold}"
            case "health":
                self.health = random.randint(1, 3)
                self.text = f"+{self.health}"
            case "hurt":
                hurt = random.randint(1, 3)
                self.health = hurt * -1
                self.text = f"-{hurt}"

    def add_widgets(self):
        vbox = qw.QVBoxLayout()
        vbox.addWidget(qw.QLabel(self.text))
        accept = qw.QPushButton("Collect")
        accept.clicked.connect(lambda: self.end_func(self.gold, self.health))
        vbox.addWidget(accept)
        self.centralWidget().setLayout(vbox)
