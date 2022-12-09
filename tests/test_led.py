import unittest
from unittest.mock import patch
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
        pin.value.assert_called_once_with(True)

    @patch("source.hardware.led.led_pin")
    def test_inverted_led_should_turn_on(self, pin):
        led = Led(inverted)
        led.turn_on()
        pin.value.assert_called_once_with(False)

    @patch("source.hardware.led.led_pin")
    def test_led_should_turn_off(self, pin):
        led = Led(standard)
        led.turn_off()
        pin.value.assert_called_once_with(False)

    @patch("source.hardware.led.led_pin")
    def test_inverted_led_should_turn_off(self, pin):
        led = Led(inverted)
        led.turn_off()
        pin.value.assert_called_once_with(True)


if __name__ == "__main__":
    unittest.main()
