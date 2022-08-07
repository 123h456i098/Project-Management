class Player:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.stamina = 100

    def move(self, direction: str):
        # check if player can move to that space (wall)
        pass
