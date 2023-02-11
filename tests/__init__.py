import sys
import warnings

warnings.simplefilter("ignore", RuntimeWarning)

sys.path.append("source")  # noqa: E402

from tests.mocks import init_micropython_mock_modules

init_micropython_mock_modules()
