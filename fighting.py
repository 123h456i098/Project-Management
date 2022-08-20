from PySide6 import QtWidgets as qw
from sys import exit
import json
from random import shuffle


class FightView(qw.QMainWindow):
    def __init__(self, player, parent_view):
        super().__init__()
        self.parent_view = parent_view
        self.health = player.level * 2
        self.exp_to_get = player.level * 2
        self.num_dice = 0
        self.setWindowTitle(f"Fight - level {player.level}")
        self.p_health = player.stamina
        self.p_max_health = player.max_stamina
        self.setCentralWidget(qw.QWidget())
        self.centralWidget().setObjectName("main_body")
        self.setStyleSheet(
            """
#main_body {
background-image: url(Images/img.jpg);
background-attachment: fixed
}

QLabel {
color: white;
}
"""
        )
        self.vbox = qw.QVBoxLayout()
        self.centralWidget().setLayout(self.vbox)
        self.add_info_to_screen()

    def add_info_to_screen(self):
        self.monster_health_bar = qw.QLabel(
            f"{self.health}/{self.exp_to_get}\n"
            "Roll a 5 or higher to deal damage."
        )
        self.get_dice = qw.QPushButton("Get Dice")
        self.get_dice.clicked.connect(self.ask_question)
        self.roll = qw.QPushButton(f"Roll {self.num_dice}")
        self.roll.clicked.connect(self.damage_roll)
        self.p_health_bar = qw.QLabel(
            f"{self.p_health}/{self.p_max_health} - {self.num_dice} x 🎲"
        )
        self.vbox.addWidget(self.monster_health_bar)
        self.vbox.addWidget(self.get_dice)
        self.vbox.addWidget(self.roll)
        self.vbox.addWidget(self.p_health_bar)

    def damage_roll(self):
        self.win()

    def ask_question(self):
        # with open("questions/england_questions.json", "r") as read_file:
        #     questions = json.load(read_file)
        # shuffle(questions)
        # self.question = qw.QLabel()
        self.num_dice += 1
        self.roll.setText(f"Roll {self.num_dice}")
        self.p_health_bar.setText(
            f"{self.p_health}/{self.p_max_health} - {self.num_dice} x 🎲"
        )

    def win(self):
        self.parent_view.show()
        self.close()
