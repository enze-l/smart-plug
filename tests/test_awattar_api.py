from unittest import IsolatedAsyncioTestCase
import uasyncio
from unittest.mock import Mock, patch, call
from source.api.awattar.awattar_api import AwattarApi
import warnings


class TestAwattarAPI(IsolatedAsyncioTestCase):
    @patch("source.api.awattar.awattar_api.AwattarApi._AwattarApi__get_is_running")
    async def test_API_should_start_and_stop(self, is_running):
        hardware = Mock()

        is_running.side_effect = [True, False]

        api = AwattarApi(hardware)
        mock_poll_request = Mock()
        api._AwattarApi__poll_api = mock_poll_request
        mock_cancel_tasks = Mock()
        api._AwattarApi__cancel_all_tasks = mock_cancel_tasks

        await uasyncio.run(await api.start())

        mock_poll_request.assert_called_once()
        mock_cancel_tasks.assert_called_once()

    def test_API_should_stop(self):
        hardware = Mock()
        api = AwattarApi(hardware)

        mock_cancel_tasks = Mock()
        api._AwattarApi__cancel_all_tasks = mock_cancel_tasks
        mock_set_is_running = Mock()
        api._AwattarApi__set_is_running = mock_set_is_running

        api.stop()

        mock_cancel_tasks.assert_called_once()
        mock_set_is_running.assert_called_once_with(False)

    def test_toggle_relay_should_succeed(self):
        hardware = Mock()
        api = AwattarApi(hardware)

        api._AwattarApi__toggle_relay_if_appropriate(True)
        api._AwattarApi__toggle_relay_if_appropriate(False)

        hardware.relay.set_on_state.assert_has_calls([call(True), call(False)])

    def test_toggle_relay_should_fail_automation_overriden(self):
        hardware = Mock()
        api = AwattarApi(hardware)

        api.automation_overriden = True

        api._AwattarApi__toggle_relay_if_appropriate(True)

        hardware.relay.set_on_state.assert_not_called()

    def test_toggle_relay_should_reset_automation(self):
        hardware = Mock()
        api = AwattarApi(hardware)

        hardware.relay.get_on_state.return_value = True
        api.automation_overriden = True

        api._AwattarApi__toggle_relay_if_appropriate(True)

        assert not api.automation_overriden

    async def test_react_to_price_change_should_toggle_relay_off(self):
        hardware = Mock()
        api = AwattarApi(hardware)
        mock_relay_toggle_function = Mock()
        api._AwattarApi__toggle_relay_if_appropriate = mock_relay_toggle_function

        api.price_threshold_eur = 200

        too_high_price = 250
        time_till_execution = 0
        await uasyncio.run(
            await api._AwattarApi__react_to_price_change(
                time_till_execution, too_high_price
            )
        )

        mock_relay_toggle_function.assert_called_once_with(False)

    async def test_react_to_price_change_should_toggle_relay_on(self):
        hardware = Mock()
        api = AwattarApi(hardware)
        mock_relay_toggle_function = Mock()
        api._AwattarApi__toggle_relay_if_appropriate = mock_relay_toggle_function

        api.price_threshold_eur = 200

        low_enough_price = 180
        time_till_execution = 0
        await uasyncio.run(
            await api._AwattarApi__react_to_price_change(
                low_enough_price, time_till_execution
            )
        )

        mock_relay_toggle_function.assert_called_once_with(True)

    @patch("source.api.awattar.awattar_api.AwattarApi._AwattarApi__react_to_price_change")
    @patch("source.api.awattar.awattar_api.uasyncio")
    @patch("source.api.awattar.awattar_api.time")
    def test_create_scheduled_task(self, mock_time, mock_uasyncio, mock_react_to_price_change):
        warnings.simplefilter("ignore", RuntimeWarning)
        hardware = Mock()
        api = AwattarApi(hardware)
        time_of_execution = 1400
        price_at_time_of_execution = 250
        current_time = 800
        mock_time.time.return_value = current_time
        time_till_execution = time_of_execution - current_time

        api._AwattarApi__create_scheduled_task(
            time_of_execution, price_at_time_of_execution
        )

        mock_react_to_price_change.assert_called_once_with(time_till_execution, price_at_time_of_execution)
        mock_uasyncio.create_task.assert_called_once()
        assert len(api.tasks) == 1

    @patch("source.api.awattar.awattar_api.AwattarApi._AwattarApi__create_scheduled_task")
    @patch("source.api.awattar.awattar_api.urequests")
    def test_poll_api(self, mock_urequest, mock_create_task):
        mock_urequest.get().json.return_value = {
            "object": "list",
            "data": [
                {
                    "start_timestamp": 1671098400000,
                    "end_timestamp": 1671102000000,
                    "marketprice": 450.72,
                    "unit": "Eur/MWh"
                },
                {
                    "start_timestamp": 1671102000000,
                    "end_timestamp": 1671105600000,
                    "marketprice": 406.56,
                    "unit": "Eur/MWh"
                },
                {
                    "start_timestamp": 1671105600000,
                    "end_timestamp": 1671109200000,
                    "marketprice": 396.53,
                    "unit": "Eur/MWh"
                }
            ],
            "url": "/de/v1/marketdata"
        }

        hardware = Mock()
        api = AwattarApi(hardware)

        api._AwattarApi__poll_api()

        assert mock_create_task.call_count == 3
