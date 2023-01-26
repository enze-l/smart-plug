import time

from config.config import WIFI_SSID, WIFI_PASSWORD
from networking.wifi_client import WifiClient
from networking import ntp_time
from hardware import hardware
from api.api_controller import APIController


def setup():
    wifi_client = WifiClient(WIFI_SSID, WIFI_PASSWORD)
    wifi_client.start()
    ntp_time.adjust_own_time()


def start_api():
    api_controller = APIController(hardware)
    api_controller.start()

    # only there to keep output going
    while True:
        time.sleep(60)


setup()
start_api()
