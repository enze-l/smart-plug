import urequests
import time
import uasyncio
from micropython import const

utc_secs_till_2000 = const(946681200)


class AwattarApi:
    def __init__(self, hardware):
        self.relay = hardware.relay
        self.url = "https://api.awattar.de/v1/marketdata"
        self.is_running = False

    def start(self):
        self.is_running = True
        while self.is_running:
            self.__get_api()
            await uasyncio.sleep(3)

    def __get_api(self):
        res = urequests.get(self.url)
        data = res.json()["data"]
        print(time.time())
        for interval in data:
            start_time = int(interval["start_timestamp"] / 1000 - utc_secs_till_2000)
            print("Price: " + str(interval["marketprice"]) + " - " + str(start_time))

    def stop(self):
        self.is_running = False
        pass
