import unittest
from source.networking.wifi_client import WifiClient
from tests.mocks import network
from unittest.mock import MagicMock, Mock


class TestWifi(unittest.TestCase):
    def setUp(self):
        self.sample_ssid = "sample_ssid"
        self.sample_password = "sample_password"

    def test_wifi_should_start(self):
        wifi = WifiClient(self.sample_ssid, self.sample_password)
        wifi.start()

    def test_wifi_should_establish_connection(self):
        wifi = WifiClient(self.sample_ssid, self.sample_password)

        active = Mock()
        connect = Mock()
        isconnected = Mock()
        network.WLAN().active = active
        network.WLAN().connect = connect
        network.WLAN().isconnected = isconnected

        wifi._WifiClient__establish_connection()

        active.assert_called_once()
        connect.assert_called_once()
        isconnected.assert_called_once()


if __name__ == "__main__":
    unittest.main()
