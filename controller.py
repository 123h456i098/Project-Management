from base_workings.map_generation_using_kruskals_alg import MapBoard, Node
from base_workings.tiles import icons
from main_files.fighting import FightView
from main_files.question import Question
from main_files.chest import Chest
from main_files.shop import Shop
from main_files.end_quiz import Quiz
from base_workings.player import Player


class Controller:
    def __init__(self, w: int, h: int, view):
        self.view = view
        self.level = 1
        self.h = h + 1 if h % 2 == 0 else 0
        self.w = w + 1 if w % 2 == 0 else 0
        self.player = Player()
        self.view.set_controllers_action_function(self.action)
        self.actions = {
            "Trap": self.trap,
            "Fight": self.open_fight_view,
            "Question": self.open_question,
            "Chest": self.open_chest,
            "Shop": self.open_shop,
            "Finish": self.end_quiz,
        }
        self.startup()

    def reset(self) -> None:
        self.view.reset()
        self.startup()

    def startup(self) -> None:
        self.board = MapBoard(self.w, self.h)
        self.view.set_window_title(self.level)
        self.player.set_up(
            self.board.start,
            self.board.nodes,
            self.w,
            self.h,
            self.on_player_level_up,
        )
        self.view.set_controllers_enter_function(lambda: None)
        self.start()

    def end_quiz(self) -> None:
        self.quiz = Quiz(self.player, self._done_end_quiz, self.level)
        self.quiz.show()
        self.view.hide()

    def _done_end_quiz(self, next_level: bool) -> None:
        if next_level:
            if self.level == 4:
                self.quiz.close()
                self.view.show()
                self.on_player_win()
            else:
                self.level += 1
                self.reset()
                self.quiz.close()
                self.view.show()
        else:
            self.quiz.close()
            self.view.show()
            self.on_player_death()

    def on_player_win(self) -> None:
        print("Congradulations, you have won!")
        self.view.close()

    def on_player_level_up(self, level: int) -> None:
        text = f"You have reached Level: {level}\n Your max stamina has increased."
        self.view.message_box(["Level up!", text])

    def on_player_death(self) -> None:
        print(f"You died!\nYou reached dungeon level {self.level}")
        self.view.close()

    def trap(self) -> None:
        self.player.stamina -= 1
        if self.player.stamina <= 0:
            self.on_player_death()
        else:
            self._update_toolbar_labels()

    # region - Open views
    def open_fight_view(self) -> None:
        self.fight = FightView(self.player, self._done_fighting, self.level)
        self.fight.show()
        self.view.hide()

    def open_question(self) -> None:
        self.question = Question(self._done_question, self.level)
        self.question.show()
        self.view.hide()

    def open_chest(self) -> None:
        self.chest = Chest(self.done_chest, self.level)
        self.chest.show()
        self.view.hide()

    def open_shop(self) -> None:
        s = self.board.nodes[self.player.pos[1]][self.player.pos[0]].view
        if s is None:
            s = Shop(self.done_shop, self.player.coins, self.level)
            self.board.nodes[self.player.pos[1]][self.player.pos[0]].view = s
        else:
            s.p_coins = self.player.coins
            s.exit_button.setText(f"Back   (you have ${s.p_coins})")
        s.show()
        self.view.hide()

    # endregion

    # region - Close views
    def _done_fighting(self, stamina: int, exp_to_get: int, coin: int) -> None:
        self.player.coins += coin
        self.player.stamina = stamina
        self.player.gain_exp(exp_to_get)
        self._done_action(self.fight)

    def _done_question(self, correct: bool) -> None:
        if correct:
            self.player.gain_exp(1)
        else:
            self.player.stamina -= 1
        self._done_action(self.question)

    def done_chest(self, coins: int, health: int) -> None:
        self.view.set_controllers_enter_function(lambda: None)
        self.player.coins += coins
        self.player.gain_health(health)
        self.view.stats.removeAction(self.view.stats.actions()[-1])
        # Replace with opened chest icon
        self.view.remove_player_from_grid(*self.player.pos)
        self.view.remove_tile_from_grid(*self.player.pos)
        self.view.add_tile_to_grid(
            f"Images/{icons['opened']}.png", *self.player.pos
        )
        self.view.add_tile_to_grid("Images/player.png", *self.player.pos)
        self.board.nodes[self.player.pos[1]][self.player.pos[0]] = Node(
            *self.player.pos,
            icons["plain"],
        )
        self._done_action(self.chest)

    def _done_action(self, view: object):
        view.close()
        if self.player.stamina > 0:
            self._update_toolbar_labels()
            self.view.show()
        else:
            self.on_player_death()

    def done_shop(self, coins: int, exp: int, health: int) -> None:
        self.view.set_controllers_enter_function(lambda: None)
        self.player.coins = coins
        self.player.gain_health(health)
        self.player.gain_exp(exp)
        action = self.view.stats.actions()[-1]
        self.view.stats.removeAction(action)
        self._update_toolbar_labels()
        self.board.nodes[self.player.pos[1]][self.player.pos[0]].view.hide()
        self.view.show()

    # endregion

    def _update_toolbar_labels(self) -> None:
        self.remove_labels_from_toolbar()
        self.add_labels_to_toolbar()

    def action(self, action: str) -> None:
        if action == "up":
            self.move_player("N")
        elif action == "down":
            self.move_player("S")
        elif action == "left":
            self.move_player("W")
        elif action == "right":
            self.move_player("E")

    def start(self) -> None:
        for row in self.board.nodes:
            for each in row:
                self.view.add_tile_to_grid(
                    f"Images/{each.tile_type}.png", each.x, each.y
                )
        self.view.add_tile_to_grid("Images/player.png", *self.player.pos)
        self.view.stats.addAction("⬆️", lambda: self.move_player("N"))
        self.view.stats.addAction("⬇️", lambda: self.move_player("S"))
        self.view.stats.addAction("⬅️", lambda: self.move_player("W"))
        self.view.stats.addAction("➡️", lambda: self.move_player("E"))
        self.view.stats.addSeparator()
        self.add_labels_to_toolbar()

    def add_labels_to_toolbar(self) -> None:
        self.view.add_label_to_toolbar(
            f"Stamina:\n{self.player.stamina}/{self.player.max_stamina}\n"
        )
        self.view.add_label_to_toolbar(
            f"EXP:\n{self.player.exp}/{5*self.player.level}\n"
        )
        self.view.add_label_to_toolbar(f"Level: {self.player.level}\n")
        self.view.add_label_to_toolbar(f"Coins: ${self.player.coins}\n")

    def remove_labels_from_toolbar(self) -> None:
        for label in self.view.toolbar_labels:
            self.view.remove_label_from_toolbar(label)
        self.view.toolbar_labels = []

    def move_player(self, direction: str) -> None:
        old_pos = self.player.move(direction)
        self.view.remove_player_from_grid(*old_pos)
        self.view.add_tile_to_grid("Images/player.png", *self.player.pos)
        current_tile = self.board.nodes[self.player.pos[1]][self.player.pos[0]]
        last_action = self.view.stats.actions()[-1]
        if last_action.text() != "":
            self.view.stats.removeAction(last_action)
            self.view.set_controllers_enter_function(lambda: None)

        if current_tile.tile.action_type == "C":
            self.view.stats.addAction(
                act := current_tile.tile.action, self.actions[act]
            )
            self.view.set_controllers_enter_function(self.actions[act])
        elif current_tile.tile.action_type == "F":
            self.actions[current_tile.tile.action]()
            self.view.remove_player_from_grid(*self.player.pos)
            self.view.remove_tile_from_grid(*self.player.pos)
            file_name = f'Images/{icons["plain" if current_tile.tile.action != "Trap" else "trap"]}.png'

            self.view.add_tile_to_grid(
                file_name,
                *self.player.pos,
            )
            self.view.add_tile_to_grid("Images/player.png", *self.player.pos)
            self.board.nodes[self.player.pos[1]][self.player.pos[0]] = Node(
                *self.player.pos,
                icons["plain"],
            )
