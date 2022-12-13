from config.config import WIFI_SSID, WIFI_PASSWORD
from networking.wifi_client import WifiClient
import hardware.hardware as hardware

wifi_client = WifiClient(WIFI_SSID, WIFI_PASSWORD)
wifi_client.start()


hardware.button.set_on_toggle_function(hardware.led.toggle)
