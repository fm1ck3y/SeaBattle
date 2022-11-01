from SeaBattleModels import SeaBoard
from SocketNetwork import Client

class ClientSeaBattle(Client):
    def __init__(self, ip, port, username, size_board, max_count_ship):
        super().__init__(ip,port,username)
        self.sea_board = SeaBoard(size_board,max_count_ship)

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
