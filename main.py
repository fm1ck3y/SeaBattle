from SeaBattleSocketApp import ClientSeaBattle, SeaBattleServer
from ConsoleMenu import ConsoleMenu
import argparse
import config

def start_client(args):
    username = input("Enter your username: ")
    with ClientSeaBattle(args.host, args.port, username, \
                    max_count_ship=config.DEFAULT_MAX_COUNT_SHIP_ON_BOARD,\
                    size_board=config.DEFAULT_SIZE_BOARD) as client:
        cm = ConsoleMenu(client)
        cm.wait_found_opponent()
        cm.pre_game()
        cm.wait_ready_opponent()
        cm.progress_game()

def start_server(args):
    try:
        server = SeaBattleServer(ip=args.host, port=args.port)
        server.accept()
    except KeyboardInterrupt:
        server.close_connections()
        exit(1)

def main():
    parser = argparse.ArgumentParser(description='SeaGame arguments')
    parser.add_argument('--port', default=config.DEFAULT_PORT, type=int, help='Port connection')
    parser.add_argument('--host', default=config.DEFAULT_HOST, type=str, help='Host connection')
    parser.add_argument('-c', '--client', action='store_true', help='Client type application')
    parser.add_argument('-s', '--server', action='store_true', help='Server type application')
    args = parser.parse_args()

    if args.client:
        start_client(args)
        exit(0)
    
    if args.server:
        start_server(args)
        exit(0)

if __name__ == "__main__":
    main()
