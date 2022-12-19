import urequests
import time
import uasyncio
from micropython import const
from .awattar_config import TURN_ON_THRESHOLD_EUR

# micropython measure time with seconds since th 1.1.2000
# to convert this time to utc this variable serves as a reference
utc_secs_till_2000 = const(946684800)


class AwattarApi:
    def __init__(self, hardware):
        self.relay = hardware.relay
        self.url = "https://api.awattar.de/v1/marketdata"
        self.is_running = False
        self.tasks = []
        self.price_threshold_eur = TURN_ON_THRESHOLD_EUR

    def start(self):
        self.is_running = True
        while self.is_running:
            self.__cancel_all_tasks()
            self.__poll_api()
            twelve_hours_in_seconds = 12 * 60 * 60
            await uasyncio.sleep(twelve_hours_in_seconds)

    def __poll_api(self):
        res = urequests.get(self.url)
        data = res.json()["data"]
        for interval in data:
            start_time = int(interval["start_timestamp"] / 1000 - utc_secs_till_2000)
            self.__create_scheduled_task(start_time, interval["marketprice"])

    def __create_scheduled_task(self, start_timestamp, price):
        current_time = time.time()
        time_till_execution = start_timestamp - current_time
        print(time_till_execution)
        task = uasyncio.create_task(self.__react_to_price_change(price, time_till_execution))
        self.tasks.append(task)

    def __react_to_price_change(self, price, time_till_execution):
        await uasyncio.sleep(time_till_execution)
        print("Executed time: " + str(time_till_execution))
        if price < self.price_threshold_eur:
            self.relay.turn_on()

    def stop(self):
        print("tasks canceled")
        self.is_running = False
        self.__cancel_all_tasks()

    def __cancel_all_tasks(self):
        for task in self.tasks:
            task.cancel()
