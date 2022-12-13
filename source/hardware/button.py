from .utilities.debouncer import Debouncer


class Button:
    def __init__(self, pin, inverted_input, debounce_delay_ms=50):
        self.inverted_input = inverted_input
        self.function = None
        self.on_value = not inverted_input
        self.off_value = inverted_input

        self.debouncer = Debouncer(pin, self.on_value, debounce_delay_ms)

    def set_function(self, function):
        self.debouncer.set_function(function)

