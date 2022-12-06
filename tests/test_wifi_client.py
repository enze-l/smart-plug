import unittest
from unittest.mock import patch, MagicMock
from source.networking.wifi_client import WifiClient


class TestWifi(unittest.TestCase):
    def setUp(self):
        self.sample_ssid = "sample_ssid"
        self.sample_password = "sample_password"

    @patch("network", MagicMock)
    def test_wifi_should_connect(self):

        wifi = WifiClient(self.sample_ssid, self.sample_password)


if __name__ == "__main__":
    unittest.main()
