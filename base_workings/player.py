from typing import List
from base_workings.map_generation_using_kruskals_alg import Node


class Player:
    def __init__(self):
        self.max_stamina = 10
        self.stamina = self.max_stamina
        self.exp = 0
        self.level = 1
        self.coins = 0

    def set_up(
        self,
        pos: List[int],
        board: List[List[Node]],
        w: int,
        h: int,
        level_up: callable,
    ) -> None:
        self.pos = pos
        self.board = board
        self.board_w = w
        self.board_h = h
        self.on_level_up = level_up

    def gain_health(self, health: int) -> None:
        self.stamina += health
        self.stamina = min(self.stamina, self.max_stamina)

    def move(self, direction: str) -> List[int]:
        # Only move if there is a clear tile where the player is going

        directions = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}
        change_x, change_y = directions[direction]
        new_x = self.pos[0] + change_x
        new_y = self.pos[1] + change_y

        # Make sure they are staying on the map
        if new_x < 0 or self.board_w - 1 < new_x:
            return self.pos
        if new_y < 0 or self.board_h - 1 < new_y:
            return self.pos

        # Make sure the next tile is walkable
        future = self.board[new_y][new_x]
        if not future.tile.walkable:
            return self.pos

        self.pos = [new_x, new_y]
        return [new_x - change_x, new_y - change_y]

    def gain_exp(self, exp: int) -> None:
        if exp >= 0:
            self.exp += exp
            while self.exp / (5 * self.level) >= 1:
                self.exp -= 5 * self.level
                self.level_up()

    def level_up(self) -> None:
        self.level += 1
        self.max_stamina += 10
        self.stamina = self.max_stamina
        self.on_level_up(self.level)
