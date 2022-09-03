from PySide6 import QtWidgets as qw, QtCore as qc
from sys import exit
import random
from ask_question import Ask_Question


class FightView(qw.QMainWindow):
    def __init__(self, player, end_function):
        super().__init__()
        self.question_machine = Ask_Question(
            self.back_to_main_screen, self.get_question_right, self.take_damage
        )
        self.end_function = end_function
        self.health = player.level * 2
        self.exp_to_get = player.level * 2
        self.num_dice = 0
        self.setWindowTitle(f"Fight - level {player.level}")
        self.setFixedSize(400, 300)
        self.p_health = player.stamina
        self.p_max_health = player.max_stamina
        self.setCentralWidget(qw.QWidget())
        self.centralWidget().setObjectName("main_body")
        self.setStyleSheet(
            """
#main_body {
border-image: url("Images/img.jpg");
background-repeat: no-repeat;
background-position: center;
}

QLabel {
color: white;
}
"""
        )
        self.stacked = qw.QStackedLayout()
        self.fight_view = qw.QWidget()
        self.vbox1 = qw.QVBoxLayout()
        self.centralWidget().setLayout(self.stacked)
        self.fight_view.setLayout(self.vbox1)
        self.stacked.addWidget(self.fight_view)
        self.stacked.setCurrentIndex(0)
        self.add_info_to_screen()

    def add_info_to_screen(self):
        self.monster_health_bar = qw.QLabel(
            f"Monster: {self.health}/{self.exp_to_get}"
            "    (Roll a 5 or higher to deal damage)"
        )
        self.get_dice = qw.QPushButton("Get Dice")
        self.get_dice.clicked.connect(self.ask_question)
        self.roll = qw.QPushButton(f"Roll {self.num_dice}")
        self.roll.clicked.connect(self.damage_roll)
        self.p_health_bar = qw.QLabel(
            f"You: {self.p_health}/{self.p_max_health} - {self.num_dice} x 🎲"
        )
        self.vbox1.addWidget(self.monster_health_bar)
        self.vbox1.addStretch()
        self.vbox1.addWidget(self.get_dice)
        self.vbox1.addWidget(self.roll)
        self.vbox1.addStretch()
        self.vbox1.addWidget(self.p_health_bar)

    def damage_roll(self):
        if self.num_dice > 0:
            rolls = [random.randint(1, 6) for _ in range(self.num_dice)]
            text = f"[{', '.join(map(str, rolls))}] - Roll {self.num_dice}"
            if max(rolls) >= 5:
                self.do_damage()
            else:
                self.take_damage()
        else:
            text = "Get a goddamnned dice!"
        self.roll.setText(text)

    def do_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.end_function(self.p_health, self.exp_to_get)
        self.monster_health_bar.setText(
            f"Monster: {self.health}/{self.exp_to_get}"
            "    (Roll a 5 or higher to deal damage)"
        )

    def ask_question(self):
        self.question_machine.ask_question()
        self.stacked.addWidget(self.question_machine.question_view)
        self.stacked.setCurrentIndex(1)

    def back_to_main_screen(self):
        self.stacked.setCurrentIndex(0)
        self.stacked.removeWidget(self.question_machine.question_view)

    def get_question_right(self):
        self.num_dice += 1
        self.roll.setText(f"Roll {self.num_dice}")
        self.p_health_bar.setText(
            f"{self.p_health}/{self.p_max_health} - {self.num_dice} x 🎲"
        )

    def take_damage(self):
        self.p_health -= 1
        if self.p_health <= 0:
            self.end_function(self.p_health, 0)
        self.p_health_bar.setText(
            f"{self.p_health}/{self.p_max_health} - {self.num_dice} x 🎲"
        )
