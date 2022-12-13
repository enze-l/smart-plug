import time
from machine import Pin


class Button:
    def __init__(self, pin, inverted_input, debounce_delay_ms=50):
        self.on_toggle_function = None
        self.on_release_function = None
        self.on_click_function = None
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.debounce_delay = debounce_delay_ms
        self.last_click_time = time.ticks_ms()
        self.last_button_state = not inverted_input
        self.pin.irq(handler=self.__debounce_function)

    def set_on_click_function(self, function):
        self.on_click_function = function

    def set_on_release_function(self, function):
        self.on_click_function = function

    def set_on_toggle_function(self, function):
        self.on_toggle_function = function

    def __debounce_function(self, irq):
        time_of_click = time.ticks_ms()
        current_button_state = self.pin.value()
        if current_button_state == self.last_button_state:
            return
        if not self.__enough_time_has_lapsed_to_trigger(time_of_click):
            return
        self.__execute_function_and_reset_(time_of_click, current_button_state)

    def __enough_time_has_lapsed_to_trigger(self, time_of_click):
        min_elapsed_time = time.ticks_add(self.last_click_time, self.debounce_delay)
        return time.ticks_diff(min_elapsed_time, time_of_click) < 0

    def __execute_function_and_reset_(self, time_of_click, current_button_state):
        self.last_click_time = time_of_click
        self.last_button_state = current_button_state
        if self.on_click_function and current_button_state:
            self.on_click_function()
        if self.on_release_function and not current_button_state:
            self.on_release_function()
        if self.on_toggle_function:
            self.on_toggle_function()
