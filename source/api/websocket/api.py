import socket
import uasyncio
from ..abstract_api import AbstractAPI
from .api_config import SERVER_IP_ADDRESS, SERVER_PORT


class API(AbstractAPI):
    def __init__(self, hardware):
        self.hardware = hardware
        self.connected = False

    def start(self):
        client_socket = socket.socket()
        while not self.connected:
            try:
                client_socket.connect((SERVER_IP_ADDRESS, SERVER_PORT))
                self.connected = True
                print("connected")
            except OSError:
                print("trying to connect again is 1 second ...")
                await uasyncio.sleep(1)
        while True:
            data = client_socket.readline()
            print(data)

    def stop(self):
        pass
