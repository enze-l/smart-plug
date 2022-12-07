import unittest
from source.networking.wifi_client import WifiClient
from unittest.mock import patch


class TestWifi(unittest.TestCase):
    def setUp(self):
        self.sample_ssid = "sample_ssid"
        self.sample_password = "sample_password"

    @patch('source.networking.wifi_client.network.WLAN')
    def test_wifi_should_establish_connection(self, wifi):
        wifi_client = WifiClient(self.sample_ssid, self.sample_password)

        wifi_client._WifiClient__establish_connection()

        wifi().active.assert_called_once_with(True)
        wifi().connect.assert_called_once_with(self.sample_ssid, self.sample_password)
        wifi().isconnected.assert_called_once()

    @patch('source.networking.wifi_client.network.WLAN')
    def test_wifi_should_establish_connection_after_retries(self, wifi):
        wifi_client = WifiClient(self.sample_ssid, self.sample_password)
        wifi().isconnected.side_effect = [False, False, True]

        wifi_client._WifiClient__establish_connection()

        wifi().active.assert_called_once_with(True)
        wifi().connect.assert_called_once_with(self.sample_ssid, self.sample_password)
        assert(wifi().isconnected.call_count == 3)

    def test_wifi_should_start(self):
        wifi = WifiClient(self.sample_ssid, self.sample_password)
        wifi.start()

if __name__ == "__main__":
    unittest.main()
