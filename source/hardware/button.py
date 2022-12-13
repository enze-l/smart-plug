from machine import Pin
import time


class Button:
    def __init__(self, pin, inverted_input, debounce_delay_ms=50):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.inverted_input = inverted_input
        self.function = None
        self.on_value = not inverted_input
        self.off_value = inverted_input
        self.pin.irq(handler=self.__use_function)

        self.debounce_delay = debounce_delay_ms
        self.last_click_time = time.ticks_ms()
        self.last_button_state = inverted_input

    def set_function(self, function):
        self.function = function

    def __use_function(self, irq):
        button_state = self.pin.value()
        click_time = time.ticks_ms()
        if button_state != self.last_button_state:
            debounced_time = time.ticks_diff(click_time, self.debounce_delay)
            if time.ticks_diff(debounced_time, self.last_click_time) > 0:
                self.last_click_time = click_time
                self.last_button_state = button_state
                self.function()
