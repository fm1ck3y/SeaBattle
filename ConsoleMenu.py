from SeaBattleModels import Ship
from SeaBattleModels import SeaBoard
import os
import config

class ConsoleMenu:
    ADD_SHIP_INPUT = 1
    BOARD_READY_INPUT = 2
    EXIT_INPUT = 3

    def __init__(self, client) -> None:
        self.client = client

    @staticmethod
    def add_ship(size_board):
        print("1) one-deck ship",
              "2) two-deck ship",
              "3) three-deck ship",
              "4) four-deck ship", sep="\n")

        ship_count_cords = int(input("Enter type ship: "))
        cords = list()
        while len(cords) != ship_count_cords:
            x,y = map(int, input("Enter cords x,y (example 1,1): ").split(','))
            if not Ship.validate_cords(cords + [(x-1,y-1)], size_board):
                print("Your enter invalid cords for this ship.")
                continue
            cords.append((x-1,y-1))
        return Ship(cords)

    def pre_game(self):
        os.system(config.CLEAR_COMMAND)
        while True:
            print(f"Count ships on board: {len(self.client.sea_board.ships)}")
            print(self.client.sea_board)
            print("","1. Add ship",
                  "2. Board ready",
                  "3. Exit", sep="\n")
            type = int(input())
            os.system(config.CLEAR_COMMAND)
            if type == ConsoleMenu.ADD_SHIP_INPUT:
                try:
                    ship = ConsoleMenu.add_ship(self.client.sea_board.size)
                    self.client.sea_board.add_ship(ship)
                except ValueError:
                    pass
            elif type == ConsoleMenu.BOARD_READY_INPUT:
                self.client.init_board()
                break
            elif type == ConsoleMenu.EXIT_INPUT:
                exit(0)
            else:
                print("Your enter invalid num of functions.")

    def wait_found_opponent(self):
        if not self.client.wait_opponent(type="found"):
            print("Couldn't find an opponent. Try again later")
            exit(1)

    def wait_ready_opponent(self):
        if not self.client.wait_opponent(type="ready"):
            print("Your opponent missed or got out. Please try again later.")
            exit(1)

    def try_shot(self):
        print("Shoooot him!")
        x,y = map(int, input("Enter cords x,y (example 1,1): ").split(','))
        if x+1 > self.client.sea_board.size or y+1 > self.client.sea_board.size:
            print("Your enter invalid cords for this ship.")
            return self.try_shot()
        return self.client.shoot_opponent(x,y)

    def print_sea_boards(self):
        my_sea_board_str_list = str(self.client.sea_board).split('\n')
        opponent_sea_board_str_list = str(self.client.opponent_sea_board).split('\n')
        print("-"*5, "BOARD", "-"*5)
        for i in range(len(my_sea_board_str_list)):
            print(my_sea_board_str_list[i], "\t\t", opponent_sea_board_str_list[i])

    def progress_game(self):
        while True:
            self.client.wait_opponent(type="turn")
            os.system(config.CLEAR_COMMAND)
            self.client.update_opponent_board()
            self.client.wait_opponent(type="turn")
            self.print_sea_boards()
            self.try_shot()
        print("Game is end.")
