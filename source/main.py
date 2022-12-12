from config.config import WIFI_SSID, WIFI_PASSWORD
from networking.wifi_client import WifiClient
import hardware.hardware as hardware
import time

wifi_client = WifiClient(WIFI_SSID, WIFI_PASSWORD)
wifi_client.start()

hardware.led.turn_on()
hardware.relay.turn_on()

while True:
    time.sleep(1)
    hardware.led.toggle()
    print(hardware.led.pin.value())
