from binary_output import BinaryOutput
import config.config as config

led = BinaryOutput(config.LED_PIN, True)
relay = BinaryOutput(config.RELAY_PIN, False)

