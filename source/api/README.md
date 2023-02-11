# API

One of the main goals of this project is to have an exchangeable api to explore different use-cases for a connected smart plug.

## Design Guidelines
To implement and use your own API you should follow the rules below:

1. Your API must reside in its own folder in the [implementations](./implementations) directory
2. It has to implement the [AbstractAPI class](abstract_api.py)
3. Its file has to be called "api.py" and its class name "API"
4. If possible, it has to be programmed to run asynchronously instead of utilizing threads. Running it with threads will break the "awattar API" due to a bug in Micropython
5. (optional) If you want to use the api straight away after bootup, you have to configure its usage under [config.json](../config.json) under "CURRENT_API"

You can use the "awattar" api as a reference and even copy and rename the "template_api" to simplify the process.
