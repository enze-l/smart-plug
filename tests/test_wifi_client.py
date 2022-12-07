import unittest
from source.networking.wifi_client import WifiClient
from unittest.mock import patch


class TestWifi(unittest.TestCase):
    def setUp(self):
        self.sample_ssid = "sample_ssid"
        self.sample_password = "sample_password"

    def test_wifi_should_start(self):
        wifi = WifiClient(self.sample_ssid, self.sample_password)
        wifi.start()

    @patch('source.networking.wifi_client.network')
    def test_wifi_should_establish_connection(self, network):
        wifi_client = WifiClient(self.sample_ssid, self.sample_password)

        wifi_client._WifiClient__establish_connection()

        network.WLAN().active.assert_called_once()
        network.WLAN().connect.assert_called_once()
        network.WLAN().isconnected.assert_called_once()


if __name__ == "__main__":
    unittest.main()
