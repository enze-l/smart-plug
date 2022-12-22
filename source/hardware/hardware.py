from .binary_output import BinaryOutput
from .button import Button
from config.config import *

led = BinaryOutput(LED_PIN, LED_IS_INVERTED)
relay = BinaryOutput(RELAY_PIN, RELAY_IS_INVERTED)

button_internal = Button(
    BUTTON_INTERNAL_PIN,
    BUTTON_INTERNAL_IS_INVERTED,
    BUTTON_EXTERNAL_DEBOUNCE_DELAY,
)
button_external = Button(
    BUTTON_EXTERNAL_PIN,
    BUTTON_EXTERNAL_IS_INVERTED,
    BUTTON_INTERNAL_DEBOUNCE_DELAY,
)
