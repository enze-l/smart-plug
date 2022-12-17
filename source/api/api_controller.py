import uasyncio


class APIController:
    def __init__(self, api):
        self.api = api

    def start(self):
        event_loop = uasyncio.get_event_loop()
        event_loop.create_task(self.api.start())
        event_loop.create_task(self.count_loop())
        event_loop.run_forever()

    def count_loop(self):
        counter = 0
        while True:
            counter = counter + 1
            print("counter: " + str(counter))
            await uasyncio.sleep(1)

    def stop(self):
        self.api.stop()
