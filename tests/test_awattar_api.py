from unittest import IsolatedAsyncioTestCase
import uasyncio
from unittest.mock import Mock, patch
from source.api.awattar.awattar_api import AwattarApi


class TestAwattarAPI(IsolatedAsyncioTestCase):
    @patch("source.api.awattar.awattar_api.urequests")
    @patch("source.api.awattar.awattar_api.AwattarApi.get_is_running")
    async def test_API_should_start(self, is_running, request):
        hardware = Mock()

        is_running.side_effect = [True, False, False]

        api = AwattarApi(hardware)

        await uasyncio.run(await api.start())

        print("Call count + " + str(request.get.call_count))
