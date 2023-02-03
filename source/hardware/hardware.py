import network
import config.config as config
from .binary_output import BinaryOutput
from .button import Button
from .relay_with_led import RelayWithLed

led = BinaryOutput(config.LED_PIN, config.LED_IS_INVERTED)
relay = BinaryOutput(config.RELAY_PIN, config.RELAY_IS_INVERTED)
relay_with_led = RelayWithLed(relay, led)

button_internal = Button(config.BUTTON_INTERNAL_PIN, config.BUTTON_INTERNAL_IS_INVERTED)
button_external = Button(config.BUTTON_EXTERNAL_PIN, config.BUTTON_EXTERNAL_IS_INVERTED)


def get_ip_address():
    network_adapter = network.WLAN(network.STA_IF)
    connection_info = network_adapter.ifconfig()
    return connection_info[0]
