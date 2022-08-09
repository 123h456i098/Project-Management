from dataclasses import dataclass


@dataclass
class Tile:
    _walkable: bool
    _action_type: str
    _action: str

    @property
    def walkable(self):
        # To see if the tile can be walked on
        return self._walkable

    @property
    def action_type(self):
        # To see if the action is (C)hoice, or (F)orced
        return self._action_type

    @property
    def action(self):
        # To see what the action is
        return self._action


tiles = {
    "plain": Tile(True, "", ""),
    "wall": Tile(False, "", ""),
    "monster": Tile(True, "F", "Fight"),
    "shop": Tile(True, "C", "Shop"),
    "chest": Tile(True, "C", "Chest"),
    "trap": Tile(True, "F", "Trap"),  # TODO be made invisible
    "question": Tile(True, "F", "Question"),
    "start": Tile(True, "", ""),
    "finish": Tile(True, "C", "Finish"),
}
