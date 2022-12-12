from .binary_output import BinaryOutput
import config.config as config

led = BinaryOutput(config.LED_PIN, config.LED_IS_INVERTED)
relay = BinaryOutput(config.RELAY_PIN, config.RELAY_IS_INVERTED)

