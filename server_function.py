import socket
import json
from threading import Thread
import math
from collections import Counter

# 各RPC関数の定義
def floor(x):
    return math.floor(x)

def nroot(n,x):
   return math.floor(x**(1/n))

def reverse(s):
    return s[::-1]

def validAnagram(str1,str2):
    return Counter(str1) == Counter(str2)

def sort(arr):
    return sorted(arr)

# リクエストと関数を関連付けるハッシュマップ
functions = {
    "floor": floor,
    "nroot": nroot,
    "reverse": reverse,
    "validAnagram": validAnagram,
    "sort": sort
}

class SocketManager:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def bind_and_listen(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f'Listening on {self.host}:{self.port}')

    def accept_connection(self):
        connection, client_address = self.sock.accept()
        print(f'Connection from {client_address}')
        return connection, client_address

class RequestHandler:
    def __init__(self, connection):
        self.connection = connection
    
    def handle_request(self):
        try:
            data = self.connection.recv(1024)
            if not data:
                return 
            
            request = json.loads(data.decode('utf-8'))
            function_name = request.get('function')
            params = request.get('params')
            
            if function_name in functions:
                function = functions[function_name]
                response = function(*params)
            else:
                response = "Function not found"
            
            return response
        except Exception as e:
            return str(e)

class ResponseSender:
    def __init__(self, connection, response):
        self.connection = connection
        self.response = response

    def send_response(self):
        response_data = json.dumps(self.response)
        self.connection.sendall(response_data.encode('utf-8'))
        self.connection.close()

def client_handler(connection):
    request_handler = RequestHandler(connection)
    response = request_handler.handle_request()
    response_sender = ResponseSender(connection, response)
    response_sender.send_response()

def main():
    host = '127.0.0.1'
    port = 8080
    socket_manager = SocketManager(host, port)
    socket_manager.bind_and_listen()

    while True:
        connection, client_address = socket_manager.accept_connection()
        Thread(target=client_handler, args=(connection,)).start()

if __name__ == "__main__":
    main()
