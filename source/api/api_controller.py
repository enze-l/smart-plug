import uasyncio
import _thread
import socket


class APIController:
    def __init__(self, hardware):
        self.hardware = hardware
        self.current_api_name = "awattar"
        self.__set_api(self.current_api_name)

    def __set_api(self, api_name):
        api = __import__("api." + api_name + ".api", globals(), locals(), [], 0)
        self.api = api.API(self.hardware)

    def start(self):
        event_loop = uasyncio.get_event_loop()
        event_loop.create_task(self.api.start())
        _thread.start_new_thread(self.__serve_ui, ())
        event_loop.run_forever()

    def __serve_ui(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(("0.0.0.0", 80))
            server_socket.listen()
            while True:
                self.__accept_requests(server_socket)
        except OSError:
            print("something went wrong")
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
        print("connection closed")

    def __extract_and_set_api(self, api_arg_string):
        api_name = api_arg_string.split("=")[1]
        if api_name != self.current_api_name:
            self.api.stop()
            self.__set_api(api_name)
            event_loop = uasyncio.get_event_loop()
            event_loop.create_task(self.api.start())

    def html(self):
        return """
        <html>
          <head>
            <title>Smart-Plug</title>
            <style>
                html { text-align: center; }
            </style>
          </head>
          <body>
            <label for="api">Chose an api</label>
            <form>
                <select name="api" id="api">""" + self.__get_api_html_options() + """</select>
                <input type="submit" value="Submit">
            </form>
          </body>
        </html>"""

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
        return "<option " + selected_placeholder + "value=\"" + name + "\">" + name + "</option>"

    def stop(self):
        self.api.stop()
