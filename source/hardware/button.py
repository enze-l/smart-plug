from machine import Pin


class Button:
    def __init__(self, pin, inverted_input):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.inverted_input = inverted_input
        self.function = None
        self.on_value = not inverted_input
        self.off_value = inverted_input
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.__use_function)

    def set_function(self, function):
        self.function = function

    def __use_function(self, irq):
        self.function()
