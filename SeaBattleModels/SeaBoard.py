from typing import List
import json
import copy
from .Ship import Ship
from config import EMPTY_CHAR, LIVE_SHIP_CHAR, DEAD_SHIP_CHAR, MISS_SHIP_CHAR, HIT_SHIP_CHAR

class SeaBoard():
    def __init__(self, size : int = 10, max_count_ship = 6,
            ships : List[Ship] = [], shots_cords : List[tuple] = [],
            missed_cords : List[tuple] = []):
        self.size = size
        self.ships = ships
        
        if len(ships) > 0 and isinstance(ships[0], dict):
            self.ships = [Ship.deserialize(x) for x in ships]
        self.max_count_ship = max_count_ship
        
        self.shots_cords = shots_cords
        if len(shots_cords) > 0 and isinstance(shots_cords[0], list):
            self.shots_cords = [(x[0],x[1]) for x in shots_cords]

        self.missed_cords = missed_cords
        if len(missed_cords) > 0 and isinstance(missed_cords[0], list):
            self.missed_cords = [(x[0],x[1]) for x in missed_cords]

    def count_ship_is_live(self):
        return len(list(self.get_lives_ship()))

    def game_is_lost(self):
        return self.count_ship_is_live() == 0

    def add_ship(self, ship):
        if self.max_count_ship <= len(self.ships):
            raise Exception('You can no longer add a ship')
        if not self.can_add_ship(ship):
            raise ValueError("You cannot add this ship.")
        self.ships.append(ship)
        return True

    def try_shot(self, cords):
        self.shots_cords.append(cords)
        for _ship in self.ships:
            if _ship.try_shot_to_ship(*cords):
                return True
        self.missed_cords.append(cords)
        return False

    def get_lives_ship(self):
        for x in self.ships:
            if not x.is_dead:
                yield x

    def can_add_ship(self, new_ship) -> bool:
        for _ship in self.ships:
            if Ship.ship_crossing(_ship, new_ship):
                return False
        return True

    def get_board(self):
        board = [[EMPTY_CHAR for __ in range(self.size)] for _ in range(self.size)]
        for x,y in self.shots_cords: # HIT'S SHIP
            board[x][y] = HIT_SHIP_CHAR
        for x,y in self.missed_cords: # MISSED SHOOTS
            board[x][y] = MISS_SHIP_CHAR

        for ship in self.ships:
            for x,y in ship.cords: # LIVE CORDS
                board[x][y] = LIVE_SHIP_CHAR
            for x,y in ship.shot_cords: # KILLED CORDS FOR SHIP
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