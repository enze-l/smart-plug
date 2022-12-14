from config.config import WIFI_SSID, WIFI_PASSWORD
from networking.wifi_client import WifiClient
import hardware.hardware as hardware

wifi_client = WifiClient(WIFI_SSID, WIFI_PASSWORD)
wifi_client.start()

hardware.button_internal.set_on_release_function(hardware.led.turn_off)
hardware.button_internal.set_on_click_function(hardware.led.turn_on)
hardware.button_internal.set_on_toggle_function(hardware.led.get_on_state)
