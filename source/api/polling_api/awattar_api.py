import urequests
import time


class AwattarApi:
    def __init__(self, hardware):
        self.relay = hardware.relay
        self.url = "https://api.awattar.de/v1/marketdata"

    def start(self):
        self.__loop_get_prices()
        print("scheduled")

    def stop(self):
        pass

    def __loop_get_prices(self):
        while True:
            time.sleep(3)
            self.__get_prices()

    def __get_prices(self):
        res = urequests.get("https://api.awattar.de/v1/marketdata")
        secs_since_2000 = time.time()
        utc_secs_till_2000 = 946681200
        print(res.text)
        print(utc_secs_till_2000 + secs_since_2000)
