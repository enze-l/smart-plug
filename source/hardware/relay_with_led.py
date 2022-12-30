class RelayWithLed:
    def __init__(self, relay, led):
        self.relay = relay
        self.led = led

    def toggle(self):
        self.relay.toggle()
        self.led.toggle()

    def turn_on(self):
        self.led.turn_on()
        self.relay.turn_on()

    def turn_off(self):
        self.led.turn_off()
        self.relay.turn_off()

    def set_on_state(self, state):
        self.led.set_on_state(state)
        self.relay.set_on_state(state)

    def get_on_state(self):
        return self.relay.get_on_state()

    def get_on_state_string(self):
        return self.relay.get_on_state_string()
