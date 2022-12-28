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
        self.handle_message_task = None
        self.connect_task = None

    def start(self):
        self.running = True
        while self.running:
            await self.__init_connection()
        self.socket.close()

    def stop(self):
        self.running = False
        self.connected = False
        if self.handle_message_task:
            self.handle_message_task.cancel()
        if self.connect_task:
            self.connect_task.cancel()
        print("api stopped")

    async def __init_connection(self):
        while not self.connected:
            self.connect_task = uasyncio.create_task(self.__connect())
            await self.connect_task
        while self.connected:
            self.handle_message_task = uasyncio.create_task(self.__get_message())
            await self.handle_message_task

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

    async def __get_message(self):
        data = self.socket.recv(1024)
        message = str(data, "utf8")
        if len(message) == 0:
            self.connected = False
        else:
            self.__process_message(message)

    def __process_message(self, message):
        print(message)
        led = self.hardware.led
        if message == "turn_on":
            led.turn_on()
        elif message == "turn_off":
            led.turn_on()
        elif message == "toggle":
            led.toggle()
        else:
            print("Message not recognized")

