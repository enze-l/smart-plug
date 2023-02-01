import sys
from unittest.mock import Mock, AsyncMock


def init_micropython_mock_modules():
    sys.modules["network"] = Mock()
    sys.modules["machine"] = Mock()
    sys.modules["time"] = Mock()
    sys.modules["urequests"] = Mock()
    sys.modules["uasyncio"] = AsyncMock()
    sys.modules["micropython"] = Mock()
