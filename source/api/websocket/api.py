import socket
import time
import _thread
from ..abstract_api import AbstractAPI
from .api_config import (
    SERVER_IP_ADDRESS,
    SERVER_PORT,
    SERVER_CONNECTION_RETRY_TIME_SECONDS,
)


class API(AbstractAPI):
    def __init__(self, hardware):
        self.connection_thread = None
        self.relay = hardware.relay_with_led
        self.button = hardware.button_external
        self.socket = None
        self.is_connected = False

    def start(self):
        self.__set_button_behaviour()
        self.connection_thread = _thread.start_new_thread(self.__run_api, ())

    def stop(self):
        self.button.reset_functions()
        self.connection_thread.exit()
        self.socket.close()
        print("api stopped")

    def get_is_connected(self):
        return self.is_connected

    def __set_button_behaviour(self):
        self.button.set_on_toggle_function(self.relay.toggle)

    def __run_api(self):
        self.socket = socket.socket()
        while True:
            self.__connect()
            self.__get_message()

    def __connect(self):
        print("Started")
        while not self.get_is_connected():
            try:
                self.socket.connect((SERVER_IP_ADDRESS, SERVER_PORT))
                self.is_connected = True
                print("connected to server")
            except OSError:
                print("trying to connect to server again in 1 second ...")
                time.sleep(SERVER_CONNECTION_RETRY_TIME_SECONDS)
                self.socket.close()
                self.socket = socket.socket()

    def __get_message(self):
        while self.get_is_connected():
            data = self.socket.recv(1024)
            message = str(data, "utf8")
            if len(message) == 0:
                self.is_connected = False
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
