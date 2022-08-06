from PySide6 import QtWidgets as qw
from map_generation_using_kruskals_alg import MapBoard
from sys import exit


class View(qw.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dungeon Explorer")
        self.setCentralWidget(qw.QWidget())
        self.vbox = qw.QVBoxLayout()
        self.centralWidget().setLayout(self.vbox)

        self.stats = qw.QHBoxLayout()
        self.vbox.addLayout(self.stats)
        self.stats.addWidget(qw.QLabel("stats"))

        self.grid = qw.QGridLayout()
        self.vbox.addLayout(self.grid)
        board = MapBoard(20, 20)
        for row in board.nodes:
            for each in row:
                tile = qw.QLabel(each.tile_type)
                self.grid.addWidget(tile, each.y, each.x)


def main():
    app = qw.QApplication([])
    win = View()
    win.show()
    exit(app.exec())


if __name__ == "__main__":
    main()
