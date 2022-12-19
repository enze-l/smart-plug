from unittest import TestCase
from unittest.mock import Mock
from source.api.awattar.awattar_api import AwattarApi


class TestAwattarAPI(TestCase):
    def test_API_should_start(self):
        hardware = Mock()
        api = AwattarApi(hardware)

        assert not api.is_running
