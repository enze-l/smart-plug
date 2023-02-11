# Smart-Plug

A development platform with an interchangeable API for smart-plugs that utilize an esp32 (untested on esp8266) chipset. It is tested on a [Shelly Plus 1PM](https://www.shelly.cloud/de/products/product-overview/2xspl1pm/shelly-plus-1-pm)

# Development Setup

## Prerequisites
- [python](https://www.python.org/downloads/)
- [make](https://wiki.ubuntuusers.de/Makefile/)

## Installation Development Pipeline
1. clone this repository
2. install pipenv to manage additional dependencies:

   ```python -m pip install --upgrade pipenv```
3. install all other necessary dependencies:

   ```make development-dependencies```

# Device Setup (Reference Hardware)
Since this process may differ for each hardware this guide may need alteration to work on other platforms. Only proceed if you have already set up your Development Pipeline.

1. Connect the hardware with an UART-Converter while EN is grounded.
2. Install micropython by running ```make install-firmware```. If your device is not recognized under the default path you may need to change its preconfigured path by modifying ```BOARD_PORT``` in the [Makefile](Makefile). If you're not utilizing the reference hardware you need to provide your own [micropython firmware](https://micropython.org/download/).
3. Make a copy of [/source/config/sample_config.py](./source/config/sample_config.py) in the same directory ```cp config_sample.json config.json```
4. Replace the sample name and password for the wifi with your own ones
5. replace the values for the relay, gate and buttons with your own ones. If you're using the [reference hardware](https://www.shelly.cloud/de/products/product-overview/2xspl1pm/shelly-plus-1-pm), you can just stick to the predefined values 
6. Execute ```make deploy-run``` to copy the code in [source](./source) to the device and execute it.
 
## Development Utilities

There are some utility functions defined in the [Makefile](./Makefile) of this Project.
They should simplify the development cycle by defining different stages. You can use them for running tests, linting, installing dependencies etc.

Install all required development dependencies:
```make development-dependencies```

Install the Micropython firmware onto the microcontroller:
```make install-firmware```

Run unit-tests:
```make unit-test```

Run linter:
```make lint```

Fix formatting:
```make fix-lint```

Run tests and check linting:
```make test```

Deploy code onto the microcontroller:
```make deploy```

Run the code by executing the main.py file:
```make run```

Deploy and execute the main.py file:
```make deploy-run```

Run a development server used for testing the websocket API:
```make websocket-server```

# Documentation

All components of this project are documented wherever their code resides. To get an overview of important components, here is a table of contents for them:

- [hardware](./source/hardware/README.md)
- [config manager](./source/config/README.md)
- [apis implementation guidelines](./source/api/README.md)
  - [awattar api](./source/api/implementations/awattar/README.md)
  - [websocket api](./source/api/implementations/websocket/README.md)


