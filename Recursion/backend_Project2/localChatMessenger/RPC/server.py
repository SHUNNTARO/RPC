import socket
import json
import inspect 
from threading import Thread
import os
#SocketManager:
#ソケットの作成、バインド、リッスンなどの基本操作を担当。

class SocketManager:
    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #UNIXSOCKET is created by SOCK_STREAM.
        
    def bind_and_listen(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(2)
        print(f'Listen on {self.host}:{self.port}')

    def accept_connection(self):
        connection, client_address = self.sock.accept()
        print(f'connection from {client_address}')
        return connection, client_address
        

#RequestHandler:
#受信したリクエストの解析、適切なレスポンスの生成を担当。
class DataHandler:
    def __init__(self,connection):
        self.connection = connection
    
    def handle_data(self):
        data = self.connection.recv(1024)
        data_str = data.decode('utf-8')
        print(f'Received data: {data_str}')

        response = 'Processing ' + data_str
        return response
#ResponseSender
#生成されたレスポンスをクライアントに送信することを担当。

class ResponseSender:
    def __init__(self, connection, response):
        self.connection = connection
        self.response = response

    def send_response(self):
        self.connection.sendall(self.response.encode())
        self.connection.close()

def main():
    host = '127.0.0.1'
    port = 8080
    socket_manager = SocketManager(host, port)
    socket_manager.bind_and_listen()

    while True:
        connection, client_address = socket_manager.accept_connection()
        request_handler = DataHandler(connection)
        response = request_handler.handle_data()
        response_sender = ResponseSender(connection, response)
        response_sender.send_response()

if __name__ == "__main__":
    main()
