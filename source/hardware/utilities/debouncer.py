import time
from machine import Pin


class Debouncer:
    def __init__(self, pin, on_state, debounce_delay_ms):
        self.function = None
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.debounce_delay = debounce_delay_ms
        self.last_click_time = time.ticks_ms()
        self.last_button_state = on_state
        self.pin.irq(handler=self.__debounce_function)

    def set_function(self, function):
        self.function = function

    def __debounce_function(self, irq):
        time_of_click = time.ticks_ms()
        current_button_state = self.pin.value()
        if current_button_state == self.last_button_state:
            return
        min_elapsed_time = time.ticks_add(self.last_click_time, self.debounce_delay)
        if time.ticks_diff(min_elapsed_time, time_of_click) > 0:
            return
        self.last_click_time = time_of_click
        self.last_button_state = current_button_state
        if current_button_state:
            self.function()
