import network
import machine


class WifiClient:
    def __init__(self, wifi_ssid, wifi_password):
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password

    def start(self):
        try:
            if not self.wifi.isconnected():
                self.try_connecting()
            print("network config:", self.wifi.ifconfig())
        except OSError as error:
            print(error)
            machine.reset()

    def try_connecting(self):
        print("connecting to network...")
        self.wifi.active(True)
        self.wifi.connect(self.wifi_ssid, self.wifi_password)
        while not self.wifi.isconnected():
            pass
