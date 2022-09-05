from PySide6 import QtWidgets as qw, QtCore as qc
from sys import exit
from controller import Controller


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
        self.toolbar_labels = []
        self.stats.setStyleSheet(
            """
QToolButton {
border: 2px outset red;
margin: 2px;
}"""
        )

        self.controllers_action_function = None

    def set_controllers_action_function(self, function):
        self.controllers_action_function = function

    def add_label_to_toolbar(self, text):
        label = qw.QLabel(text)
        self.toolbar_labels.append(label)
        self.stats.addWidget(label)

    def remove_label_from_toolbar(self, label):
        label.deleteLater()

    def keyPressEvent(self, event):
        match event.key():
            case qc.Qt.Key_Up | qc.Qt.Key_W:
                self.controllers_action_function("up")
            case qc.Qt.Key_Down | qc.Qt.Key_S:
                self.controllers_action_function("down")
            case qc.Qt.Key_Left | qc.Qt.Key_A:
                self.controllers_action_function("left")
            case qc.Qt.Key_Right | qc.Qt.Key_D:
                self.controllers_action_function("right")

    def add_tile_to_grid(self, label: str, x: int, y: int):
        tile = qw.QLabel(label)
        self.grid.addWidget(tile, y, x)

    def remove_tile_from_grid(self, x: int, y: int):
        tile = self.grid.itemAtPosition(y, x)
        tile.widget().setParent(None)

    def remove_player_from_grid(self, x: int, y: int):
        text = self.grid.itemAtPosition(y, x).widget().text()
        self.remove_tile_from_grid(x, y)
        self.remove_tile_from_grid(x, y)
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
