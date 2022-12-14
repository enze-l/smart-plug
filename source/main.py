from config.config import WIFI_SSID, WIFI_PASSWORD
from networking.wifi_client import WifiClient

wifi_client = WifiClient(WIFI_SSID, WIFI_PASSWORD)
wifi_client.start()

