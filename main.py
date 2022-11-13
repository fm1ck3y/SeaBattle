from SeaBattleClient import ClientSeaBattle
from ConsoleMenu import ConsoleMenu
import config

if __name__ == "__main__":
    username = input("Enter your username: ")
    with ClientSeaBattle(config.DEFAULT_HOST, config.DEFAULT_PORT, username, \
                    max_count_ship=config.DEFAULT_MAX_COUNT_SHIP_ON_BOARD,\
                    size_board=config.DEFAULT_SIZE_BOARD) as client:
        cm = ConsoleMenu(client)
        cm.wait_found_opponent()
        cm.pre_game()
        cm.wait_ready_opponent()
        cm.progress_game()
