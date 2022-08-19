from PySide6 import QtWidgets as qw, QtCore as qc
from sys import exit
from controller import Controller
from fighting import FightView


class View(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dungeon Explorer")
        self.setCentralWidget(qw.QWidget())
        self.grid = qw.QGridLayout()
        self.centralWidget().setLayout(self.grid)
        self.centralWidget().setStyleSheet("QLabel {}")

        self.stats = qw.QToolBar()
        self.addToolBar(qc.Qt.LeftToolBarArea, self.stats)
        self.stats.setFixedWidth(70)

        self.controllers_action_function = None

    def set_controllers_action_function(self, function):
        self.controllers_action_function = function

    def open_fight_view(self, level):
        self.fight = FightView(level, self)
        self.fight.show()
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == qc.Qt.Key_Up:
            self.controllers_action_function("up")
        if event.key() == qc.Qt.Key_Down:
            self.controllers_action_function("down")
        if event.key() == qc.Qt.Key_Left:
            self.controllers_action_function("left")
        if event.key() == qc.Qt.Key_Right:
            self.controllers_action_function("right")

    def add_tile_to_grid(self, label: str, x: int, y: int):
        tile = qw.QLabel(label)
        self.grid.addWidget(tile, y, x)

    def remove_player_from_grid(self, x: int, y: int):
        tile = self.grid.itemAtPosition(y, x)
        text = tile.widget().text()
        tile.widget().setParent(None)
        player = self.grid.itemAtPosition(y, x)
        player.widget().setParent(None)
        self.add_tile_to_grid(text, x, y)


def main():
    app = qw.QApplication([])
    win = View()
    control = Controller(win, 20, 20)
    control.start()
    win.show()
    exit(app.exec())


if __name__ == "__main__":
    main()
