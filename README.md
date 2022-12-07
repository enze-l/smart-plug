# Smart-Plug

A development platform with an interchangeable API for smart-plugs that utilize esp32 (untested on esp8266) chipset.

# Installation
1. Install [micropython](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html) on the platform of your choice
2. make a copy of [/source/config/sample_config.py](./source/config/sample_config.py) in the same directory
3. rename the file to ```config.py```
4. replace the sample values for the wifi with your own ones
5. copy the content of [/source](./source) on onto your smart plug
6. execute the main method

# Development Setup

## Prerequisites
- [python](https://www.python.org/downloads/)
- make

## Installation
1. clone this repository
2. install pipenv to manage additional dependencies:

    ```python -m pip install --upgrade pipenv```
3. install all other necessary dependencies:
   
    ```make development-dependencies```
 
## Development Utilities

There are some utility functions defined in the [Makefile](./Makefile) of this Project.
They should simplify the development cycle by defining different stages. You can use them for running tests, linting, installing dependencies etc.

Run unit-tests:
```make unit-test```

Run linter:
```make lint```

Fix formatting:
```make fix-lint```

Run tests and check linting:
```make test```
