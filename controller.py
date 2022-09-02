from base_workings.player import Player
from base_workings.map_generation_using_kruskals_alg import MapBoard, Node
from fighting import FightView
from base_workings.tiles import icons


class Controller:
    def __init__(self, view, w, h):
        self.view = view
        h += 1 if h % 2 == 0 else 0
        w += 1 if w % 2 == 0 else 0
        self.board = MapBoard(w, h)
        self.player = Player(*self.board.start, self.board.nodes, w, h)
        self.view.set_controllers_action_function(self.action)
        self.actions = {
            "Fight": self.open_fight_view,
            "Shop": lambda: print("shop"),
            "Chest": lambda: print("chest"),
            "Trap": lambda: print("trap"),
            "Question": lambda: print("question"),
            "Finish": lambda: print("finish"),
        }

    def open_fight_view(self):
        self.fight = FightView(self.player, self._done_fighting)
        self.fight.show()
        self.view.hide()

    def _done_fighting(self, alive, exp_to_get):
        if alive:
            self.player.gain_exp(exp_to_get)
            self.fight.close()
            self.view.show()
        else:
            print("you died")
            self.view.close()

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
        self.view.stats.addAction("⬆️", lambda: self.move_player("N"))
        self.view.stats.addAction("⬇️", lambda: self.move_player("S"))
        self.view.stats.addAction("⬅️", lambda: self.move_player("W"))
        self.view.stats.addAction("➡️", lambda: self.move_player("E"))
        self.view.stats.addSeparator()

    def move_player(self, direction: str):
        old_pos = self.player.move(direction)
        self.view.remove_player_from_grid(*old_pos)
        self.view.add_tile_to_grid("P", *self.player.pos)
        current_tile = self.board.nodes[self.player.pos[1]][self.player.pos[0]]
        last_action = self.view.stats.actions()[-1]
        if last_action.text() != "":
            self.view.stats.removeAction(last_action)

        if current_tile.tile.action_type == "C":
            self.view.stats.addAction(
                act := current_tile.tile.action, self.actions[act]
            )
        elif current_tile.tile.action_type == "F":
            self.actions[current_tile.tile.action]()
            self.view.remove_player_from_grid(*self.player.pos)
            self.view.remove_tile_from_grid(*self.player.pos)
            self.view.add_tile_to_grid(icons["plain"], *self.player.pos)
            self.view.add_tile_to_grid("P", *self.player.pos)
            self.board.nodes[self.player.pos[1]][self.player.pos[0]] = Node(
                *self.player.pos,
                icons["plain"],
            )
