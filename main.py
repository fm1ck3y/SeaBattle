from SeaBattleClient import ClientSeaBattle
from SeaBattleModels import Ship
import sys
import os

if sys.platform == "linux" or sys.platform == "linux2":
    CLEAR_COMMAND = "clear"
elif sys.platform == "darwin":
    CLEAR_COMMAND = "clear"
elif sys.platform == "win32":
    CLEAR_COMMAND = "cls"

def add_ship_input():
    os.system(CLEAR_COMMAND)
    print("1. 1x ship",
          "2. 2x ship",
          "3. 3x ship",
          "4. 4x ship", sep="\n")
    ship_count_cords = int(input("Enter type ship: "))
    cords = list()
    for _ in range(ship_count_cords):
        x,y = map(int, input("Enter cords x,y (example 1,1): ").split(','))
        cords.append((x-1,y-1))
    return Ship(cords)

def pre_game_menu():
    ADD_SHIP_INPUT = 1
    BOARD_READY_INPUT = 2
    EXIT_INPUT = 3

    while True:
        os.system(CLEAR_COMMAND)
        print(f"Count ships on board: {len(client.sea_board.ships)}")
        print(client.sea_board)
        print()

        print("1. Add ship",
              "2. Board ready",
              "3. Exit", sep="\n")
        type = int(input())

        if type == ADD_SHIP_INPUT:
            ship = add_ship_input()
            client.sea_board.add_ship(ship)
            os.system(CLEAR_COMMAND)

        if type == BOARD_READY_INPUT:
            client.init_board()
            break

        if type == EXIT_INPUT:
            os.system(CLEAR_COMMAND)
            exit(0)

def progress_game_menu():
    pass

if __name__ == "__main__":
    client = ClientSeaBattle("127.0.0.1", 1000, "fm1ck3y", max_count_ship=6, size_board=10)
    client.connect()
    pre_game_menu()
    progress_game_menu()
