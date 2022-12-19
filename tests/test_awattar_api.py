from unittest import TestCase
import uasyncio
from unittest.mock import Mock
from source.api.awattar.awattar_api import AwattarApi


class TestAwattarAPI(TestCase):
    async def test_API_should_start(self):
        hardware = Mock()
        api = AwattarApi(hardware)

        assert not api.is_running

        event_loop = uasyncio.get_event_loop()
        task = event_loop.create_task(api.start())
        event_loop.run_forever()
        await task

        assert api.is_running
