import socket
import uasyncio
from ..abstract_api import AbstractAPI
from .api_config import SERVER_IP_ADDRESS, SERVER_PORT


class API(AbstractAPI):
    def __init__(self, hardware):
        self.hardware = hardware
        self.connected = False
        self.socket = socket.socket()
        self.running = False

    def start(self):
        self.running = True
        while self.running:
            await self.__init_connection()
        self.socket.close()

    async def __init_connection(self):
        while not self.connected:
            await self.__connect()
        while self.connected:
            self.__handle_message()

    async def __connect(self):
        try:
            self.socket.connect((SERVER_IP_ADDRESS, SERVER_PORT))
            self.connected = True
            print("connected")
        except OSError:
            print("trying to connect again is 1 second ...")
            await uasyncio.sleep(1)
            self.socket.close()
            self.socket = socket.socket()

    def __handle_message(self):
        data = self.socket.recv(1024)
        message = str(data, "utf8")
        if len(message) == 0:
            self.connected = False
        else:
            print(message)

    def stop(self):
        pass
