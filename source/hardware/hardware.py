import network
from config.config_manager import ConfigManager, STANDARD_CONFIG_FILE_PATH
from .binary_output import BinaryOutput
from .button import Button
from .relay_with_led import RelayWithLed

_config = ConfigManager(STANDARD_CONFIG_FILE_PATH)

led = BinaryOutput(_config.get_value("LED_PIN"), _config.get_value("LED_IS_INVERTED"))
relay = BinaryOutput(
    _config.get_value("RELAY_PIN"), _config.get_value("RELAY_IS_INVERTED")
)
relay_with_led = RelayWithLed(relay, led)

button_internal = Button(
    _config.get_value("BUTTON_INTERNAL_PIN"),
    _config.get_value("BUTTON_INTERNAL_IS_INVERTED"),
)
button_external = Button(
    _config.get_value("BUTTON_EXTERNAL_PIN"),
    _config.get_value("BUTTON_EXTERNAL_IS_INVERTED"),
)


def get_ip_address():
    network_adapter = network.WLAN(network.STA_IF)
    connection_info = network_adapter.ifconfig()
    return connection_info[0]
