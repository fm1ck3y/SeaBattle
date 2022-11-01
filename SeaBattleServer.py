
from SocketNetwork import Server
from SeaBattleModels import SeaBoard

class SeaBattleServer(Server):
    def __init__(self, ip = "127.0.0.1", port = 1000, max_connections=2):
        super().__init__(ip, port, max_connections, handler_func=self.handler_sea_game)
        self.boards = dict()

    def handler_sea_game(self, data, addr):
        if data['command'] == 'set_username':
            self.data_connection[addr]['username'] = data['username']

        if data['command'] == "init_board":
            if addr not in self.boards:
                self.boards[addr] = SeaBoard.deserialize(data['sea_board'])
                print(f"Board init for {addr}")

            elif hash(self.boards[addr]) != data['board_hash']:
                return {"status" : "incorrect_board", "sea_board": self.boards[addr].sirialize()}
        return {"status" : "ok"}

if __name__ == "__main__":
    SeaBattleServer().accept()
