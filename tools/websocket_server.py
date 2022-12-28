from _thread import start_new_thread
import time
import socket

connections = []


def connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("0.0.0.0", 8080))
        while True:
            server_socket.listen()
            connection, address = server_socket.accept()
            connections.append(connection)


def send():
    while True:
        for connection in connections:
            print("Connected")
            while True:
                time.sleep(1)
                print("Hello")
                connection.sendall(b"Hello\n")


start_new_thread(connect, ())
send()
