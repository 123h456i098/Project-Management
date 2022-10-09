from random import randint
from PySide6 import QtWidgets as qw, QtCore as qc
from main_files.ask_question import Ask_Question


class Shop(qw.QMainWindow):
    def __init__(self, end_function, coins, level):
        super().__init__()
        self.p_coins = coins
        self.end_function = end_function
        self.health_to_get = 0
        self.exp_to_get = 0
        self.stock = []
        self.setWindowTitle("Shop")
        self.setFixedSize(400, 300)
        self.setCentralWidget(qw.QWidget())
        self.centralWidget().setObjectName("main_body")
        self.setStyleSheet(
            """
#main_body {
border-image: url("Images/backgrounds/shop.png");
background-repeat: no-repeat;
background-position: center;
}

QLabel {
color: black;
}
"""
        )
        self.vbox = qw.QVBoxLayout()
        self.centralWidget().setLayout(self.vbox)
        self.exit_button = qw.QPushButton(f"Back   (you have ${self.p_coins})")
        self.exit_button.clicked.connect(
            lambda: self.end_function(
                self.p_coins, self.exp_to_get, self.health_to_get
            )
        )
        self.vbox.addWidget(self.exit_button)
        self.hbox = qw.QHBoxLayout()
        self.vbox.addLayout(self.hbox)
        # 3 rewards, answer, exp, health
        self.tags = ["An answer", "Some EXP", "Some stamina"]
        self.prices = [randint(2, 4) for _ in range(3)]
        self.products = [
            Ask_Question(level).get_answer(),
            randint(1, 3),
            randint(3, 5),
        ]
        self.buttons = []
        for index, tag in enumerate(self.tags):
            widget = qw.QWidget()
            widget.setObjectName("item-area")
            widget.setStyleSheet(
                """
#item-area {
border: 2px solid black;
background-color: rgba(255, 255, 255, 150);
}
"""
            )
            vbox = qw.QVBoxLayout()
            widget.setLayout(vbox)
            title = qw.QLabel(f"{tag}\n")
            vbox.addWidget(title, 1, qc.Qt.AlignCenter)
            button = qw.QPushButton(f"${self.prices[index]}")
            self.buttons.append(button)
            vbox.addWidget(button)
            button.clicked.connect(lambda sac=None, i=index: self.buy(i))
            self.hbox.addWidget(widget)
            self.stock.append(widget)

            # Some labels and a button that buys the item, clears it from shop
            # and displays in a message box to user

    def buy(self, index):
        price = self.prices[index]
        if self.p_coins >= price:
            self.p_coins -= self.prices.pop(index)
            self.exit_button.setText(f"Back   (you have ${self.p_coins})")
            tag = self.tags.pop(index)
            if tag == "An answer":
                text = (
                    f"Q: {self.products[index][0]}\n"
                    f"A: {self.products[index][1]}"
                )
            else:
                text = f"You get: +{self.products[index]} {tag.split(' ')[1]}"
            qw.QMessageBox(
                qw.QMessageBox.Icon.Information, f"Bought {tag}", text
            ).exec()
            if tag == "Some EXP":
                self.exp_to_get = self.products[index]
            elif tag == "Some health":
                self.health_to_get = self.products[index]
            del self.products[index]

            del self.buttons[index]

            widget = self.stock.pop(index)
            widget.setParent(None)
        for i in range(len(self.buttons)):
            self.buttons[i].clicked.disconnect()
            self.buttons[i].clicked.connect(lambda sac=None, i=i: self.buy(i))
