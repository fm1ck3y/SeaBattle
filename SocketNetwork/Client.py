import socket
import json

class Client():
    def __init__(self, ip, port, username):
        self.ip = ip
        self.port = port
        self.username = username

    def connect(self):
        print(f"Connection to {self.ip}:{self.port}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        response = self.send_data_with_response({'command' : 'set_username','username': self.username})
        if response["status"] == "ok":
            print(f"Connection {self.ip}:{self.port} success")

    def __send_data(self, data):
        try:
            return self.sock.send(
                json.dumps(data).encode('UTF-8')
            )
        except Exception as e:
            print(e)
            print(f"Can't send data to {self.ip}:{self.port}")
            self.__del__()

    def send_data_with_response(self, data):
        d = self.__send_data(data)
        return self.__wait_response()

    def __wait_response(self, data = ""):
        _data = self.sock.recv(1024).decode('UTF-8')
        if not _data:
            print(f"Can't recv data to {self.ip}:{self.port}")
            self.__del__()
        data += _data
        try:
            return json.loads(data)
        except ValueError:
            self.__wait_response(data=data)

    def __del__(self):
        print(f"Connection close: {self.ip}:{self.port}")
        self.sock.close()
