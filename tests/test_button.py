import unittest
from unittest.mock import Mock, patch
from source.hardware.button import Button

is_inverted = True
is_not_inverted = False
input_pin = 0
on_value = True
off_value = False
enough_time_passed_to_click = -200


class TestButton(unittest.TestCase):
    @patch("source.hardware.button.Pin")
    @patch("source.hardware.button.time")
    def test_click_should_trigger_function(self, mock_time, mock_pin):
        button = Button(input_pin, is_not_inverted)
        mock_pin().value = Mock(return_value=on_value)
        mock_time.ticks_diff = Mock(return_value=enough_time_passed_to_click)

        test_function = Mock()
        button.set_on_click_function(test_function)

        button._Button__debounce_input(None)

        test_function.assert_called_once()

    @patch("source.hardware.button.Pin")
    @patch("source.hardware.button.time")
    def test_release_should_trigger_function(self, mock_time, mock_pin):
        button = Button(input_pin, is_not_inverted)
        mock_pin().value = Mock(return_value=off_value)
        mock_time.ticks_diff = Mock(return_value=enough_time_passed_to_click)

        test_function = Mock()
        button.set_on_release_function(test_function)

        button._Button__debounce_input(None)

        test_function.assert_called_once()

    @patch("source.hardware.button.Pin")
    @patch("source.hardware.button.time")
    def test_click_should_trigger_toggle_function(self, mock_time, mock_pin):
        button = Button(input_pin, is_not_inverted)
        mock_pin().value = Mock(return_value=on_value)
        mock_time.ticks_diff = Mock(return_value=enough_time_passed_to_click)

        test_function = Mock()
        button.set_on_toggle_function(test_function)

        button._Button__debounce_input(None)

        test_function.assert_called_once()

    @patch("source.hardware.button.Pin")
    @patch("source.hardware.button.time")
    def test_click_and_release_should_trigger_toggle_function(
        self, mock_time, mock_pin
    ):
        button = Button(input_pin, is_not_inverted)
        mock_pin().value = Mock(side_effect=[on_value, off_value])
        mock_time.ticks_diff = Mock(return_value=enough_time_passed_to_click)

        test_function = Mock()
        button.set_on_toggle_function(test_function)

        button._Button__debounce_input(None)
        button._Button__debounce_input(None)

        assert test_function.call_count == 2

    @patch("source.hardware.button.Pin")
    @patch("source.hardware.button.time")
    def test_click_should_trigger_function_on_inverted_button(
        self, mock_time, mock_pin
    ):
        button = Button(input_pin, is_inverted)
        mock_pin().value = Mock(return_value=off_value)
        mock_time.ticks_diff = Mock(return_value=enough_time_passed_to_click)

        test_function = Mock()
        button.set_on_click_function(test_function)

        button._Button__debounce_input(None)

        test_function.assert_called_once()

    @patch("source.hardware.button.Pin")
    @patch("source.hardware.button.time")
    def test_click_should_not_trigger_function_not_enough_time_passed(
        self, mock_time, mock_pin
    ):
        button = Button(input_pin, is_not_inverted)
        mock_pin().value = Mock(return_value=on_value)
        not_enough_time_passed_to_click = 200
        mock_time.ticks_diff = Mock(return_value=not_enough_time_passed_to_click)

        test_function = Mock()
        button.set_on_click_function(test_function)

        button._Button__debounce_input(None)

        test_function.assert_not_called()

    @patch("source.hardware.button.Pin")
    @patch("source.hardware.button.time")
    def test_click_should_not_trigger_function_state_has_not_changed(
        self, mock_time, mock_pin
    ):
        button = Button(input_pin, is_not_inverted)
        mock_pin().value = Mock(return_value=off_value)
        mock_time.ticks_diff = Mock(return_value=enough_time_passed_to_click)

        test_function = Mock()
        button.set_on_click_function(test_function)

        button._Button__debounce_input(None)

        test_function.assert_not_called()
