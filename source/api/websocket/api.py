import socket
import uasyncio
from ..abstract_api import AbstractAPI
from .api_config import SERVER_IP_ADDRESS, SERVER_PORT, SERVER_CONNECTION_RETRY_TIME_SECONDS


class API(AbstractAPI):
    def __init__(self, hardware):
        self.relay = hardware.relay_with_led
        self.button = hardware.button_external
        self.connected = False
        self.socket = None
        self.is_running = False
        self.handle_message_task = None
        self.handle_connect_task = None

    async def start(self):
        self.__set_is_running(True)
        self.__set_button_behaviour()
        while self.__get_is_running():
            await self.__init_connection()
        self.socket.close()

    def stop(self):
        self.button.reset_functions()
        self.__set_is_running(False)
        self.connected = False
        if self.handle_message_task:
            self.handle_message_task.cancel()
        if self.handle_connect_task:
            self.handle_connect_task.cancel()
        print("api stopped")

    def __get_is_running(self):
        return self.is_running

    def __set_is_running(self, is_running):
        self.is_running = is_running

    def __set_button_behaviour(self):
        self.button.set_on_toggle_function(self.relay.toggle)

    async def __init_connection(self):
        self.socket = socket.socket()
        while not self.connected:
            self.handle_connect_task = uasyncio.create_task(self.__connect())
            await self.handle_connect_task
        while self.connected:
            self.handle_message_task = uasyncio.create_task(self.__get_message())
            await self.handle_message_task

    async def __connect(self):
        try:
            self.socket.connect((SERVER_IP_ADDRESS, SERVER_PORT))
            self.connected = True
            print("connected to server")
        except OSError:
            retry_time_string = str(SERVER_CONNECTION_RETRY_TIME_SECONDS)
            print(
                "trying to connect to server again in "
                + retry_time_string
                + " second ..."
            )
            await uasyncio.sleep(SERVER_CONNECTION_RETRY_TIME_SECONDS)
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
        if message == "turn_on":
            self.relay.turn_on()
        elif message == "turn_off":
            self.relay.turn_off()
        elif message == "toggle":
            self.relay.toggle()
        elif message == "get_state":
            self.socket.sendall(self.relay.get_on_state_string())
        else:
            print("Command not recognized")
