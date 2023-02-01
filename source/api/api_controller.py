import gc
import uasyncio
import socket
from config.config import API_NAME


class APIController:
    def __init__(self, hardware):
        self.hardware = hardware
        self.api_cash_dict = {}
        self.current_api_name = API_NAME
        self.api = None
        self.__load_api(self.current_api_name)

    def __import_api(self, api_name):
        api = __import__("api." + api_name + ".api", globals(), locals(), [], 0)
        self.api = api.API(self.hardware)
        self.api_cash_dict[api_name] = self.api

    def __load_api(self, api_name):
        if api_name in self.api_cash_dict:
            print("api loaded from cash")
            self.api = self.api_cash_dict[api_name]
        else:
            print("api loaded from memory")
            self.__import_api(api_name)
        self.current_api_name = api_name
        gc.collect()

    async def start_api(self):
        await self.api.start()

    def stop_api(self):
        self.api.stop()

    async def change_api(self, api_name):
        self.stop_api()
        self.__load_api(api_name)
        await self.start_api()

    async def serve_ui(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setblocking(False)
        try:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(("0.0.0.0", 80))
            server_socket.listen()
            while True:
                try:
                    self.__accept_requests(server_socket)
                except OSError as e:
                    pass
                await uasyncio.sleep(0)
        except OSError as e:
            print("something went wrong")
            print(e)
            server_socket.close()

    def __accept_requests(self, server_socket):
        connection, address = server_socket.accept()
        request = str(connection.recv(1024))
        request_parameters = request.split(" ")
        for parameter in request_parameters:
            if parameter.startswith("/?api"):
                self.__extract_and_set_api(parameter)
        connection.sendall(self.html())
        connection.close()
        print("request processed")

    def __extract_and_set_api(self, api_arg_string):
        api_name = api_arg_string.split("=")[1]
        if api_name != self.current_api_name:
            self.api.stop()
            self.__load_api(api_name)
            event_loop = uasyncio.get_event_loop()
            event_loop.create_task(self.api.start())

    def html(self):
        return """
            <html>
              <head>
                <title>Smart-Plug</title>
                <style>
                    html {{ text-align: center; }}
                </style>
              </head>
              <body>
                <label for="api">Chose an api</label>
                <form>
                    <select name="api" id="api">{0}</select>
                    <input type="submit" value="Set API">
                </form>
                {1}
              </body>
            </html>""".format(
            self.__get_api_html_options(), self.api.get_html_options()
        )

    def __get_api_html_options(self):
        options = ["awattar", "websocket"]
        html_options = ""
        for option in options:
            html_options = html_options + self.__get_api_html_name(option)
        return html_options

    def __get_api_html_name(self, name):
        selected_placeholder = ""
        if name == self.current_api_name:
            selected_placeholder = """selected="selected" """
        return (
            "<option "
            + selected_placeholder
            + 'value="'
            + name
            + '">'
            + name
            + "</option>"
        )
