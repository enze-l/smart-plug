import uasyncio
import _thread
import socket
from config.config import API_NAME


class APIController:
    def __init__(self, hardware):
        api = __import__("api." + API_NAME + ".api", globals(), locals(), [], 0)
        self.api = api.API(hardware)

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
                <select name="api" id="api">
                    <option value="awattar">Awattar</option>
                    <option value="websocket">Websocket</option>
                </select>
                <input type="submit" value="Submit">
            </form>
          </body>
        </html>"""

    def stop(self):
        self.api.stop()
