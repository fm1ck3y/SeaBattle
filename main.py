from SeaBattleClient import ClientSeaBattle
from ConsoleMenu import ConsoleMenu
import os
import config

if __name__ == "__main__":
    username = input("Enter your username: ")
    with ClientSeaBattle("127.0.0.1", 1000, username, \
                    max_count_ship=config.DEFAULT_MAX_COUNT_SHIP_ON_BOARD,\
                    size_board=config.DEFAULT_SIZE_BOARD) as client:
        ConsoleMenu.wait_found_opponent(client)
        ConsoleMenu.pre_game(client)
        ConsoleMenu.wait_ready_opponent(client)
        ConsoleMenu.progress_game()
