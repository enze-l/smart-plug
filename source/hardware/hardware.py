from .binary_output import BinaryOutput
from .button import Button
import config.config as config

led = BinaryOutput(config.LED_PIN, config.LED_IS_INVERTED)
relay = BinaryOutput(config.RELAY_PIN, config.RELAY_IS_INVERTED)
button_internal = Button(config.BUTTON_PIN, config.BUTTON_IS_INVERTED)
button_external = Button()
