from base_workings.player import Player
from base_workings.tiles import tiles, Tile


class Node:
    def __init__(self, tile: Tile):
        self.tile = tile


example_board = [
    ["plain", "wall", "plain", "wall", "plain"],
    ["wall", "plain", "plain", "plain", "wall"],
    ["plain", "wall", "plain", "wall", "plain"],
    ["plain", "plain", "wall", "plain", "plain"],
    ["plain", "wall", "plain", "plain", "plain"],
]

example_tiles = []
for row in example_board:
    example_tiles.append([])
    for each in row:
        example_tiles[-1].append(Node(tiles[each]))


# region - Movement clear within the board
def test_movement_up_clear() -> None:
    """Tests that the player will move up one if the above tile is clear"""
    player = Player(2, 2, example_tiles, 5, 5)
    player.move("N")
    assert player.pos == [2, 1]


def test_movement_down_clear() -> None:
    """Tests that the player will move down if the lower tile is clear"""
    player = Player(2, 1, example_tiles, 5, 5)
    player.move("S")
    assert player.pos == [2, 2]


def test_movement_left_clear() -> None:
    """Tests that the player will move left one if the left tile is clear"""
    player = Player(2, 1, example_tiles, 5, 5)
    player.move("W")
    assert player.pos == [1, 1]


def test_movement_right_clear() -> None:
    """Tests that the player will move right if the right tile is clear"""
    player = Player(2, 1, example_tiles, 5, 5)
    player.move("E")
    assert player.pos == [3, 1]


# endregion

# region - Movement blocked within the board
def test_movement_up_blocked() -> None:
    """Tests that the player will not move up one if the above tile is wall"""
    player = Player(1, 3, example_tiles, 5, 5)
    player.move("N")
    assert player.pos == [1, 3]


def test_movement_down_blocked() -> None:
    """Tests that the player will not move down if the lower tile is wall"""
    player = Player(2, 2, example_tiles, 5, 5)
    player.move("S")
    assert player.pos == [2, 2]


def test_movement_left_blocked() -> None:
    """Tests that the player will not move left one if the left tile is wall"""
    player = Player(2, 2, example_tiles, 5, 5)
    player.move("W")
    assert player.pos == [2, 2]


def test_movement_right_blocked() -> None:
    """Tests that the player will not move right if the right tile is wall"""
    player = Player(2, 2, example_tiles, 5, 5)
    player.move("E")
    assert player.pos == [2, 2]


# endregion

# region - Movement clear to the border
def test_movement_up_clear_to_border() -> None:
    """Tests that player will move up one if the above border tile is clear"""
    player = Player(2, 1, example_tiles, 5, 5)
    player.move("N")
    assert player.pos == [2, 0]


def test_movement_down_clear_to_border() -> None:
    """Tests the player will move down if the lower border tile is clear"""
    player = Player(3, 3, example_tiles, 5, 5)
    player.move("S")
    assert player.pos == [3, 4]


def test_movement_left_clear_to_border() -> None:
    """Tests the player will move left one if the left border tile is clear"""
    player = Player(1, 3, example_tiles, 5, 5)
    player.move("W")
    assert player.pos == [0, 3]


def test_movement_right_clear_to_border() -> None:
    """Tests the player will move right if the right border tile is clear"""
    player = Player(3, 3, example_tiles, 5, 5)
    player.move("E")
    assert player.pos == [4, 3]


# endregion

# region - Movement blocked to the border
def test_movement_up_blocked_to_border() -> None:
    """Tests the player will not move up if the above border tile is wall"""
    player = Player(1, 1, example_tiles, 5, 5)
    player.move("N")
    assert player.pos == [1, 1]


def test_movement_down_blocked_to_border() -> None:
    """Tests the player will not move down if the lower border tile is wall"""
    player = Player(1, 3, example_tiles, 5, 5)
    player.move("S")
    assert player.pos == [1, 3]


def test_movement_left_blocked_to_border() -> None:
    """Tests the player will not move left if the left border tile is wall"""
    player = Player(1, 1, example_tiles, 5, 5)
    player.move("W")
    assert player.pos == [1, 1]


def test_movement_right_blocked_to_border() -> None:
    """Tests the player will not move right if the right border tile is wall"""
    player = Player(3, 1, example_tiles, 5, 5)
    player.move("E")
    assert player.pos == [3, 1]


# endregion
