from map_generation_using_kruskals_alg import MapBoard


class Controller:
    def __init__(self, view):
        self.view = view

    def start(self):
        board = MapBoard(20, 20)
        for row in board.nodes:
            for each in row:
                self.view.add_tile_to_grid(each.tile_type, each.x, each.y)
