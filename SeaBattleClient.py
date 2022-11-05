from SeaBattleModels import SeaBoard
from SocketNetwork import Client
import config
import time

class ClientSeaBattle(Client):
    def __init__(self, ip, port, username, size_board, max_count_ship):
        super().__init__(ip,port,username)
        self.sea_board = SeaBoard(size_board,max_count_ship)
        self.opponent_sea_board = None

    def init_board(self):
        response = self.send_data_with_response({
            "command" : "init_board",
            "sea_board" : self.sea_board.serialize(),
            "board_hash": hash(self.sea_board)
        })
        if response["status"] == "incorrect_board":
            self.sea_board = SeaBoard.deserialize(response['sea_board'])

        if response["status"] == "ok":
            return True

        return False

    def wait_opponent(self, type):
        for counter,_ in enumerate(range(config.MAX_COUNT_WAIT_APPONENT)):
            print(f"[{counter}/{config.MAX_COUNT_WAIT_APPONENT}] Wait opponent every {config.EVERY_SECOND_WAIT_APPONENT} second.")
            response = self.send_data_with_response({
                "command" : f"wait_opponent_{type}"
            })
            if response[f"opponent_{type}"]:
                return True
            if response[f"opponent_{type}"] is None:
                return False
            time.sleep(config.EVERY_SECOND_WAIT_APPONENT)
        return False

    def is_my_turn(self) -> bool:
        try:
            response = self.send_data_with_response({
                "command" : "is_my_turn"
            })
            if response['your_turn']:
                return True
            return False
        except: return False

    def update_opponent_board(self):
        response = self.send_data_with_response({
            "command" : "get_opponent_board"
        })
        self.opponent_sea_board = SeaBoard.deserialize(response['sea_board'])
        return self.opponent_sea_board
