import unittest
from unittest.mock import Mock, patch
from source.hardware.button import Button

is_inverted = True
is_not_inverted = False
input_pin = 0
on_value = True
off_value = False


class TestButton(unittest.TestCase):
    @patch('source.hardware.button.Pin')
    @patch('source.hardware.button.time')
    def test_click_should_trigger_function(self, mock_time, mock_pin):
        button = Button(input_pin, is_not_inverted)
        mock_pin().value = Mock(return_value=on_value)
        enough_time_passed_to_click = -200
        mock_time.ticks_diff = Mock(return_value=enough_time_passed_to_click)

        test_function = Mock()
        button.set_on_click_function(test_function)

        button._Button__debounce_function(None)

        test_function.assert_called_once()

    @patch('source.hardware.button.Pin')
    @patch('source.hardware.button.time')
    def test_click_should_trigger_function_on_inverted_button(self, mock_time, mock_pin):
        button = Button(input_pin, is_inverted)
        mock_pin().value = Mock(return_value=off_value)
        enough_time_passed_to_click = -200
        mock_time.ticks_diff = Mock(return_value=enough_time_passed_to_click)

        test_function = Mock()
        button.set_on_click_function(test_function)

        button._Button__debounce_function(None)

        test_function.assert_called_once()

    @patch('source.hardware.button.Pin')
    @patch('source.hardware.button.time')
    def test_click_should_not_trigger_function_not_enough_time_passed(self, mock_time, mock_pin):
        button = Button(input_pin, is_not_inverted)
        mock_pin().value = Mock(return_value=on_value)
        not_enough_time_passed_to_click = 200
        mock_time.ticks_diff = Mock(return_value=not_enough_time_passed_to_click)

        test_function = Mock()
        button.set_on_click_function(test_function)

        button._Button__debounce_function(None)

        test_function.assert_not_called()

    @patch('source.hardware.button.Pin')
    @patch('source.hardware.button.time')
    def test_click_should_not_trigger_function_state_has_not_changed(self, mock_time, mock_pin):
        button = Button(input_pin, is_not_inverted)
        mock_pin().value = Mock(return_value=off_value)
        enough_time_passed_to_click = -200
        mock_time.ticks_diff = Mock(return_value=enough_time_passed_to_click)

        test_function = Mock()
        button.set_on_click_function(test_function)

        button._Button__debounce_function(None)

        test_function.assert_not_called()
