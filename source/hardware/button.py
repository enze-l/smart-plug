from machine import Pin
import time


class Button:
    def __init__(self, pin, inverted_input, debounce_delay_ms=50):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.inverted_input = inverted_input
        self.function = None
        self.on_value = not inverted_input
        self.off_value = inverted_input
        self.pin.irq(handler=self.__execute_function_debounced)

        self.debounce_delay = debounce_delay_ms
        self.last_click_time = time.ticks_ms()
        self.last_button_state = inverted_input

    def set_function(self, function):
        self.function = function

    def __execute_function_debounced(self, irq):
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
