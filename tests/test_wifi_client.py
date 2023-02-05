import sys
sys.path.append("source")  # noqa: E402

from unittest import TestCase
from source.networking.wifi_client import WifiClient
from unittest.mock import patch, Mock

sample_ssid = "sample_ssid"
sample_password = "sample_password"
host_name = "Micro-Plug"

smart_plug_config_name_var = "SMART_PLUG_NAME"


class TestWifi(TestCase):
    @patch("source.networking.wifi_client.ConfigManager.get_value")
    @patch("source.networking.wifi_client.network.WLAN")
    def test_wifi_should_connect(self, mock_wifi, mock_config):
        wifi_client = WifiClient(sample_ssid, sample_password)
        mock_config.side_effect = host_name

        wifi_client.try_connecting()

        mock_wifi().active.assert_called_once_with(True)
        mock_config.assert_called_once_with(smart_plug_config_name_var)
        mock_wifi().connect.assert_called_once_with(sample_ssid, sample_password)
        mock_wifi().isconnected.assert_called_once()

    @patch("source.networking.wifi_client.ConfigManager.get_value")
    @patch("source.networking.wifi_client.network.WLAN")
    def test_wifi_should_connect_after_retries(self, mock_wifi, mock_config):
        wifi_client = WifiClient(sample_ssid, sample_password)
        mock_wifi().isconnected.side_effect = [False, False, True]
        mock_config.side_effect = host_name

        wifi_client.try_connecting()

        mock_wifi().active.assert_called_once_with(True)
        mock_config.assert_called_once_with(smart_plug_config_name_var)
        mock_wifi().connect.assert_called_once_with(sample_ssid, sample_password)
        assert mock_wifi().isconnected.call_count == 3

    @patch("source.networking.wifi_client.network.WLAN")
    def test_wifi_should_start(self, wifi):
        wifi_client = WifiClient(sample_ssid, sample_password)
        wifi().isconnected = Mock(return_value=False)
        wifi_client.try_connecting = Mock()

        wifi_client.start()

        wifi_client.try_connecting.assert_called_once()
        wifi().isconnected.assert_called_once()

    @patch("source.networking.wifi_client.network.WLAN")
    def test_wifi_has_already_started(self, wifi):
        wifi_client = WifiClient(sample_ssid, sample_password)
        wifi().isconnected = Mock(return_value=True)
        wifi_client.try_connecting = Mock()

        wifi_client.start()

        wifi_client.try_connecting.assert_not_called()
        wifi().isconnected.assert_called_once()

    @patch("source.networking.wifi_client.network.WLAN")
    @patch("source.networking.wifi_client.machine.reset")
    def test_wifi_fatal_error(self, wifi, reset):
        wifi_client = WifiClient(sample_ssid, sample_password)
        wifi().isconnected = Mock(return_value=False)
        wifi_client.try_connecting = Mock(side_effect=Exception("error"))

        wifi_client.start()

        reset.assert_called_once()
