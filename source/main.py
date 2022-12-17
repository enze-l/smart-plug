from config.config import WIFI_SSID, WIFI_PASSWORD
from networking.wifi_client import WifiClient
from networking import ntp_time
from api.polling_api.awattar_api import AwattarApi
from hardware import hardware
from api.api_controller import APIController


def setup():
    wifi_client = WifiClient(WIFI_SSID, WIFI_PASSWORD)
    wifi_client.start()
    ntp_time.adjust_own_time()


def start_api():
    polling_api = AwattarApi(hardware)
    api_controller = APIController(polling_api)
    api_controller.start()


setup()
start_api()
