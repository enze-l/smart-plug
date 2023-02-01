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


async def run_api_for_ten_seconds(api_controller, api_name):
    await uasyncio.sleep(10)
    uasyncio.create_task(api_controller.change_api(api_name))


setup()
event_loop = uasyncio.get_event_loop()
api_controller = APIController(hardware)
event_loop.create_task(api_controller.start_api())
event_loop.create_task(api_controller.serve_ui())
event_loop.run_forever()
