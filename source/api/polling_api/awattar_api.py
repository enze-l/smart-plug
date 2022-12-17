import urequests
import time
import uasyncio


class AwattarApi:
    def __init__(self, hardware):
        self.relay = hardware.relay
        self.url = "https://api.awattar.de/v1/marketdata"

    async def start(self):
        while True:
            res = urequests.get("https://api.awattar.de/v1/marketdata")
            secs_since_2000 = time.time()
            utc_secs_till_2000 = 946681200
            response_text = res.text
            print(utc_secs_till_2000 + secs_since_2000)
            await uasyncio.sleep(3)

    def stop(self):
        pass
