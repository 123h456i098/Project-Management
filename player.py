class Player:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.stamina = 100

    def move(self, direction: str, board: list):
        tiles = board.nodes
        # old_pos = [self.pos[0], self.pos[1]]
        # Check if they are trying to move off the board
        if direction == "N":
            if self.pos[1] < 1:
                return self.pos
            future = tiles[self.pos[1] - 1][self.pos[0]]
            if not future.tile.walkable:
                return self.pos
            self.pos[1] -= 1
            return [self.pos[0], self.pos[1] + 1]
        if direction == "S":
            if self.pos[1] + 1 > board.h:
                return self.pos
            future = tiles[self.pos[1] + 1][self.pos[0]]
            if not future.tile.walkable:
                return self.pos
            self.pos[1] += 1
            return [self.pos[0], self.pos[1] - 1]
        if direction == "W":
            if self.pos[0] < 1:
                return self.pos
            future = tiles[self.pos[1]][self.pos[0] - 1]
            if not future.tile.walkable:
                return self.pos
            self.pos[0] -= 1
            return [self.pos[0] + 1, self.pos[1]]
        else:
            if self.pos[0] + 1 > board.w:
                return self.pos
            future = tiles[self.pos[1]][self.pos[0] + 1]
            if not future.tile.walkable:
                return self.pos
            self.pos[0] += 1
            return [self.pos[0] - 1, self.pos[1]]
