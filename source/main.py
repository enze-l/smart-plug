import uasyncio
from config.config import WIFI_SSID, WIFI_PASSWORD
from networking.wifi_client import WifiClient
from networking import ntp_time
from hardware import hardware
from api.api_controller import APIController


def setup():
    wifi_client = WifiClient(WIFI_SSID, WIFI_PASSWORD)
    wifi_client.start()
    ntp_time.adjust_own_time()


async def run_api():
    api_controller = APIController(hardware)
    uasyncio.create_task(api_controller.start_api())
    print("API started")
    while True:
        await uasyncio.sleep(10)
        print("should change api to awattar")
        uasyncio.create_task(api_controller.change_api("awattar"))
        await uasyncio.sleep(10)
        print("should chang api to websocket")
        uasyncio.create_task(api_controller.change_api("websocket"))


setup()
event_loop = uasyncio.get_event_loop()
event_loop.create_task(run_api())
event_loop.run_forever()
