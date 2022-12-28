import socket
import uasyncio
import machine
from ..abstract_api import AbstractAPI
from .api_config import SERVER_IP_ADDRESS


class API(AbstractAPI):
    def __init__(self, hardware):
        self.hardware = hardware
        self.connected = False
        self.socket = socket.socket()

    def start(self):
        while True:
            while not self.connected:
                try:
                    self.socket.connect((SERVER_IP_ADDRESS, 8080))
                    self.connected = True
                    print("connected")
                except OSError:
                    print("trying to connect again is 1 second ...")
                    await uasyncio.sleep(1)
                    self.socket.close()
                    self.socket = socket.socket()
            while self.connected:
                data = self.socket.recv(1024)
                message = str(data, "utf8")
                if len(message) == 0:
                    self.connected = False
                else:
                    print(message)



    def stop(self):
        pass
