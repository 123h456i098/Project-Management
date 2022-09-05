from base_workings.player import Player
from base_workings.map_generation_using_kruskals_alg import MapBoard, Node
from base_workings.tiles import icons
from main_files.fighting import FightView
from main_files.question import Question
from main_files.chest import Chest


class Controller:
    def __init__(self, view, w, h):
        self.view = view
        h += 1 if h % 2 == 0 else 0
        w += 1 if w % 2 == 0 else 0
        self.board = MapBoard(w, h)
        self.player = Player(*self.board.start, self.board.nodes, w, h)
        self.view.set_controllers_action_function(self.action)
        self.actions = {
            "Trap": self.trap,
            "Fight": self.open_fight_view,
            "Question": self.open_question,
            "Chest": self.open_chest,
            "Shop": lambda: print("shop"),
            "Finish": lambda: print("finish"),
        }

    def trap(self):
        self.player.stamina -= 1
        self._update_toolbar_labels()

    # region - Open views
    def open_fight_view(self):
        self.fight = FightView(self.player, self._done_fighting)
        self.fight.show()
        self.view.hide()

    def open_question(self):
        self.question = Question(self._done_question)
        self.question.show()
        self.view.hide()

    def open_chest(self):
        self.chest = Chest(self.done_chest)
        self.chest.show()
        self.view.hide()

    # endregion

    # region - Close views
    def _done_fighting(self, stamina, exp_to_get, coin):
        self.player.coins += coin
        self.player.stamina = stamina
        self.player.gain_exp(exp_to_get)
        self._done_action(self.fight)

    def _done_question(self, correct):
        if correct:
            self.player.gain_exp(1)
        else:
            self.player.stamina -= 1
        self._done_action(self.question)

    def done_chest(self, coins, health):
        self.player.coins += coins
        self.player.stamina += health
        self.view.stats.removeAction(self.view.stats.actions()[-1])
        # Replace with opened chest icon
        self.view.remove_player_from_grid(*self.player.pos)
        self.view.remove_tile_from_grid(*self.player.pos)
        self.view.add_tile_to_grid(icons["opened"], *self.player.pos)
        self.view.add_tile_to_grid("@", *self.player.pos)
        self.board.nodes[self.player.pos[1]][self.player.pos[0]] = Node(
            *self.player.pos,
            icons["plain"],
        )
        self._done_action(self.chest)

    def _done_action(self, view):
        if self.player.stamina > 0:
            self._update_toolbar_labels()
            view.close()
            self.view.show()
        else:
            print("you died")
            self.view.close()

    # endregion

    def _update_toolbar_labels(self):
        self.remove_labels_from_toolbar()
        self.add_labels_to_toolbar()

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
        self.view.add_tile_to_grid("@", *self.player.pos)
        self.view.stats.addAction("⬆️", lambda: self.move_player("N"))
        self.view.stats.addAction("⬇️", lambda: self.move_player("S"))
        self.view.stats.addAction("⬅️", lambda: self.move_player("W"))
        self.view.stats.addAction("➡️", lambda: self.move_player("E"))
        self.view.stats.addSeparator()
        self.add_labels_to_toolbar()

    def add_labels_to_toolbar(self):
        self.view.add_label_to_toolbar(
            f"Stamina:\n{self.player.stamina}/{self.player.max_stamina}\n"
        )
        self.view.add_label_to_toolbar(
            f"EXP:\n{self.player.exp}/{5*self.player.level}\n"
        )
        self.view.add_label_to_toolbar(f"Level: {self.player.level}\n")
        self.view.add_label_to_toolbar(f"Coins: ${self.player.coins}\n")

    def remove_labels_from_toolbar(self):
        for label in self.view.toolbar_labels:
            self.view.remove_label_from_toolbar(label)
        self.view.toolbar_labels = []

    def move_player(self, direction: str):
        old_pos = self.player.move(direction)
        self.view.remove_player_from_grid(*old_pos)
        self.view.add_tile_to_grid("@", *self.player.pos)
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
            self.view.add_tile_to_grid(
                icons[
                    "plain" if current_tile.tile.action != "Trap" else "trap"
                ],
                *self.player.pos,
            )
            self.view.add_tile_to_grid("@", *self.player.pos)
            self.board.nodes[self.player.pos[1]][self.player.pos[0]] = Node(
                *self.player.pos,
                icons["plain"],
            )
