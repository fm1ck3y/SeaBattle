
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
            return self.set_username(data,addr)
        elif data['command'] == "init_board":
            return self.init_board(data,addr)
        elif data['command'] == "wait_opponent_found":
            return self.wait_opponent_found(data,addr)
        elif data['command'] == 'check_on_game_end':
            return self.check_on_game_end(data,addr)
        elif data['command'] == "wait_opponent_ready":
            return self.wait_opponent_ready(data, addr)
        elif data['command'] == 'get_opponent_board':
            return self.get_opponent_board(data, addr)
        elif data['command'] == 'get_my_board':
            return {"sea_board": self.boards[addr].serialize(), "status" : "ok"}
        elif data['command'] == 'shoot':
            return self.shoot(data, addr)

        return {"status" : "not_found"}

    def set_username(self, data, addr):
        self.data_connection[addr]['username'] = data['username']
        self.data_connection[addr]['found'] = True
        return {"status" : "ok"}

    def init_board(self, data, addr):
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
        return {"status" : "ok"}

    def wait_opponent_found(self, data, addr):
        if len(self.data_connection.keys()) > 1:
            for _addr in self.data_connection.keys():
                if 'found' in self.data_connection[_addr] and _addr != addr and self.data_connection[_addr]['found']:
                    self.data_connection[addr]['opponent'] = _addr
                    self.data_connection[addr]['ready'] = False
                    self.data_connection[_addr]['opponent'] = addr
                    self.data_connection[_addr]['ready'] = False
                    return {"opponent_found" : self.data_connection[_addr]['found'], "status" : "ok"}
        return {"opponent_found" : False, "status" : "ok"}

    def check_on_game_end(self, data, addr):
        if 'opponent' not in self.data_connection[addr]:
            return {"status" : "opponent exit"}
        _addr_opponent = self.data_connection[addr]['opponent']
        user_lost = self.boards[addr].game_is_lost()
        opponent_lost = self.boards[_addr_opponent].game_is_lost()
        return {
            "opponent_turn" : None,
            "status" : "ok",
            "opponent_lost" : opponent_lost,
            "game_end": user_lost or opponent_lost
        }

    def wait_opponent_ready(self, data, addr):
        if 'opponent' not in self.data_connection[addr]:
            return {"status" : "opponent exit"}
        _addr_opponent = self.data_connection[addr]['opponent']
        if not (_addr_opponent in self.data_connection.keys()):
            self.data_connection[addr].pop('opponent')
            self.data_connection[addr]['found'] = False
            return {"opponent_ready" : None, "status" : "ok"}
        return {"opponent_ready" : self.data_connection[_addr_opponent]['ready'], "status" : "ok"}

    def get_opponent_board(self, data, addr):
        if 'opponent' not in self.data_connection[addr]:
            return {"status" : "opponent exit"}
        _addr_opponent = self.data_connection[addr]['opponent']
        return {"sea_board": self.boards[_addr_opponent].serialize(hide_ships=True), "status" : "ok"}

    def shoot(self, data, addr):
        if 'opponent' not in self.data_connection[addr]:
            return {"status" : "opponent exit"}
        _addr_opponent = self.data_connection[addr]['opponent']
        hit = self.boards[_addr_opponent].try_shot((data['x'], data['y']))
        return {"status" : "ok", 'hit': hit}
