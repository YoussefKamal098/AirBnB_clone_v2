#!/usr/bin/python3
"""FileStorage module - Handles file storage operations for objects"""

import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """FileStorage class - Handles file storage operations for objects"""

    __file_path = "file.json"
    __objects = {}
    __MODELS = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def all(self):
        """Returns the dictionary of stored objects.

        Returns:
            dict: The dictionary containing all stored objects.
        """
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage.

        Parameter:
            obj (BaseModel): The object to add.
        """
        if not obj or type(obj) not in self.get_models_classes():
            return

        model_name = obj.__class__.__name__
        key = FileStorage._get_obj_key(model_name, obj.id)

        self.__objects[key] = obj

    def save(self):
        """Serializes objects to JSON and saves to file"""
        serialized_objects = {
            key: obj.to_dict()
            for key, obj in self.__objects.items()
        }

        with open(self.__file_path, "w") as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Deserializes JSON from file and reloads objects"""

        if not os.path.isfile(self.__file_path):
            return

        try:
            with open(self.__file_path, "r") as file:
                deserialized_objects = json.load(file)

                self.__objects = {
                    key: self._deserialize(dictionary)
                    for key, dictionary in deserialized_objects.items()
                }

        except (OSError, json.JSONDecodeError):
            pass

    def find_obj(self, model_name, _id):
        """
        Finds and returns an object by model name and ID
        Parameters:
            model_name (str): the name of the model
            _id (str): the ID of the object
        Returns:
            The object if found, otherwise None
        """
        if model_name not in self.get_models_names() or not _id:
            return None

        key = FileStorage._get_obj_key(model_name, _id)
        if key not in self.__objects:
            print("** no instance found **")
            return None

        return self.__objects.get(key)

    def remove_obj(self, model_name, _id):
        """
        Removes an object from storage by model name and ID
        Parameters:
            model_name (str): the name of the model
            _id (str): the ID of the object
        """
        obj = self.find_obj(model_name, _id)
        if not obj:
            return

        key = FileStorage._get_obj_key(model_name, _id)

        del self.__objects[key]
        self.save()

    def find_all(self, model_name=""):
        """
        Finds and returns all objects of a given model
        Parameters:
            model_name (str): the name of the model
        Returns:
            A list of objects if found, otherwise an empty list
        """
        if not model_name:
            return [str(obj) for key, obj in self.__objects.items()]

        if model_name not in self.get_models_names():
            return []

        return [str(obj) for key, obj in self.__objects.items()
                if obj.__class__.__name__ == model_name]

    def update_obj_attribute(self, model_name, _id, **kwargs):
        """
        Updates an attribute of an object by
        model name, ID, and attribute name/value pair
        Parameters:
            model_name (str): the name of the model
            _id (str): the ID of the object
            **kwargs: keyword arguments representing attribute name/value pair
        """
        obj = self.find_obj(model_name, _id)
        if not obj:
            return

        attribute_name = kwargs.get("attribute_name")
        attribute_value = kwargs.get("attribute_value")

        if not attribute_name or not attribute_value:
            return

        FileStorage._update_obj_attribute(obj, attribute_name, attribute_value)
        self.save()

    def update_obj_attributes(self, model_name, _id, **kwargs):
        """Updates attributes of an object identified by model name and ID.

        This function takes a model name (string), an object ID (str), and
        keyword arguments representing the attributes to update.
        It iterates through the keyword arguments and calls a separate
        function (presumably `update_obj_attribute`) to update each
        attribute of the specified object.

        Parameters:
            model_name (str): The name of the model the object belongs to.
            _id (str): The ID of the object to update.
            **kwargs: Keyword arguments where the key represents
            the attribute name and the value represents the new
            attribute value.
        """
        for key, value in kwargs.items():
            self.update_obj_attribute(
                model_name, _id, attribute_name=key, attribute_value=value)

    @staticmethod
    def _update_obj_attribute(obj, attribute_name, value):
        """
        Updates an attribute of an object
        Parameters:
            obj (BaseModel): the object to update
            attribute_name (str): the name of the attribute
            value (any): the new value of the attribute
        """
        if not obj or not isinstance(attribute_name, str):
            return

        if not hasattr(obj, attribute_name):
            setattr(obj, attribute_name, value)
            return

        attribute = getattr(obj, attribute_name)
        if attribute_name.startswith("__") or attribute_name.startswith("_"):
            return

        if callable(attribute):
            return

        attribute_type = type(attribute)
        if not isinstance(value, (str, attribute_type)):
            return

        setattr(obj, attribute_name, attribute_type(value))

    def count(self, model_name):
        """
        Count and returns number of objects of a given model
        Parameters:
            model_name (str): the name of the model
        Returns:
            number of objects of a given model if found, otherwise None
        """
        if not model_name:
            return None

        if model_name not in self.get_models_names():
            return None

        return sum(1 for key in self.__objects.keys()
                   if key.startswith(model_name))

    def _deserialize(self, dictionary):
        """
        Deserializes a dictionary into an object
        Parameters:
            dictionary (dict[str, any]): the dictionary to deserialize
        Returns:
            An object if deserialization is successful of (BaseModel),
            otherwise None
        """
        if dictionary is None:
            return None

        model_name = dictionary.get("__class__")
        if not model_name:
            return None

        model_class = self.get_model_class(model_name)
        if not model_class:
            return None

        return model_class(**dictionary)

    @staticmethod
    def _get_obj_key(model_name, _id):
        """
        Generates a unique key for an object based on model name and ID
        Parameters:
            model_name (str): the name of the model
            _id (str): the ID of the object
        Returns:
            The generated key (str)
        """
        if not model_name or not _id:
            return None

        return f"{model_name}.{_id}"

    def get_models_classes(self):
        """Returns a tuple of model classes"""
        return tuple(self.__MODELS.values())

    def get_models_names(self):
        """Returns a tuple of model names"""
        return tuple(self.__MODELS.keys())

    def get_model_class(self, model_name):
        """
        Returns the class corresponding to a model name
        Parameters:
            model_name (str): the name of the model
        Returns:
            The class if found (BaseModel), otherwise None
        """
        if model_name not in self.get_models_names():
            print("** class doesn't exist **")
            return None

        return self.__MODELS.get(model_name)
