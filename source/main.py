from config.config import WIFI_SSID, WIFI_PASSWORD
from networking.wifi_client import WifiClient
from networking import ntp_time

wifi_client = WifiClient(WIFI_SSID, WIFI_PASSWORD)
wifi_client.start()
ntp_time.adjust_own_time()
