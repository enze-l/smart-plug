from config.config import WIFI_SSID, WIFI_PASSWORD
import network
import machine


def start():
    wifi = network.WLAN(network.STA_IF)

    try:
        if not wifi.isconnected():
            print("connecting to network...")
            wifi.active(True)
            wifi.connect(WIFI_SSID, WIFI_PASSWORD)
            while not wifi.isconnected():
                pass
        print("network config:", wifi.ifconfig())
    except OSError as error:
        print(error)
        machine.reset()
