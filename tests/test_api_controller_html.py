from unittest import TestCase
from unittest.mock import Mock, patch
from source.api.api_controller_html import generate_html


class TestAPIControllerHTML(TestCase):
    @patch("source.api.api_controller_html.os")
    def test_generate_html(self, mock_os):
        mock_api = Mock()
        mock_api.get_html_options.return_value = "<p> Mock Content <p/>"
        current_html_name = "test_api"

        test_html = generate_html(mock_api, current_html_name)
        expected_html = """
            <html>
              <head>
                <title>Smart-Plug</title>
                <style>
                    .container {
                        margin-left: auto;
                        margin-right: auto;
                        width: 24em;
                        display: flex;
                    }
                    input, select {
                        width: 12em;
                    }
                </style>
              </head>
              <body>
                <div class="container">
                    <h>API Selection<h/>
                    <form method="post">
                        <select name="api" id="api"></select>
                        <input type="submit" value="Set API">
                    </form>
                    <h>test_api Settings<h>
                    <p> Mock Content <p/>
                <div/>
              </body>
            </html>"""

        assert expected_html.replace(" ", "") in test_html.replace(" ", "")


