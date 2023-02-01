import gc
import urequests
import time
import uasyncio
from .api_config import TURN_ON_THRESHOLD_EUR
from ..abstract_api import AbstractAPI

# micropython measure time with seconds since th 1.1.2000
# to convert this time to utc this variable serves as a reference
utc_secs_till_2000 = 946684800


class API(AbstractAPI):
    def __init__(self, hardware):
        self.relay = hardware.relay
        self.button = hardware.button_external
        self.url = "https://api.awattar.de/v1/marketdata"
        self.is_running = False
        self.tasks = []
        self.price_threshold_eur = TURN_ON_THRESHOLD_EUR
        self.automation_overriden = False

    async def start(self):
        self.__set_is_running(True)
        self.__set_button_behaviour()
        while self.__get_is_running():
            self.__cancel_all_tasks()
            await self.__poll_api()
            twelve_hours_in_seconds = 12 * 60 * 60
            await uasyncio.sleep(twelve_hours_in_seconds)

    def stop(self):
        self.__set_is_running(False)
        self.__cancel_all_tasks()
        self.button.reset_functions()

    def __cancel_all_tasks(self):
        for task in self.tasks:
            task.cancel()
        self.tasks.clear()
        gc.collect()

    def __get_is_running(self):
        return self.is_running

    def __set_is_running(self, is_running):
        self.is_running = is_running

    def __execute_button_behaviour(self):
        self.relay.toggle()
        self.automation_overriden = True

    def __set_button_behaviour(self):
        self.button.set_on_toggle_function(self.__execute_button_behaviour)

    async def __poll_api(self, time_delay=0):
        await uasyncio.sleep(time_delay)
        res = urequests.get(self.url)
        if res.status_code == 200:
            self.__process_price_changes(res.json()["data"])
        else:
            uasyncio.create_task(self.__poll_api(3))

    def __process_price_changes(self, data):
        for interval in data:
            start_time_sec_esp_utc = int(
                interval["start_timestamp"] / 1000 - utc_secs_till_2000
            )
            self.__schedule_price_change_reaction(
                start_time_sec_esp_utc, interval["marketprice"]
            )

    def __schedule_price_change_reaction(self, start_timestamp, price):
        current_time = time.time()
        time_till_execution = start_timestamp - current_time
        task = uasyncio.create_task(
            self.__react_to_price_change(time_till_execution, price)
        )
        self.tasks.append(task)

    async def __react_to_price_change(self, time_till_execution, price):
        await uasyncio.sleep(time_till_execution)
        print("Executed time: " + str(time_till_execution))
        if price <= self.price_threshold_eur:
            self.__toggle_relay_if_appropriate(True)
        else:
            self.__toggle_relay_if_appropriate(False)

    def __toggle_relay_if_appropriate(self, new_state):
        automation_override_should_be_reset = new_state == self.relay.get_on_state()
        if automation_override_should_be_reset:
            self.automation_overriden = False
        if not self.automation_overriden:
            self.relay.set_on_state(new_state)
