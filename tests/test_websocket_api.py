from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock, patch
from source.api.websocket.api import API


class TestWebsocketAPI(IsolatedAsyncioTestCase):
    @patch("source.api.websocket.api.API._API__set_button_behaviour")
    async def test_start_api(self, mock_button_behaviour):
        hardware = Mock()
        api = API(hardware)
        api._API__get_is_running = Mock(side_effect=[True, False])
        mock_init_connection = AsyncMock()
        api._API__init_connection = mock_init_connection
        mock_socket = Mock()
        api.socket = mock_socket
        mock_set_running = Mock()
        api._API__set_is_running = mock_set_running

        await api.start()

        mock_button_behaviour.assert_called_once()
        mock_init_connection.assert_called_once()
        mock_socket.close.assert_called_once()
        mock_set_running.assert_called_once()
