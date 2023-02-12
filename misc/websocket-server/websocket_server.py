from _thread import start_new_thread
import time
import socket
from websocket_config import (
    WEBSOCKET_PORT,
    WEBSOCKET_CONCATENATED_COMMANDS,
    WEBSOCKET_COMMAND_INTERVALL_SECONDS,
)


class WebsocketServer:
    def __init__(self):
        self.clients = []
        self.all_messages = WEBSOCKET_CONCATENATED_COMMANDS
        self.running = False

    def start(self):
        self.running = True
        start_new_thread(self.connect, ())
        self.send()

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(("0.0.0.0", WEBSOCKET_PORT))
            while self.running:
                server_socket.listen()
                connection, address = server_socket.accept()
                self.clients.append((connection, address))
                print(str(address) + " connected")
                start_new_thread(self.receive, ((connection, address),))

    def receive(self, client):
        while client in self.clients:
            data = client[0].recv(1024)
            answer = str(data, "utf8")
            if answer != "":
                print(str(client[1]) + " is " + answer)
            else:
                self.disconnect_client(client)
                print("connection timed out")

    def send(self):
        for message in self.all_messages.splitlines():
            time.sleep(WEBSOCKET_COMMAND_INTERVALL_SECONDS)
            print(message)
            for client in self.clients:
                try:
                    client[0].sendall(message.encode("utf-8"))
                except (BrokenPipeError, ConnectionResetError):
                    self.disconnect_client(client)
                    print("request timed out")
        self.running = False

    def disconnect_client(self, client):
        self.clients.remove(client)
        client[0].close()


websocket_server = WebsocketServer()
websocket_server.start()
