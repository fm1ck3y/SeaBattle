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
        input()

    def print_sea_boards(self):
        my_sea_board_str = str(self.client.sea_board)
        opponent_sea_board_str = str(self.client.opponent_sea_board)        
        print("-"*5, "BOARD", "-"*5)
        for line_1 , line_2 in my_sea_board_str.split('\n'), opponent_sea_board_str.split('\n'):
            print(line_1, "\t\t", line_2)

    def progress_game(self):
        while True:
            self.client.wait_opponent(type="turn")
            os.system(config.CLEAR_COMMAND)
            self.client.update_opponent_board()
            self.print_sea_boards(self.client)
            self.try_shot(self.client)
        print("Game is end.")
