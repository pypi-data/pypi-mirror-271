import os
import json
import yaml
import logging

class configContainer:
    def __init__(self, path, filename, type):
        self.path = path
        self.filename = filename
        self.type = type
        self.data = {}
        self.load()

    def load(self):
        if self.type == "json":
            self.loadJSON()
        elif self.type == "yaml":
            self.loadYAML()
        else:
            raise TypeError(f"Type '{self.type}' is not supported, use 'json' or 'yaml' instead.")

    def loadJSON(self):
        os.makedirs(self.path, exist_ok=True)
        file_path = os.path.join(self.path, f"{self.filename}.json")
        if not os.path.isfile(file_path):
            with open(file_path, "w") as file:
                json.dump({}, file)
        with open(file_path, "r") as file:
            self.data = json.load(file) or {}

    def loadYAML(self):
        os.makedirs(self.path, exist_ok=True)
        file_path = os.path.join(self.path, f"{self.filename}.yaml")
        if not os.path.isfile(file_path):
            with open(file_path, "w") as file:
                file.write("{}")
        with open(file_path, "r") as file:
            try:
                self.data = yaml.safe_load(file) or {}
            except Exception as e:
                logging.error(f"Failed to load YAML file {file_path}: {e}")
                self.data = {}

    def registerValues(self, config):
        for key, value in config.items():
            self.__register(key, value)

    def __register(self, key, value):
        if key not in self.data:
            self.data[key] = value
            self.__save()

    def __save(self):
        if self.type == "json":
            self.__saveJSON()
        elif self.type == "yaml":
            self.__saveYAML()
        else:
            raise TypeError(f"Type '{self.type}' is not supported, use 'json' or 'yaml' instead.")

    def __saveJSON(self):
        with open(os.path.join(self.path, f"{self.filename}.json"), "w") as file:
            json.dump(self.data, file, indent=4)

    def __saveYAML(self):
        with open(os.path.join(self.path, f"{self.filename}.yaml"), "w") as file:
            yaml.dump(self.data, file)

    def get(self, key):
        return self.data.get(key)

    def getValue(self, key):
        value = self.data.get(key)
        return value['value'] if isinstance(value, dict) else value

    def setValue(self, key, value):
        self.data[key] = value
        self.__save()

    def changeType(self, key, type):
        self.data[key] = type(self.data[key])
        self.__save()

    def reload(self):
        self.load()
        return self.data