import time


class Debouncer:
    def __init__(self, debounce_delay_ms=50):
        self.debounce_delay = debounce_delay_ms
        self.last_click_time = time.ticks_ms()
        self.last_button_state = inverted_input

