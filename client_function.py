import socket
import json

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.host, self.port))
        print(f'Connected to {self.host}:{self.port}')

    def send_request(self, function_name, params):
        request = {
            'function': function_name,
            'params': params
        }
        self.sock.sendall(json.dumps(request).encode('utf-8'))
        
        response = self.sock.recv(1024).decode('utf-8')
        print(f'Received: {response}')
        return json.loads(response)

    def close(self):
        self.sock.close()
        print('Connection closed')

def main():
    host = '127.0.0.1'
    port = 8080
    client = Client(host, port)
    
    try:
        client.connect()
        
        while True:
            function_name = input('Enter function name (or "exit" to quit): ')
            if function_name.lower() == 'exit':
                break
            params = input('Enter parameters (comma separated): ').split(',')
            # パラメータを適切な型に変換
            params = [int(p) if p.isdigit() else float(p) if '.' in p else p for p in params]
            
            client.send_request(function_name, params)
            
    finally:
        client.close()

if __name__ == "__main__":
    main()
