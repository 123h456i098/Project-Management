class Player:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.stamina = 100

    def move(self, direction: str, board: list):
        # check if player can move to that space (wall) edge of map
        # print()
        # Move that direction
        match direction:
            case "N":
                self.pos[1] -= 1
                print(board[self.pos[1]][self.pos[0]].tile)
                return [self.pos[0], self.pos[1] + 1]
            case "E":
                self.pos[0] += 1
                print(board[self.pos[1]][self.pos[0]].tile)
                return [self.pos[0] - 1, self.pos[1]]
            case "S":
                self.pos[1] += 1
                print(board[self.pos[1]][self.pos[0]].tile)

                return [self.pos[0], self.pos[1] - 1]
            case "W":
                self.pos[0] -= 1
                print(board[self.pos[1]][self.pos[0]].tile)

                return [self.pos[0] + 1, self.pos[1]]
