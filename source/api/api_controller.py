import uasyncio
import _thread
import socket


class APIController:
    def __init__(self, hardware):
        self.hardware = hardware
        self.current_api_name = "websocket"
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
        print("Hello before")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", 80))
        server_socket.listen()
        while True:
            connection, address = server_socket.accept()
            request = connection.recv(1024)
            print(str(request))
            connection.sendall(self.html())
            connection.close()
            print("connection closed")

    def html(self):
        api_options = self.__get_api_option()

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
            <form action="/set-api">
                <select name="api" id="api">""" + api_options + """</select>
                <input type="submit" value="Submit">
            </form>
          </body>
        </html>"""

    def __get_api_option(self):
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
