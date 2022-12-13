from machine import Pin


class Switch:
    def __init__(self, pin, inverted_input):
        self.off_function = None
        self.on_function = None
        self.pin = (pin, Pin.In)
        self.inverted_input = inverted_input
        self.on_value = not inverted_input
        self.off_value = inverted_input

    def set_on_function(self, function):
        self.on_function = function

    def set_off_function(self, function):
        self.off_function = function

    def set_toggle_function(self, function):
        self.on_function = function
        self.off_function = function
