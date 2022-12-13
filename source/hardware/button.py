from .utilities.debouncer import Debouncer


class Button:
    def __init__(self, pin, inverted_input, debounce_delay_ms=50):
        on_value = not inverted_input
        self.debouncer = Debouncer(pin, on_value, debounce_delay_ms)

    def set_on_click_function(self, function):
        self.debouncer.set_on_release_function(function)

    def set_on_release_function(self, function):
        self.debouncer.set_on_click_function(function)

    def set_on_toggle_function(self, function):
        self.debouncer.set_on_toggle_function(function)
