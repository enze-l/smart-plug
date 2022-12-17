import urequests
import time
import uasyncio


class AwattarApi:
    def __init__(self, hardware):
        self.relay = hardware.relay
        self.url = "https://api.awattar.de/v1/marketdata"

    def start(self):
        while True:
            self.__get_api()
            await uasyncio.sleep(3)
    
    def __get_api(self):
        res = urequests.get(self.url)
        secs_since_2000 = time.time()
        utc_secs_till_2000 = 946681200
        response_text = res.text
        print(utc_secs_till_2000 + secs_since_2000)

    def stop(self):
        pass
