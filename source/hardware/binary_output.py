from machine import Pin


class BinaryOutput:
    def __init__(self, pin, is_inverted):
        self.pin = Pin(pin, Pin.OUT)
        self.is_inverted = is_inverted
        self.on_value = not is_inverted
        self.off_value = is_inverted

    def turn_on(self):
        self.pin.value(self.on_value)

    def turn_off(self):
        self.pin.value(self.off_value)

    def toggle(self):
        self.pin.value(not self.pin.value)

    def set_on_state(self, desired_state):
        if self.is_inverted:
            self.pin.value(not desired_state)
        else:
            self.pin.value(desired_state)

    def get_on_state(self):
        if self.is_inverted:
            return not self.pin.value()
        else:
            return self.pin.value()
