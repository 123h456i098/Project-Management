from base_workings.player import Player
from base_workings.map_generation_using_kruskals_alg import MapBoard


class Controller:
    def __init__(self, view, w, h):
        self.view = view
        h += 1 if h % 2 == 0 else 0
        w += 1 if w % 2 == 0 else 0
        self.board = MapBoard(w, h)
        self.player = Player(*self.board.start, self.board.nodes, w, h)
        self.view.set_controllers_action_function(self.action)

    def action(self, action):
        if action == "up":
            self.move_player("N")
        elif action == "down":
            self.move_player("S")
        elif action == "left":
            self.move_player("W")
        elif action == "right":
            self.move_player("E")

    def start(self):
        for row in self.board.nodes:
            for each in row:
                self.view.add_tile_to_grid(each.tile_type, each.x, each.y)
        self.view.add_tile_to_grid("P", *self.player.pos)
        self.view.stats.addAction("N", lambda: self.move_player("N"))
        self.view.stats.addAction("E", lambda: self.move_player("E"))
        self.view.stats.addAction("S", lambda: self.move_player("S"))
        self.view.stats.addAction("W", lambda: self.move_player("W"))

    def move_player(self, direction: str):
        old_pos = self.player.move(direction)
        self.view.remove_player_from_grid(*old_pos)
        self.view.add_tile_to_grid("P", *self.player.pos)
