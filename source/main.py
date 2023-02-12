import uasyncio
from config.config_manager import ConfigManager, STANDARD_CONFIG_FILE_PATH
from networking.wifi_client import WifiClient
from networking import ntp_time
from hardware import hardware
from api.api_controller import APIController


def setup():
    config = ConfigManager(STANDARD_CONFIG_FILE_PATH)
    wifi_ssid = config.get_value("WIFI_SSID")
    wifi_password = config.get_value("WIFI_PASSWORD")
    wifi_client = WifiClient(wifi_ssid, wifi_password)
    wifi_client.start()
    ntp_time.adjust_own_time()


setup()
event_loop = uasyncio.get_event_loop()
api_controller = APIController(hardware)
event_loop.create_task(api_controller.start_api())
event_loop.create_task(api_controller.serve_ui())
event_loop.run_forever()
