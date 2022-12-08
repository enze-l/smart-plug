import unittest
from source.networking.wifi_client import WifiClient
from unittest.mock import patch, Mock


class TestWifi(unittest.TestCase):
    def setUp(self):
        self.sample_ssid = "sample_ssid"
        self.sample_password = "sample_password"
        self.host_name = "Micro-Plug"

    @patch("source.networking.wifi_client.network.WLAN")
    def test_wifi_should_connect(self, wifi):
        wifi_client = WifiClient(self.sample_ssid, self.sample_password)

        wifi_client.try_connecting()

        wifi().active.assert_called_once_with(True)
        wifi().config.assert_called_once_with(dhcp_hostname=self.host_name)
        wifi().connect.assert_called_once_with(self.sample_ssid, self.sample_password)
        wifi().isconnected.assert_called_once()

    @patch("source.networking.wifi_client.network.WLAN")
    def test_wifi_should_connect_after_retries(self, wifi):
        wifi_client = WifiClient(self.sample_ssid, self.sample_password)
        wifi().isconnected.side_effect = [False, False, True]

        wifi_client.try_connecting()

        wifi().active.assert_called_once_with(True)
        wifi().config.assert_called_once_with(dhcp_hostname=self.host_name)
        wifi().connect.assert_called_once_with(self.sample_ssid, self.sample_password)
        assert wifi().isconnected.call_count == 3

    @patch("source.networking.wifi_client.network.WLAN")
    def test_wifi_should_start(self, wifi):
        wifi_client = WifiClient(self.sample_ssid, self.sample_password)
        wifi().isconnected = Mock(return_value=False)
        wifi_client.try_connecting = Mock()

        wifi_client.start()

        wifi_client.try_connecting.assert_called_once()
        wifi().isconnected.assert_called_once()

    @patch("source.networking.wifi_client.network.WLAN")
    def test_wifi_has_already_started(self, wifi):
        wifi_client = WifiClient(self.sample_ssid, self.sample_password)
        wifi().isconnected = Mock(return_value=True)
        wifi_client.try_connecting = Mock()

        wifi_client.start()

        wifi_client.try_connecting.assert_not_called()
        wifi().isconnected.assert_called_once()

    @patch("source.networking.wifi_client.network.WLAN")
    @patch("source.networking.wifi_client.machine.reset")
    def test_wifi_fatal_error(self, wifi, reset):
        wifi_client = WifiClient(self.sample_ssid, self.sample_password)
        wifi().isconnected = Mock(return_value=False)
        wifi_client.try_connecting = Mock(side_effect=Exception("error"))

        wifi_client.start()

        reset.assert_called_once()


if __name__ == "__main__":
    unittest.main()
