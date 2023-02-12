# Config Manager

The config Manager is used throughout this project to retrieve and save information from a config file. While it is mostly used to handle the global konfiguration of this Projekt, it is also used by APIs to handle their individual configuration.

To use the config manager, you first have to use the constructor of the config manager and provide the path to your json config file:

```
config_manager = ConfigManager("/path/to/config.json")
```

to set and retrieve variables you can use the following methods.

```
config_manager.set_value("NAME_OF_VALUE", "actual_value")
config_manager.get_value("NAME_OF_VALUE")
```
