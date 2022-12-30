# Awattar Api

This implementation is used to power up and down the consumer based on the prices conveyed by the electricity provider "Awattar". The Awattar Api enables to check the electricity prices 24 hours in advance (simplified, click [here](https://www.awattar.de/services/api) for more). It does so by sending a list describing at which point in time the price will change at to which level.

To make use of low energy prices the user of this implementation can set a maximum price. If the price for electricity is higher than the maximum, the consumer gets switched off. If the price is lower or as expensive as the maximum, the consumer gets switched on. The price can be set via the [config file](./api_config.py) by setting the variable "TURN_ON_THRESHOLD_EUR" to an appropriate value.
