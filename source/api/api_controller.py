import uasyncio


class APIController:
    def __init__(self, api):
        self.api = api

    def start(self):
        event_loop = uasyncio.get_event_loop()
        event_loop.create_task(self.api.start())
        event_loop.run_forever()

    def stop(self):
        self.api.stop()
