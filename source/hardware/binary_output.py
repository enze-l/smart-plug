from machine import Pin


class BinaryOutput:
    def __init__(self, pin, inverted_output):
        self.pin = Pin(pin, Pin.OUT)
        self.inverted_output = inverted_output
        self.on_value = not inverted_output
        self.off_value = inverted_output

    def turn_on(self):
        self.pin.value(self.on_value)

    def turn_off(self):
        self.pin.value(self.off_value)

    def toggle(self):
        self.pin.value(not self.pin.value())

    def set_on_state(self, desired_state):
        if self.inverted_output:
            self.pin.value(not desired_state)
        else:
            self.pin.value(desired_state)

    def get_on_state(self):
        if self.inverted_output:
            return not self.pin.value()
        else:
            return self.pin.value()
