from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock, patch
from source.api.websocket.api import API


class TestWebsocketAPI(IsolatedAsyncioTestCase):
    @patch("source.api.websocket.api.API._API__set_button_behaviour")
    async def test_start_api(self, mock_button_behaviour):
        hardware = Mock()
        api = API(hardware)
        mock_get_is_running = Mock(side_effect=[True, False])
        api._API__get_is_running = mock_get_is_running
        mock_init_connection = AsyncMock()
        mock_set_running = Mock()
        api._API__set_is_running = mock_set_running
        api._API__init_connection = mock_init_connection
        mock_socket = Mock()
        api.socket = mock_socket

        await api.start()

        mock_button_behaviour.assert_called_once()
        mock_init_connection.assert_called_once()
        mock_socket.close.assert_called_once()
        mock_set_running.assert_called_once()
        assert mock_get_is_running.call_count == 2

    @patch("source.api.websocket.api.API._API__set_button_behaviour")
    async def test_api_runs_three_cycles(self, mock_button_behaviour):
        hardware = Mock()
        api = API(hardware)
        mock_get_is_running = Mock(side_effect=[True, True, True, False])
        api._API__get_is_running = mock_get_is_running
        mock_init_connection = AsyncMock()
        mock_set_running = Mock()
        api._API__set_is_running = mock_set_running
        api._API__init_connection = mock_init_connection
        mock_socket = Mock()
        api.socket = mock_socket

        await api.start()

        mock_button_behaviour.assert_called_once()
        assert mock_init_connection.call_count == 3
        mock_socket.close.assert_called_once()
        mock_set_running.assert_called_once()
        assert mock_get_is_running.call_count == 4

    def test_stop_api(self):
        hardware = Mock()
        api = API(hardware)
        mock_set_is_running = Mock()
        api._API__set_is_running = mock_set_is_running
        mock_handle_message_task = Mock()
        api.handle_message_task = mock_handle_message_task
        mock_handel_connect_task = Mock()
        api.handle_connect_task = mock_handel_connect_task
        mock_button = Mock()
        api.button = mock_button

        api.stop()

        mock_set_is_running.assert_called_once()
        mock_handle_message_task.cancel.assert_called_once()
        mock_handel_connect_task.cancel.asser_called_once()
        mock_button.reset_functions.assert_called_once()

    async def test_connect(self):
        hardware = Mock()
        api = API(hardware)
        mock_socket = Mock()
        api.socket = mock_socket

        await api._API__connect()

        mock_socket.connect.assert_called_once()
        assert api.connected

    @patch("source.api.websocket.api.socket")
    async def test_connect_fails(self, mock_socket_module):
        hardware = Mock()
        api = API(hardware)
        mock_socket = Mock()
        mock_socket.connect.side_effect = OSError()
        api.socket = mock_socket

        await api._API__connect()

        mock_socket.connect.assert_called_once()
        mock_socket.close.assert_called_once()
        mock_socket_module.socket.assert_called_once()
        assert not api.connected

