import gc
import socket
import urequests
import time
import uasyncio
from config.config_manager import ConfigManager
from api.abstract_api import AbstractAPI

# micropython measure time with seconds since th 1.1.2000
# to convert this time to utc this variable serves as a reference
utc_secs_till_2000 = 946684800


class API(AbstractAPI):
    def get_html_options(self):
        return """
        <iframe name="dummyframe" id="dummyframe" style="display: none;"></iframe>
        <form method="post" action="http://{}:{}" target="dummyframe">
            <input name="toggle_threshold" type="number" required value={}>
            <input type="submit" value="Set price Euro/MWh">
        </form>""".format(
            self.ip_address,
            self.config.get_value("UI_INTERFACE_PORT"),
            self.price_threshold_eur,
        )

    def __init__(self, hardware):
        self.config = ConfigManager("/api/implementations/awattar/api_config.json")
        self.relay = hardware.relay_with_led
        self.button = hardware.button_external
        self.ip_address = hardware.get_ip_address()
        self.url = self.config.get_value("API_PROVIDER_URL")
        self.is_running = False
        self.tasks = []
        self.price_threshold_eur = self.config.get_value("TURN_ON_THRESHOLD_EUR")
        self.automation_overriden = False

    async def start(self):
        self.__set_is_running(True)
        self.__set_button_behaviour()
        uasyncio.create_task(self.__poll_interface_port())
        while self.__get_is_running():
            self.__cancel_all_tasks()
            await self.__poll_api()
            nine_hours_in_seconds = 9 * 60 * 60
            await uasyncio.sleep(nine_hours_in_seconds)

    async def __poll_interface_port(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setblocking(False)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", self.config.get_value("UI_INTERFACE_PORT")))
        server_socket.listen()
        while self.__get_is_running():
            try:
                self.__accept_requests(server_socket)
            except OSError:
                pass
            await uasyncio.sleep(0)
        server_socket.close()

    def __accept_requests(self, server_socket):
        connection, address = server_socket.accept()
        request = str(connection.recv(1024))
        threshold_substring = request.split("toggle_threshold=")
        if len(threshold_substring) > 1:
            price_threshold_string = threshold_substring[1].replace("'", "")
            self.price_threshold_eur = int(price_threshold_string)
            self.config.set_value("TURN_ON_THRESHOLD_EUR", self.price_threshold_eur)
            print("Threshold set to " + price_threshold_string)
            self.__cancel_all_tasks()
            uasyncio.create_task(self.__poll_api())

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
