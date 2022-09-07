from random import randint
from PySide6 import QtWidgets as qw
from main_files.ask_question import Ask_Question

# shop screen
# decide what rewards are available and for what prices?
# buttons to buy, make sure have enough money to buy,
# needs to save what has been bought and the current inventory so users can't
# continuously reroll
# if there is only one shop per round, can just hide and show the same screen
# but not sure what do do for more than one shop


class Shop(qw.QMainWindow):
    def __init__(self, end_function, coins):
        super().__init__()
        self.p_coins = coins
        self.end_function = end_function
        self.health_to_get = 0
        self.exp_to_get = 0
        self.setWindowTitle("Shop")
        self.setFixedSize(400, 300)
        self.setCentralWidget(qw.QWidget())
        self.vbox = qw.QVBoxLayout()
        self.centralWidget().setLayout(self.vbox)
        self.exit_button = qw.QPushButton("Back")
        self.exit_button.clicked.connect(
            lambda: self.end_function(
                self.p_coins, self.exp_to_get, self.health_to_get
            )
        )
        self.vbox.addWidget(self.exit_button)
        self.hbox = qw.QHBoxLayout()
        self.vbox.addLayout(self.hbox)
        # 3 rewards, answer, exp, health
        self.tags = ["An answer", "Some EXP", "Some health"]
        self.prices = [randint(2, 4) for _ in range(3)]
        self.products = [
            Ask_Question().get_answer(),
            randint(1, 3),
            randint(3, 5),
        ]
        for index, tag in enumerate(self.tags):
            widget = qw.QWidget()
            widget.setObjectName("item-area")
            widget.setStyleSheet(
                """
#item-area {
border: 2px solid black;
}
"""
            )
            vbox = qw.QVBoxLayout()
            widget.setLayout(vbox)
            title = qw.QLabel(f"{tag}\n")
            vbox.addWidget(title)
            button = qw.QPushButton(f"${self.prices[index]}")
            vbox.addWidget(button)
            button.clicked.connect(lambda sac=None, i=index: self.buy(i))
            self.hbox.addWidget(widget)

            # Some labels and a button that buys the item, clears it from shop
            # and displays in a message box to user

    def buy(self, index):
        price = self.prices[index]
        if self.p_coins >= price:
            self.p_coins -= price
            qw.QMessageBox(
                qw.QMessageBox.Icon.Information,
                f"Bought {self.tags[index]}",
                f"{self.products[index]}",
            ).exec()
            if self.tags[index] == "Some EXP":
                self.exp_to_get = self.products[index]
            elif self.tags[index] == "Some health":
                self.health_to_get = self.products[index]
            # self.exit_button.clicked.connect(
            #     lambda: self.end_function(
            #         self.p_coins, self.exp_to_get, self.health_to_get
            #     )
            # )
        else:
            print("not enough money")
