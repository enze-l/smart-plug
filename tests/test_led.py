import unittest
from unittest.mock import Mock, patch
from source.hardware.led import Led

on_value = True
off_value = False
inverted_on_value = False
inverted_off_value = True
inverted = True
standard = False


class TestLed(unittest.TestCase):

    @patch("source.hardware.led.led_pin")
    def test_led_should_turn_on(self, pin):
        led = Led(standard)
        led.turn_on()
        pin.value.assert_called_once_with(on_value)

    @patch("source.hardware.led.led_pin")
    def test_inverted_led_should_turn_on(self, pin):
        led = Led(inverted)
        led.turn_on()
        pin.value.assert_called_once_with(inverted_on_value)

    @patch("source.hardware.led.led_pin")
    def test_led_should_turn_off(self, pin):
        led = Led(standard)
        led.turn_off()
        pin.value.assert_called_once_with(off_value)

    @patch("source.hardware.led.led_pin")
    def test_inverted_led_should_turn_off(self, pin):
        led = Led(inverted)
        led.turn_off()
        pin.value.assert_called_once_with(inverted_off_value)

    @patch("source.hardware.led.led_pin")
    def test_led_should_get_toggled(self, pin):
        led = Led(standard)
        led.toggle()
        pin.value.assert_called_once()

    @patch("source.hardware.led.led_pin")
    def test_set_led_state(self, pin):
        led = Led(standard)
        led.set_on_state(on_value)
        pin.value.assert_called_once_with(on_value)

    @patch("source.hardware.led.led_pin")
    def test_set_inverted_led_state(self, pin):
        led = Led(inverted)
        led.set_on_state(on_value)
        pin.value.assert_called_once_with(inverted_on_value)

    @patch("source.hardware.led.led_pin")
    def test_get_led_on_state(self, pin):
        led = Led(standard)
        pin.value = Mock(return_value=on_value)

        current_on_state = led.get_on_state()

        self.assertEqual(on_value, current_on_state)

    @patch("source.hardware.led.led_pin")
    def test_get_inverted_led_on_state(self, pin):
        led = Led(inverted)
        pin.value = Mock(return_value=on_value)

        current_on_state = led.get_on_state()

        self.assertEqual(inverted_on_value, current_on_state)


if __name__ == "__main__":
    unittest.main()
