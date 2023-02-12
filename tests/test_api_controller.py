from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, AsyncMock, patch
from source.api.api_controller import APIController


class TestAPIController(IsolatedAsyncioTestCase):
    @patch("source.api.api_controller.ConfigManager")
    @patch("source.api.api_controller.APIController._APIController__load_api")
    async def test_start_api(self, mock_load_api, mock_config_manager):
        hardware = Mock()
        api_controller = APIController(hardware)
        mock_api = AsyncMock()
        api_controller.api = mock_api

        await api_controller.start_api()

        mock_api.start.assert_called_once()
        api_controller.config.get_value.assert_called_once_with("CURRENT_API")
        mock_load_api.asser_called_once()

    @patch("source.api.api_controller.ConfigManager")
    @patch("source.api.api_controller.APIController._APIController__load_api")
    async def test_stop_api(self, mock_load_api, mock_config_manager):
        hardware = Mock()
        api_controller = APIController(hardware)
        mock_api = Mock()
        api_controller.api = mock_api

        api_controller.stop_api()

        mock_api.stop.assert_called_once()

    @patch("source.api.api_controller.ConfigManager")
    @patch("source.api.api_controller.APIController._APIController__load_api")
    async def test_change_api(self, mock_load_api, mock_config_manager):
        hardware = Mock()
        api_controller = APIController(hardware)
        mock_start_api = AsyncMock()
        mock_stop_api = Mock()
        api_controller.start_api = mock_start_api
        api_controller.stop_api = mock_stop_api

        api_name = "test_api"
        await api_controller.change_api(api_name)

        mock_start_api.assert_called_once()
        mock_stop_api.assert_called_once()
        mock_load_api.asser_called_once()

    @patch("source.api.api_controller.ConfigManager")
    @patch("source.api.api_controller.APIController._APIController__import_api")
    def test_load_api_from_memory(self, mock_import_api, mock_confi_manager):
        hardware = Mock()
        api_controller = APIController(hardware)

        test_api_name = "test_api_name"
        api_controller._APIController__load_api(test_api_name)

        assert mock_import_api.call_count == 2
        assert api_controller.current_api_name == test_api_name

    @patch("source.api.api_controller.ConfigManager")
    @patch("source.api.api_controller.APIController._APIController__import_api")
    def test_load_api_from_cash(self, mock_import_api, mock_confi_manager):
        hardware = Mock()
        api_controller = APIController(hardware)

        test_api_name = "test_api_name"
        mock_test_api = Mock()
        api_controller.api_cash_dict[test_api_name] = mock_test_api

        api_controller._APIController__load_api(test_api_name)

        assert mock_import_api.call_count == 1
        assert api_controller.current_api_name == test_api_name

    @patch("source.api.api_controller.ConfigManager")
    @patch("source.api.api_controller.socket")
    @patch("source.api.api_controller.APIController._APIController__import_api")
    @patch("source.api.api_controller.APIController._APIController__accept_requests_forever")
    async def test_serve_ui(self, mock_accept_requests, mock_import_api, mock_socket, mock_config):
        hardware = Mock()
        api_controller = APIController(hardware)

        await api_controller.serve_ui()

        mock_socket.socket.assert_called_once()
        mock_socket.socket().setblocking.assert_called_once_with(False)
        mock_socket.socket().setsockopt.assert_called_once()
        mock_socket.socket().bind.assert_called_once()
        mock_socket.socket().listen.assert_called_once()
        mock_accept_requests.assert_called_once()

    @patch("source.api.api_controller.ConfigManager")
    @patch("source.api.api_controller.socket")
    @patch("source.api.api_controller.APIController._APIController__import_api")
    @patch("source.api.api_controller.generate_html")
    def test_accept_requests(self, mock_generate_html, mock_import_api, mock_config_manager, mock_socket, ):
        hardware = Mock()
        api_controller = APIController(hardware)

        mock_socket = Mock()
        mock_connection = Mock()
        mock_address = "186.158.156.156"

        def mock_accept():
            return mock_connection, mock_address
        mock_socket.accept = mock_accept
        api_controller._APIController__accept_requests(mock_socket)

        mock_generate_html.assert_called_once()
        mock_connection.sendall.assert_called_once()
        mock_connection.close.assert_called_once()


