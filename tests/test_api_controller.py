from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, AsyncMock, patch
from source.api.api_controller import APIController


class TestAPIController(IsolatedAsyncioTestCase):
    @patch("source.api.api_controller.ConfigManager")
    @patch("source.api.api_controller.APIController._APIController__load_api")
    async def test_start_api(self, mock_get_value, mock_import):
        hardware = Mock()
        api_controller = APIController(hardware)
        mock_api = AsyncMock()
        api_controller.api = mock_api

        await api_controller.start_api()

        mock_api.start.assert_called_once()




