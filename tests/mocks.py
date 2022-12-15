import sys
from unittest.mock import Mock


def init_micropython_mock_modules():
    sys.modules["network"] = Mock()
    sys.modules["machine"] = Mock()
    sys.modules["time"] = Mock()
