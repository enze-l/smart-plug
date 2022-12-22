# API

One of the main goals of this project is to have an exchangeable api to explore different use-cases for a connected smart plug.

## Design Guidelines
To implement and use your own API you should follow the rules below:

1. Your API must reside in its own folder in [this](.) directory.
2. It has to implement the [AbstractAPI class](abstract_api.py)
3. Its file has to be called api.py and its class API
4. You have to configure to its usage in the [config.py](../config/config.py) under "API_NAME"

You can use the "awattar" api as a reference and even copy and rename the "template_api" to simplify the process.
