from typing import List
import json

class Ship():
    def __init__(self, cords : tuple, shot_cords : List[tuple] = []):
        if not Ship.validate_cords(cords):
            raise ValueError("You have entered incorrect ship coordinates.")
        self.cords = cords
        self.shot_cords = shot_cords

    @property
    def is_dead(self):
        if len(self.shot_cords) == len(self.cords):
            return True
        return False

    def try_shot_to_ship(self, x, y):
        if (x,y) in self.cords:
            self.shot_cords.append((x,y))
            return True
        return False

    @staticmethod
    def validate_cords(cords):
        if len(cords) < 1:
            return True
        for i in range(len(cords) - 1):
            if abs(cords[i][0] - cords[i+1][0]) > 1:
                return False
            if abs(cords[i][1] - cords[i+1][1]) > 1:
                return False
            if cords[i][0] != cords[i+1][0] and \
                cords[i][1] != cords[i+1][1]:
                return False
        return True

    @staticmethod
    def ship_crossing(ship_1, ship_2):
        for x,y in ship_1.cords:
            for _x,_y in ship_2.cords:
                if _x == x and _y == y:
                    return True
        return False

    def serialize(self):
        return json.dumps(self.__dict__,default=lambda o: o.__dict__)
