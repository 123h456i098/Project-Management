from PySide6 import QtWidgets as qw
from sys import exit


class FightView(qw.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fight")
        self.setCentralWidget(qw.QWidget())
        self.centralWidget().setStyleSheet(
            """
background-image: url(Images/img.jpg);
background-attachment: fixed
"""
        )


def main():
    app = qw.QApplication([])
    print(app.styleSheet())
    win = FightView()
    win.show()
    exit(app.exec())


if __name__ == "__main__":
    main()
