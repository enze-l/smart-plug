import uasyncio
from config.config import API_NAME


class APIController:
    def __init__(self, hardware):
        api = __import__("api." + API_NAME + ".api", globals(), locals(), [], 0)
        self.api = api.API(hardware)

    def start(self):
        event_loop = uasyncio.get_event_loop()
        event_loop.create_task(self.api.start())
        event_loop.run_forever()

    def stop(self):
        self.api.stop()
