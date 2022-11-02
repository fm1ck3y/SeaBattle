from SeaBattleClient import ClientSeaBattle
from SeaBattleModels import Ship
import os
from SeaBattleModels.SeaBoard import SeaBoard
import config

class ConsoleMenu:
    ### pre game menu
    ADD_SHIP_INPUT = 1
    BOARD_READY_INPUT = 2
    EXIT_INPUT = 3
    ###

    ### progress game menu 

    ###

    @staticmethod
    def enter_ship_cords():
        print("1) one-deck ship",
              "2) two-deck ship",
              "3) three-deck ship",
              "4) four-deck ship", sep="\n")

        ship_count_cords = int(input("Enter type ship: "))
        cords = list()
        for _ in range(ship_count_cords):
            x,y = map(int, input("Enter cords x,y (example 1,1): ").split(','))
            if not Ship.validate_cords(cords + (x,y)):
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
                ship = ConsoleMenu.add_ship_input()
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

    def progress_game(client):
        pass
        

if __name__ == "__main__":
    username = input("Enter your username: ")
    with ClientSeaBattle("127.0.0.1", 1000, username, \
                    max_count_ship=config.DEFAULT_MAX_COUNT_SHIP_ON_BOARD,\
                    size_board=config.DEFAULT_SIZE_BOARD) as client:
        ConsoleMenu.wait_found_opponent(client)
        ConsoleMenu.pre_game(client)
        ConsoleMenu.wait_ready_opponent(client)
        ConsoleMenu.progress_game()
