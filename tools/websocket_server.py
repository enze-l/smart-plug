from _thread import start_new_thread
import time
import socket
from websocket_config import WEBSOCKET_PORT

clients = []
message = "get_state"


def connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("0.0.0.0", WEBSOCKET_PORT))
        while True:
            server_socket.listen()
            connection, address = server_socket.accept()
            clients.append((connection, address))
            print(str(address) + " connected")
            start_new_thread(receive, ((connection, address),))


def receive(client):
    while client in clients:
        data = client[0].recv(1024)
        answer = str(data, "utf8")
        if answer != "":
            print(str(client[1]) + " is " + answer)
        else:
            disconnect_client(client)
            print("connection timed out")


def send():
    while True:
        time.sleep(1)
        print(message)
        for client in clients:
            try:
                client[0].sendall(message.encode("utf-8"))
            except (BrokenPipeError, ConnectionResetError):
                disconnect_client(client)
                print("request timed out")


def disconnect_client(client):
    clients.remove(client)
    client[0].close()


start_new_thread(connect, ())
send()
