from typing import List
import json
import copy
from .Ship import Ship
from config import EMPTY_CHAR, LIVE_SHIP_CHAR, DEAD_SHIP_CHAR

class SeaBoard():
    def __init__(self, size : int = 10, max_count_ship = 6,
            ships : List[Ship] = [], shots_cords : List[tuple] = []):
        self.size = size
        self.ships = ships
        self.max_count_ship = max_count_ship
        self.shots_cords = shots_cords

    def count_ship_is_live(self):
        return sum(self.get_lives_ship())

    def add_ship(self, ship):
        if self.max_count_ship <= len(self.ships):
            raise Exception('You can no longer add a ship')
        if not self.can_add_ship(ship):
            raise ValueError("You cannot add this ship.")
        self.ships.append(ship)
        return True

    def try_shot(self, cords):
        for _ship in self.ships:
            if _ship.try_shot_to_ship(*cords):
                return True
        return False

    def get_lives_ship(self):
        return [not x.is_dead for x in self.ships]

    def can_add_ship(self, new_ship) -> bool:
        for _ship in self.ships:
            if Ship.ship_crossing(_ship, new_ship):
                return False
        return True

    def get_board(self):
        board = [[EMPTY_CHAR for __ in range(self.size)] for _ in range(self.size)]
        for ship in self.ships:
            for x,y in ship.cords:
                board[x][y] = LIVE_SHIP_CHAR
            for x,y in ship.shot_cords:
                board[x][y] = DEAD_SHIP_CHAR
            for x,y in self.shots_cords:
                board[x][y] = DEAD_SHIP_CHAR
        return board

    @staticmethod
    def deserialize(data):
        return SeaBoard(**json.loads(data))

    def serialize(self, hide_ships = False):
        if hide_ships:
            _self = copy.deepcopy(self)
            for _ship in list(_self.get_lives_ship()):
                _self.ships.remove(_ship)
            return json.dumps(_self.__dict__, default=lambda o: o.__dict__)
        else:
            return json.dumps(self.__dict__, default=lambda o: o.__dict__)

    def __str__(self):
        _str = ""
        for raw in self.get_board():
            _str += f"\n{' '.join(raw)}"
        return _str

    def __hash__(self):
        return hash(str(self.get_board()))