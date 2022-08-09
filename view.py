from PySide6 import QtWidgets as qw, QtCore as qc
from sys import exit
from controller import Controller


class View(qw.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dungeon Explorer")
        self.setCentralWidget(qw.QWidget())
        self.grid = qw.QGridLayout()
        self.centralWidget().setLayout(self.grid)
        self.centralWidget().setStyleSheet("QLabel {}")

        self.stats = qw.QToolBar()
        self.addToolBar(qc.Qt.BottomToolBarArea, self.stats)

    def add_tile_to_grid(self, label: str, x: int, y: int):
        tile = qw.QLabel(label)
        self.grid.addWidget(tile, y, x)

    def remove_player_from_grid(self, x: int, y: int):
        tile = self.grid.itemAtPosition(y, x)
        text = tile.widget().text()
        self.grid.removeItem(tile)
        player = self.grid.itemAtPosition(y, x)
        player.widget().deleteLater()
        self.add_tile_to_grid(text, x, y)


def main():
    app = qw.QApplication([])
    win = View()
    control = Controller(win)
    control.start()
    win.show()
    exit(app.exec())


if __name__ == "__main__":
    main()
