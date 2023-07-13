#!/usr/bin/python3
"""Module for FileStorage class."""
import json


class FileStorage:
    """
    FileStorage class for serializing instances to a JSON file and deserializing JSON file to instances.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary __objects.
        """
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the JSON file (__file_path) exists;
        otherwise, do nothing).
        """
        try:
            with open(self.__file_path, 'r') as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    cls_name, obj_id = key.split('.')
                    module = __import__("models.{}".format(cls_name), fromlist=[cls_name])
                    cls = getattr(module, cls_name)
                    self.__objects[key] = cls(**value)
        except FileNotFoundError:
            pass
