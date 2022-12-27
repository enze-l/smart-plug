import time
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen()
    connection, address = server_socket.accept()
    with connection:
        print(f"Connected by {address}")
        while True:
            time.sleep(1)
            connection.sendall(b"Hello\n")
            print("Hello")
