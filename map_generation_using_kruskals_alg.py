import pygame
import random


class MapBoard:
    def __init__(self, w: int, h: int):
        # Initialize a board, where - is a wall and X is a platform
        self.board = []
        row = []
        for _ in range(w // 2):
            row.extend(["-", "x"])
        row.append("-")
        for _ in range(h // 2):
            self.board.extend([["-" for _ in row], row])
        self.board.append(["-" for _ in row])

    def display(self):
        for row in self.board:
            print(*row)


board = MapBoard(10, 10)
board.display()
