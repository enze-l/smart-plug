import _thread

from config.config import API_NAME


class APIController:
    def __init__(self, hardware):
        api = __import__("api." + API_NAME + ".api", globals(), locals(), [], 0)
        self.api = api.API(hardware)

    def start(self):
        _thread.start_new_thread(self.api.start, ())

    def stop(self):
        self.api.stop()
