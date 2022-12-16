import urequests
import time
import _thread


class AwattarApi:
    def __init__(self, hardware):
        self.relay = hardware.relay
        self.url = "https://api.awattar.de/v1/marketdata"

    def start(self):
        _thread.start_new_thread(self.__loop_get_prices, ())
        print("scheduled")

    def stop(self):
        pass

    def __loop_get_prices(self):
        while True:
            time.sleep(3)
            self.__get_prices()

    def __get_prices(self):
        res = urequests.get("https://api.awattar.de/v1/marketdata")
        print(res.text)
