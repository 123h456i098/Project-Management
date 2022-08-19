from PySide6 import QtWidgets as qw
from sys import exit


class FightView(qw.QMainWindow):
    def __init__(self, level, parent_view):
        super().__init__()
        self.parent_view = parent_view
        self.exp_to_get = level * 2
        self.setWindowTitle(f"Fight - level {level}")
        self.setCentralWidget(qw.QPushButton("push to win"))
        self.centralWidget().setStyleSheet(
            """
background-image: url(Images/img.jpg);
background-attachment: fixed
"""
        )
        self.centralWidget().clicked.connect(self.win)

    def win(self):
        self.parent_view.show()
        self.close()


def main():
    app = qw.QApplication([])
    print(app.styleSheet())
    win = FightView()
    win.show()
    exit(app.exec())


if __name__ == "__main__":
    main()
