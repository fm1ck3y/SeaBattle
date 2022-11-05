from SeaBattleModels import Ship
from SeaBattleModels import SeaBoard
import os
import config

class ConsoleMenu:
    ADD_SHIP_INPUT = 1
    BOARD_READY_INPUT = 2
    EXIT_INPUT = 3

    @staticmethod
    def add_ship():
        print("1) one-deck ship",
              "2) two-deck ship",
              "3) three-deck ship",
              "4) four-deck ship", sep="\n")

        ship_count_cords = int(input("Enter type ship: "))
        cords = list()
        for _ in range(ship_count_cords):
            x,y = map(int, input("Enter cords x,y (example 1,1): ").split(','))
            if not Ship.validate_cords(cords + [(x,y)]):
                print("Your enter invalid cords for this ship.")
                continue
            cords.append((x-1,y-1))
        return Ship(cords)

    @staticmethod
    def pre_game(client):
        os.system(config.CLEAR_COMMAND)
        while True:
            print(f"Count ships on board: {len(client.sea_board.ships)}")
            print(client.sea_board)
            print("","1. Add ship",
                  "2. Board ready",
                  "3. Exit", sep="\n")
            type = int(input())
            os.system(config.CLEAR_COMMAND)
            if type == ConsoleMenu.ADD_SHIP_INPUT:
                ship = ConsoleMenu.add_ship()
                client.sea_board.add_ship(ship)
            elif type == ConsoleMenu.BOARD_READY_INPUT:
                client.init_board()
                break
            elif type == ConsoleMenu.EXIT_INPUT:
                exit(0)
            else:
                print("Your enter invalid num of functions.")

    @staticmethod
    def wait_found_opponent(client):
        if not client.wait_opponent(type="found"):
            print("Couldn't find an opponent. Try again later")
            exit(1)

    @staticmethod
    def wait_ready_opponent(client):
        if not client.wait_opponent(type="ready"):
            print("Your opponent missed or got out. Please try again later.")
            exit(1)

    @staticmethod
    def try_shot(client):
        input()

    @staticmethod
    def print_sea_boards(my_sea_board, opponent_sea_board):
        my_sea_board_str = str(client.sea_board)
        opponent_sea_board_str = str(client.opponent_sea_board)        
        print("-"*5, "BOARD", "-"*5)
        for line_1 , line_2 in my_sea_board_str.split('\n'), opponent_sea_board_str.split('\n'):
            print(line_1, "\t\t", line_2)

    @staticmethod
    def progress_game(client):
        while True:
            my_turn = client.is_my_turn()
            if my_turn is None:
                break
            if not my_turn:
                client.wait_opponent(type="turn")

            os.system(config.CLEAR_COMMAND)
            client.update_opponent_board()
            ConsoleMenu.print_sea_boards(client)
            ConsoleMenu.try_shot(client)
        print("Game is end.")
