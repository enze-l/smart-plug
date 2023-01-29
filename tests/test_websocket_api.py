from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, patch
from source.api.websocket.api import API


class TestWebsocketAPI(IsolatedAsyncioTestCase):
    @patch("source.api.websocket.api.API._API__set_button_behaviour")
    @patch("source.api.websocket.api._thread")
    def test_start_api(self, mock_thread, mock_button_behaviour):
        hardware = Mock()
        api = API(hardware)

        api.start()

        mock_button_behaviour.assert_called_once()
        mock_thread.start_new_thread.assert_called_once_with(api._API__run_api, ())

    def test_stop_api(self):
        hardware = Mock()
        api = API(hardware)
        mock_button = Mock()
        api.button = mock_button
        mock_socket = Mock()
        api.socket = mock_socket
        mock_connection_thread = Mock()
        api.connection_thread = mock_connection_thread

        api.stop()

        mock_button.reset_functions.assert_called_once()
        mock_socket.close.assert_called_once()
        mock_connection_thread.exit.assert_called_once()

    def test_connect(self):
        hardware = Mock()
        api = API(hardware)
        mock_socket = Mock()
        api.socket = mock_socket
        mock_is_connected = Mock(side_effect=[False, True])
        api.get_is_connected = mock_is_connected

        api._API__connect()

        mock_socket.connect.assert_called_once()
        assert api.is_connected

    @patch("source.api.websocket.api.socket")
    def test_connect_fails(self, mock_socket_module):
        hardware = Mock()
        api = API(hardware)
        mock_socket = Mock()
        mock_socket.connect.side_effect = OSError()
        api.socket = mock_socket
        mock_is_connected = Mock(side_effect=[False, True])
        api.get_is_connected = mock_is_connected

        api._API__connect()

        mock_socket.connect.assert_called_once()
        mock_socket.close.assert_called_once()
        mock_socket_module.socket.assert_called_once()
        assert not api.is_connected

    @patch("source.api.websocket.api.API._API__process_message")
    def test_get_message(self, mock_process_message):
        message_encoded = b"Hello"
        message_decoded = "Hello"
        hardware = Mock()
        api = API(hardware)
        api.socket = Mock()
        api.socket.recv = Mock(return_value=message_encoded)
        mock_is_connected = Mock(side_effect=[True, False])
        api.get_is_connected = mock_is_connected

        api._API__get_message()

        mock_process_message.assert_called_with(message_decoded)

    @patch("source.api.websocket.api.API._API__process_message")
    def test_get_message_fails_broke_pipe(self, mock_process_message):
        message_encoded = b""
        hardware = Mock()
        api = API(hardware)
        api.socket = Mock()
        api.socket.recv = Mock(return_value=message_encoded)
        mock_is_connected = Mock(side_effect=[True, False])
        api.get_is_connected = mock_is_connected

        api._API__get_message()

        mock_process_message.assert_not_called()
        assert not api.is_connected

    def test_process_message_succeeds(self):
        hardware = Mock()
        api = API(hardware)
        mock_relay = Mock()
        api.relay = mock_relay

        api._API__process_message("turn_on")
        mock_relay.turn_on.assert_called_once()

        api._API__process_message("turn_off")
        mock_relay.turn_off.assert_called_once()

        api._API__process_message("toggle")
        mock_relay.toggle.assert_called_once()

    def test_process_message_get_succeeds(self):
        hardware = Mock()
        api = API(hardware)
        mock_relay = Mock()
        api.relay = mock_relay
        mock_socket = Mock()
        api.socket = mock_socket

        api._API__process_message("get_state")

        mock_relay.get_on_state_string.assert_called_once()
        mock_socket.sendall.assert_called_once()

    def test_process_message_command_not_recognized(self):
        hardware = Mock()
        api = API(hardware)
        mock_relay = Mock()
        api.relay = mock_relay
        bad_message = "bad message"

        api._API__process_message(bad_message)

        api.relay.assert_not_called()
