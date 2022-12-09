from machine import Pin
from config.config import LED_PIN

led_pin = Pin(LED_PIN, Pin.OUT)


class Led:
    def __init__(self, is_inverted):
        self.is_inverted = is_inverted
        self.on_value = not is_inverted
        self.off_value = is_inverted

    def turn_on(self):
        led_pin.value(self.on_value)

    def turn_off(self):
        led_pin.value(self.off_value)

    @staticmethod
    def toggle():
        led_pin.value(not led_pin.value)

    def set_state(self, desired_state):
        if self.is_inverted:
            led_pin.value(not desired_state)
        else:
            led_pin.value(desired_state)

    def get_state(self):
        if self.is_inverted:
            return not led_pin.value()
        else:
            return led_pin.value()
