from unittest import TestCase
from unittest.mock import Mock, patch
from source.hardware.binary_output import BinaryOutput

on_value = True
off_value = False
inverted_on_value = False
inverted_off_value = True
inverted = True
standard = False
output_pin = 0


class TestLed(TestCase):
    @patch("source.hardware.binary_output.Pin")
    def test_led_should_turn_on(self, mock_pin):
        output = BinaryOutput(output_pin, standard)
        output.turn_on()
        mock_pin().value.assert_called_once_with(on_value)

    @patch("source.hardware.binary_output.Pin")
    def test_inverted_led_should_turn_on(self, mock_pin):
        output = BinaryOutput(output_pin, inverted)
        output.turn_on()
        mock_pin().value.assert_called_once_with(inverted_on_value)

    @patch("source.hardware.binary_output.Pin")
    def test_led_should_turn_off(self, mock_pin):
        output = BinaryOutput(output_pin, standard)
        output.turn_off()
        mock_pin().value.assert_called_once_with(off_value)

    @patch("source.hardware.binary_output.Pin")
    def test_inverted_led_should_turn_off(self, mock_pin):
        output = BinaryOutput(output_pin, inverted)
        output.turn_off()
        mock_pin().value.assert_called_once_with(inverted_off_value)

    @patch("source.hardware.binary_output.Pin")
    def test_led_should_get_toggled_on(self, mock_pin):
        output = BinaryOutput(output_pin, standard)
        mock_pin().value = Mock(return_value=off_value)

        output.toggle()

        mock_pin().value.assert_called_with(on_value)

    @patch("source.hardware.binary_output.Pin")
    def test_led_should_get_toggled_off(self, mock_pin):
        output = BinaryOutput(output_pin, standard)
        mock_pin().value = Mock(return_value=on_value)

        output.toggle()

        mock_pin().value.assert_called_with(off_value)

    @patch("source.hardware.binary_output.Pin")
    def test_set_led_state(self, mock_pin):
        output = BinaryOutput(output_pin, standard)
        output.set_on_state(on_value)
        mock_pin().value.assert_called_once_with(on_value)

    @patch("source.hardware.binary_output.Pin")
    def test_set_inverted_led_state(self, mock_pin):
        output = BinaryOutput(output_pin, inverted)
        output.set_on_state(on_value)
        mock_pin().value.assert_called_once_with(inverted_on_value)

    @patch("source.hardware.binary_output.Pin")
    def test_get_led_on_state(self, mock_pin):
        output = BinaryOutput(output_pin, standard)
        mock_pin().value = Mock(return_value=on_value)

        current_on_state = output.get_on_state()

        self.assertEqual(on_value, current_on_state)

    @patch("source.hardware.binary_output.Pin")
    def test_get_inverted_led_on_state(self, mock_pin):
        output = BinaryOutput(output_pin, inverted)
        mock_pin().value = Mock(return_value=on_value)

        current_on_state = output.get_on_state()

        self.assertEqual(inverted_on_value, current_on_state)
