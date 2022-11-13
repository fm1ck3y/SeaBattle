
from SocketNetwork import Server
from SeaBattleModels import SeaBoard
import config
import random

class SeaBattleServer(Server):
    def __init__(self, ip = config.DEFAULT_HOST, port = config.DEFAULT_PORT, max_connections=2):
        super().__init__(ip, port, max_connections, handler_func=self.handler_sea_game)
        self.boards = dict()

    def handler_sea_game(self, data, addr):
        if data['command'] == 'set_username':
            self.data_connection[addr]['username'] = data['username']
            self.data_connection[addr]['found'] = True

        elif data['command'] == "init_board":
            if addr not in self.boards:
                self.boards[addr] = SeaBoard.deserialize(data['sea_board'])
                self.data_connection[addr]['my_turn'] = False
                self.data_connection[addr]['ready'] = True
                print(f"Board init for {addr}")

            elif hash(self.boards[addr]) != data['board_hash']:
                return {"status" : "incorrect_board", "sea_board": self.boards[addr].serialize()}

            _addr_opponent = self.data_connection[addr]['opponent']
            if _addr_opponent in self.data_connection.keys() and \
                    self.data_connection[_addr_opponent]['ready']:
                print("Random turn")
                self.data_connection[random.choice([addr,_addr_opponent])]['my_turn'] = True

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

        elif data['command'] == 'wait_opponent_turn':
            if 'my_turn' in self.data_connection[addr]:
                return {"opponent_turn" : self.data_connection[addr]['my_turn'], "status" : "ok"}
            return {"opponent_turn" : None, "status" : "ok"}

        elif data['command'] == "wait_opponent_ready":
            if 'opponent' not in self.data_connection[addr]:
                return {"status" : "opponent exit"}
            _addr_opponent = self.data_connection[addr]['opponent']
            if not (_addr_opponent in self.data_connection.keys()):
                self.data_connection[addr].pop('opponent')
                self.data_connection[addr]['found'] = False
                return {"opponent_ready" : None, "status" : "ok"}
            return {"opponent_ready" : self.data_connection[_addr_opponent]['ready'], "status" : "ok"}

        elif data['command'] == 'get_opponent_board':
            if 'opponent' not in self.data_connection[addr]:
                return {"status" : "opponent exit"}
            _addr_opponent = self.data_connection[addr]['opponent']
            return {"sea_board": self.boards[_addr_opponent].serialize(hide_ships=True), "status" : "ok"}

        return {"status" : "ok"}

if __name__ == "__main__":
    try:
        server = SeaBattleServer()
        server.accept()
    except KeyboardInterrupt:
        server.close_connections()
        exit(1)
