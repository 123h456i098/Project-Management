import pygame
import random


class Node:
    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.parent_node = None

    def find_root(self):
        parent = self
        while parent.parent_node is not None:
            parent = parent.parent_node
        return parent


class MapBoard:
    def __init__(self, w: int, h: int):
        # Initialize a board, where - is a wall and x is a tile
        self.nodes = []
        self.edges = []
        tile = True
        for y in range(h + 1 if h % 2 == 0 else h):
            self.nodes.append([])
            for x in range(w + 1 if w % 2 == 0 else w):
                if tile:
                    self.nodes[-1].append(
                        Node(x, y, ("x" if y % 2 == 0 else "-"))
                    )
                else:
                    self.nodes[-1].append(Node(x, y, "o"))
                    self.edges.append([x, y])

                tile = not tile

    def kruskals_alg(self):
        random.shuffle(self.edges)
        while len(self.edges) > 0:
            x, y = self.edges.pop()
            if x % 2 == 0:
                # Direction vertical
                tile1 = self.nodes[y + 1][x]
                tile2 = self.nodes[y - 1][x]
            else:
                # Direction horizontal
                tile1 = self.nodes[y][x + 1]
                tile2 = self.nodes[y][x - 1]
            if tile1.find_root() != tile2.find_root():
                tile1.find_root().parent_node = tile2
                self.nodes[y][x].tile_type = "x"

    def display(self):
        self.kruskals_alg()
        for row in self.nodes:
            print(*["⬜" if node.tile_type == "x" else "⬛" for node in row])


board = MapBoard(20, 20)
board.display()
