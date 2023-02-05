import sys
sys.path.append("source")  # noqa: E402

import network
import machine
from config.config_manager import ConfigManager, STANDARD_CONFIG_FILE_PATH


class WifiClient:
    def __init__(self, wifi_ssid, wifi_password):
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password
        self.config = ConfigManager(STANDARD_CONFIG_FILE_PATH)

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
        self.wifi.config(dhcp_hostname=self.config.get_value("SMART_PLUG_NAME"))
        self.wifi.connect(self.wifi_ssid, self.wifi_password)
        while not self.wifi.isconnected():
            pass
