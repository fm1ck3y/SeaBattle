import socket
import threading
import json
import sys

class Server:
    def __init__(self, ip = "127.0.0.1", port = 1000, max_connections=2, handler_func = None):
        self.ip = ip
        self.port = port
        self.max_connections = max_connections
        self.connections = dict()
        self.data_connection = dict()
        self.sock = self.bind()
        self.handler_func = handler_func
        if handler_func is None:
            self.handler_func = Server.default_handler_func

    def bind(self):
        sock = socket.socket()
        sock.bind((self.ip, self.port))
        sock.listen(self.max_connections)
        return sock

    def accept(self):
        print(f"Server started: {self.ip}:{self.port}")
        while True:
            try:
                conn, addr = self.sock.accept()
                print(f"New connection : {addr}")
                self.connections[addr] = conn
                _thread = threading.Thread(target=self.handler_conn, args=(addr, ))
                self.data_connection[addr] = dict()
                self.data_connection[addr]['thread'] = _thread
                _thread.start()
            except KeyboardInterrupt:
                sys.exit(1)

    def handler_conn(self, addr):
        while True:
            data = self.__wait_response(addr)
            if not data:
                break
            self.handler_data(data, addr)
        print(f"Connection {addr} closed.")
        self.connections.pop(addr)
        self.data_connection.pop(addr)

    def __send_data(self, data, addr):
        try:
            return self.connections[addr].send(
                json.dumps(data).encode('UTF-8')
            )
        except Exception as e:
            print(e)
            print(f"Can't send data to {self.ip}:{self.port}")

    def __wait_response(self, addr, data = ""):
        try:
            _data = self.connections[addr].recv(1024).decode('UTF-8')
            if not _data:
                return None
            data += _data
        except socket.error as e:
            return None

        try:
            return json.loads(data)
        except ValueError:
            self.__wait_response(addr, data=data)

    def handler_data(self, data, addr):
        response = self.handler_func(data, addr)
        self.__send_data(response, addr)

    @staticmethod
    def default_handler_func(data, addr):
        print(data, addr)
        return data

    def __del__(self):
        print(f"Connection close: {self.ip}:{self.port}")
        self.sock.close()
