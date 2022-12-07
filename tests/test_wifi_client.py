import unittest
from source.networking.wifi_client import WifiClient
from unittest.mock import patch, MagicMock


class TestWifi(unittest.TestCase):
    def setUp(self):
        self.sample_ssid = "sample_ssid"
        self.sample_password = "sample_password"

    @patch('source.networking.wifi_client.network.WLAN')
    def test_wifi_should_establish_connection(self, wifi):
        wifi_client = WifiClient(self.sample_ssid, self.sample_password)

        wifi_client.try_connecting()

        wifi().active.assert_called_once_with(True)
        wifi().connect.assert_called_once_with(self.sample_ssid, self.sample_password)
        wifi().isconnected.assert_called_once()

    @patch('source.networking.wifi_client.network.WLAN')
    def test_wifi_should_establish_connection_after_retries(self, wifi):
        wifi_client = WifiClient(self.sample_ssid, self.sample_password)
        wifi().isconnected.side_effect = [False, False, True]

        wifi_client.try_connecting()

        wifi().active.assert_called_once_with(True)
        wifi().connect.assert_called_once_with(self.sample_ssid, self.sample_password)
        assert(wifi().isconnected.call_count == 3)

    @patch('source.networking.wifi_client.network.WLAN')
    def test_wifi_should_start(self, wifi):
        wifi_client = WifiClient(self.sample_ssid, self.sample_password)
        wifi().isconnected = MagicMock(return_value=False)
        wifi_client.try_connecting = MagicMock()

        wifi_client.start()

        wifi_client.try_connecting.assert_called_once()
        wifi().isconnected.assert_called_once()


if __name__ == "__main__":
    unittest.main()
