from _thread import start_new_thread
import time
import socket

connections = []

message = "turn_off"

def connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("0.0.0.0", 8080))
        while True:
            server_socket.listen()
            connection, address = server_socket.accept()
            connections.append(connection)
            print(str(address) + " connected")


def send():
    while True:
        time.sleep(1)
        print(message)
        for connection in connections:
            try:
                connection.sendall(message.encode("utf-8"))
            except (BrokenPipeError, ConnectionResetError):
                connections.remove(connection)
                print("request timed out")


start_new_thread(connect, ())
send()
