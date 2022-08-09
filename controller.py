from player import Player
import model


class Controller:
    def __init__(self, view):
        self.view = view

    def start(self):
        for row in model.board.nodes:
            for each in row:
                self.view.add_tile_to_grid(each.tile_type, each.x, each.y)
        self.player = Player(*model.board.start)
        self.view.add_tile_to_grid("P", *self.player.pos)
        self.view.stats.addAction("N", lambda: self.move_player("N"))
        self.view.stats.addAction("E", lambda: self.move_player("E"))
        self.view.stats.addAction("S", lambda: self.move_player("S"))
        self.view.stats.addAction("W", lambda: self.move_player("W"))

    def move_player(self, direction: str):
        old_pos = self.player.move(direction, model.board.nodes)
        self.view.remove_player_from_grid(*old_pos)
        self.view.add_tile_to_grid("P", *self.player.pos)
