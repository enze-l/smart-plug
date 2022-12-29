from _thread import start_new_thread
import time
import socket

connections = []
message = "get_state"


def connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("0.0.0.0", 8080))
        while True:
            server_socket.listen()
            connection, address = server_socket.accept()
            connections.append(connection)
            print(str(address) + " connected")
            start_new_thread(receive, (connection,))


def receive(connection):
    while connection in connections:
        data = connection.recv(1024)
        answer = str(data, "utf8")
        if answer != "":
            print("This is an answer:" + answer)
        else:
            close_connection(connection)
            print("connection timed out")


def send():
    while True:
        time.sleep(1)
        print(message)
        for connection in connections:
            try:
                connection.sendall(message.encode("utf-8"))
            except (BrokenPipeError, ConnectionResetError):
                close_connection(connection)
                print("request timed out")


def close_connection(connection):
    connections.remove(connection)
    connection.close()


start_new_thread(connect, ())
send()
