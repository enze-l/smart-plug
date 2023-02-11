import warnings
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, AsyncMock, patch, call
from source.api.implementations.awattar.api import API


@patch("source.api.implementations.awattar.api.ConfigManager.get_value")
class TestAwattarAPI(IsolatedAsyncioTestCase):
    @patch("source.api.implementations.awattar.api.API._API__get_is_running")
    async def test_api_should_start_and_stop(self, mock_is_running, mock_get_value):
        warnings.simplefilter("ignore", RuntimeWarning)
        hardware = Mock()

        mock_is_running.side_effect = [True, False]

        api = API(hardware)
        mock_poll_request = AsyncMock()
        api._API__poll_awattar_api = mock_poll_request
        mock_cancel_tasks = Mock()
        api._API__cancel_all_tasks = mock_cancel_tasks

        await api.start()

        mock_poll_request.assert_called_once()
        mock_cancel_tasks.assert_called_once()

    def test_api_should_stop(self, mock_get_value):
        hardware = Mock()
        api = API(hardware)

        mock_cancel_tasks = Mock()
        api._API__cancel_all_tasks = mock_cancel_tasks
        mock_set_is_running = Mock()
        api._API__set_is_running = mock_set_is_running

        api.stop()

        mock_cancel_tasks.assert_called_once()
        mock_set_is_running.assert_called_once_with(False)

    def test_toggle_relay_should_succeed(self, mock_get_value):
        hardware = Mock()
        api = API(hardware)

        api._API__toggle_relay_if_appropriate(True)
        api._API__toggle_relay_if_appropriate(False)

        hardware.relay_with_led.set_on_state.assert_has_calls([call(True), call(False)])

    def test_toggle_relay_should_fail_automation_overriden(self, mock_get_value):
        hardware = Mock()
        api = API(hardware)

        api.automation_overriden = True

        api._API__toggle_relay_if_appropriate(True)

        hardware.relay_with_led.set_on_state.assert_not_called()

    def test_toggle_relay_should_reset_automation(self, mock_get_value):
        hardware = Mock()
        api = API(hardware)

        hardware.relay_with_led.get_on_state.return_value = True
        api.automation_overriden = True

        api._API__toggle_relay_if_appropriate(True)

        assert not api.automation_overriden

    async def test_react_to_price_change_should_toggle_relay_off(self, mock_get_value):
        hardware = Mock()
        api = API(hardware)
        mock_relay_toggle_function = Mock()
        api._API__toggle_relay_if_appropriate = mock_relay_toggle_function

        api.price_threshold_eur = 200

        too_high_price = 250
        time_till_execution = 0
        await api._API__react_to_price_change(time_till_execution, too_high_price)

        mock_relay_toggle_function.assert_called_once_with(False)

    async def test_react_to_price_change_should_toggle_relay_on(self, mock_get_value):
        hardware = Mock()
        api = API(hardware)
        mock_relay_toggle_function = Mock()
        api._API__toggle_relay_if_appropriate = mock_relay_toggle_function

        api.price_threshold_eur = 200

        low_enough_price = 180
        time_till_execution = 0
        await api._API__react_to_price_change(low_enough_price, time_till_execution)

        mock_relay_toggle_function.assert_called_once_with(True)

    @patch("source.api.implementations.awattar.api.API._API__react_to_price_change")
    @patch("source.api.implementations.awattar.api.uasyncio")
    @patch("source.api.implementations.awattar.api.time")
    def test_create_scheduled_price_change_reaction(
        self, mock_time, mock_uasyncio, mock_react_to_price_change, mock_get_value
    ):
        warnings.simplefilter("ignore", RuntimeWarning)
        hardware = Mock()
        api = API(hardware)
        time_of_execution = 1400
        price_at_time_of_execution = 250
        current_time = 800
        mock_time.time.return_value = current_time
        time_till_execution = time_of_execution - current_time

        api._API__schedule_price_change_reaction(
            time_of_execution, price_at_time_of_execution
        )

        mock_react_to_price_change.assert_called_once_with(
            time_till_execution, price_at_time_of_execution
        )
        mock_uasyncio.create_task.assert_called_once()
        assert len(api.tasks) == 1

    @patch("source.api.implementations.awattar.api.API._API__process_price_changes")
    @patch("source.api.implementations.awattar.api.urequests")
    @patch("source.api.implementations.awattar.api.uasyncio")
    async def test_poll_api_succeeds(
        self, mock_uasyncio, mock_urequest, mock_process_changes, mock_get_value
    ):
        mock_urequest.get().status_code = 200

        hardware = Mock()
        api = API(hardware)

        await api._API__poll_awattar_api()

        mock_process_changes.assert_called_once()
        mock_uasyncio.create_task.assert_not_called()

    @patch("source.api.implementations.awattar.api.API._API__process_price_changes")
    @patch("source.api.implementations.awattar.api.urequests")
    @patch("source.api.implementations.awattar.api.uasyncio")
    async def test_poll_api_fails(
        self, mock_uasyncio, mock_urequest, mock_process_changes, mock_get_value
    ):
        warnings.simplefilter("ignore", RuntimeWarning)
        mock_urequest.get().status_code = 404

        hardware = Mock()
        api = API(hardware)

        await api._API__poll_awattar_api()

        mock_process_changes.assert_not_called()
        mock_uasyncio.create_task.assert_called_once()

    @patch(
        "source.api.implementations.awattar.api.API._API__schedule_price_change_reaction"
    )
    def test_process_price_changes(self, mock_schedule_reaction, mock_get_value):
        hardware = Mock()
        api = API(hardware)

        data = [
            {
                "start_timestamp": 1671098400000,
                "end_timestamp": 1671102000000,
                "marketprice": 450.72,
                "unit": "Eur/MWh",
            },
            {
                "start_timestamp": 1671102000000,
                "end_timestamp": 1671105600000,
                "marketprice": 406.56,
                "unit": "Eur/MWh",
            },
            {
                "start_timestamp": 1671105600000,
                "end_timestamp": 1671109200000,
                "marketprice": 396.53,
                "unit": "Eur/MWh",
            },
        ]

        api._API__process_price_changes(data)
        assert mock_schedule_reaction.call_count == 3

    def test_get_html_options(self, mock_get_value):
        hardware = Mock()
        api = API(hardware)
        test_ip_address = "156.156.156.156"
        api.ip_address = test_ip_address
        test_price_threshold = 180
        api.price_threshold_eur = test_price_threshold
        test_api_port = 8888
        mock_get_value.return_value = test_api_port

        expected_html = """
        <iframe name="dummyframe" id="dummyframe" style="display: none;"></iframe>
        <form method="post" action="http://156.156.156.156:8888" target="dummyframe">
            <input name="toggle_threshold" type="number" required value=180>
            <input type="submit" value="Set price Euro/MWh">
        </form>"""

        assert expected_html.replace(" ", "") in api.get_html_options().replace(" ", "")
