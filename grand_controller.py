from base_workings.player import Player

# import end of level quiz
import view


class GrandController:
    def __init__(self):
        self.player = Player()

        view.main(1, self.player)


if __name__ == "__main__":
    GrandController()
