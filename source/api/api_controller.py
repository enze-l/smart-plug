import uasyncio


class APIController:
    def __init__(self, api):
        self.api = api

    def start(self):
        event_loop = uasyncio.get_event_loop()
        event_loop.create_task(self.api.start())
        event_loop.create_task(self.stop_countdown())
        event_loop.run_forever()

    def stop_countdown(self):
        await uasyncio.sleep(10)
        self.stop()

    def stop(self):
        self.api.stop()
