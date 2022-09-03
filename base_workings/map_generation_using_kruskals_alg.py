import random
from typing import List
from base_workings.tiles import tiles, icons


class Node:
    def __init__(self, x: int, y: int, tile_type: str):
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.parent_node = None
        self.tile = tiles["plain"]

    def find_root(self):  # why -> Node: not defined?
        parent = self
        while parent.parent_node is not None:
            parent = parent.parent_node
        return parent


class MapBoard:
    def __init__(self, w: int, h: int):
        # Initialize a board, where - is a wall and x is a tile
        self.w = w
        self.h = h
        self.nodes = []
        self.edges = []
        self.create_board(w, h)
        self.kruskals_alg()
        self.add_tiles()
        self.display()

    def create_board(self, w, h):
        tile = True
        for y in range(h):
            self.nodes.append([])
            for x in range(w):
                if tile:
                    self.nodes[-1].append(
                        Node(x, y, ("plain" if y % 2 == 0 else "wall"))
                    )
                else:
                    self.nodes[-1].append(Node(x, y, "wall"))
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
                self.nodes[y][x].tile_type = "plain"

    def create_tiles(self) -> List[str]:
        tiles = [
            "start",
            "finish",
            *["monster" for _ in range(random.randint(6, 9))],
            *["shop" for _ in range(random.randint(1, 2))],
            *["chest" for _ in range(random.randint(3, 5))],
            *["trap" for _ in range(20)],
            *["question" for _ in range(random.randint(2, 3))],
        ]
        random.shuffle(tiles)
        return tiles

    def add_tiles(self):  # There has to be a better way to do this
        for tile_type in self.create_tiles():
            tile = ""
            while tile != "plain":
                tile = self.nodes[(y := random.randint(0, self.h - 1))][
                    (x := random.randint(0, self.w - 1))
                ].tile_type
            self.nodes[y][x].tile_type = tile_type

    def display(self):  # There has to be a better way to do this
        for y, row in enumerate(self.nodes):
            for x, each in enumerate(row):
                each.tile = tiles[each.tile_type]
                if each.tile_type == "start":
                    self.start = (x, y)
                self.nodes[y][x].tile_type = icons[
                    each.tile_type if each.tile_type != "trap" else "plain"
                ]
