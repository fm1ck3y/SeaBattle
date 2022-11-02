
from SocketNetwork import Server
from SeaBattleModels import SeaBoard

class SeaBattleServer(Server):
    def __init__(self, ip = "127.0.0.1", port = 1000, max_connections=2):
        super().__init__(ip, port, max_connections, handler_func=self.handler_sea_game)
        self.boards = dict()

    def handler_sea_game(self, data, addr):
        if data['command'] == 'set_username':
            self.data_connection[addr]['username'] = data['username']
            self.data_connection[addr]['found'] = True

        elif data['command'] == "init_board":
            if addr not in self.boards:
                self.boards[addr] = SeaBoard.deserialize(data['sea_board'])
                print(f"Board init for {addr}")

            elif hash(self.boards[addr]) != data['board_hash']:
                return {"status" : "incorrect_board", "sea_board": self.boards[addr].serialize()}

        elif data['command'] == "wait_opponent_found":
            if len(self.data_connection.keys()) > 1:
                for _addr in self.data_connection.keys():
                    if 'found' in self.data_connection[_addr]:
                        if self.data_connection[_addr]['found']:
                            self.data_connection[addr]['opponent'] = _addr
                            self.data_connection[addr]['ready'] = False
                            self.data_connection[_addr]['opponent'] = addr
                            self.data_connection[_addr]['ready'] = False
                        return {"opponent_found" : self.data_connection[_addr]['found'], "status" : "ok"}
            return {"opponent_found" : False, "status" : "ok"}
        
        elif data['command'] == "wait_opponent_ready":
            _addr_opponent = self.data_connection[addr]['opponent']
            if not _addr_opponent in self.data_connection:
                self.data_connection[addr].pop('opponent')
                self.data_connection[addr]['found'] = False
                return {"opponent_ready" : None, "status" : "ok"}
            return {"opponent_ready" : self.data_connection[_addr_opponent]['ready'], "status" : "ok"}

        return {"status" : "ok"}

if __name__ == "__main__":
    SeaBattleServer().accept()
