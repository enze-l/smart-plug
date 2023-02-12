import json

STANDARD_CONFIG_FILE_PATH = "config.json"


class ConfigManager:
    def __init__(self, config_file_path):
        self._config_file_path = config_file_path

    def get_value(self, key):
        return self.__get_dictionary()[key]

    def set_value(self, key, value):
        dictionary = self.__get_dictionary()
        dictionary[key] = value
        file = open(self._config_file_path, "w")
        file.write(json.dumps(dictionary, separators=(",\n", " : ")))
        file.close()

    def __get_dictionary(self):
        file = open(self._config_file_path)
        dictionary = json.loads(file.read())
        file.close()
        return dictionary
