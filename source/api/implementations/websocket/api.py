import socket
import uasyncio
from api.abstract_api import AbstractAPI
from .api_config import (
    SERVER_ADDRESS,
    SERVER_PORT,
    SERVER_CONNECTION_RETRY_TIME_SECONDS,
    UI_INTERFACE_PORT,
)


class API(AbstractAPI):
    def get_html_options(self):
        return """
        <iframe name="dummyframe" id="dummyframe" style="display: none;"></iframe>
        <form method="post" action="http://{}:{}" target="dummyframe">
            <input name="server_address" required value={}>
            <input type="submit" value="Set Server Address">
        </form>
        <p> setting a non existent server will lead to lagging
        """.format(
            self.ip_address, UI_INTERFACE_PORT, self.server_address
        )

    def __init__(self, hardware):
        self.relay = hardware.relay_with_led
        self.button = hardware.button_external
        self.ip_address = hardware.get_ip_address()
        self.server_address = SERVER_ADDRESS
        self.connected = False
        self.socket = None
        self.is_running = False
        self.handle_message_task = None
        self.handle_connect_task = None

    async def start(self):
        self.__set_is_running(True)
        self.__set_button_behaviour()
        uasyncio.create_task(self.__poll_interface_port())
        while self.__get_is_running():
            await self.__establish_connection()
        self.socket.close()

    async def __poll_interface_port(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setblocking(False)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", UI_INTERFACE_PORT))
        server_socket.listen()
        while self.__get_is_running():
            try:
                self.__accept_requests(server_socket)
            except OSError:
                pass
            await uasyncio.sleep(0)
        server_socket.close()

    def __accept_requests(self, server_socket):
        connection, address = server_socket.accept()
        request = str(connection.recv(1024))
        server_address_request = request.split("server_address=")
        if len(server_address_request) > 1:
            self.server_address = server_address_request[1].replace("'", "")
            print("Server address set to " + self.server_address)

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

    async def __establish_connection(self):
        while not self.connected and self.__get_is_running():
            self.handle_connect_task = uasyncio.create_task(self.__connect())
            await self.handle_connect_task
        while self.connected and self.__get_is_running():
            self.handle_message_task = uasyncio.create_task(self.__get_message())
            await self.handle_message_task

    async def __connect(self):
        try:
            print("trying to connect to " + self.server_address)
            self.socket = socket.socket()
            server_address = socket.getaddrinfo(self.server_address, SERVER_PORT)[0][-1]
            self.socket.connect(server_address)
            self.connected = True
            print("connected to server")
        except OSError:
            self.socket.close()
            print(
                """trying to connect to server again in {} second ...""".format(
                    int(SERVER_CONNECTION_RETRY_TIME_SECONDS)
                )
            )
            await uasyncio.sleep(SERVER_CONNECTION_RETRY_TIME_SECONDS)

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
