from config.config import WIFI_SSID, WIFI_PASSWORD
from networking.wifi_client import WifiClient
from hardware.led import Led
import time

wifi_client = WifiClient(WIFI_SSID, WIFI_PASSWORD)
wifi_client.start()

led = Led(True)
led.turn_on()
time.sleep(1)
led.turn_off()
time.sleep(1)
led.toggle_led()
time.sleep(1)
led.set_state(True)
print(led.get_state())

