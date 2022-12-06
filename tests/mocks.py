import sys
from unittest.mock import MagicMock

network = MagicMock()
machine = MagicMock()


def init_micropython_mock_modules():
    sys.modules['network'] = network
    sys.modules['machine'] = machine
