# Smart-Plug

A smart plug with an interchangeable API

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
