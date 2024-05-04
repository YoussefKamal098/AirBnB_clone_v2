#!/usr/bin/python3
"""FileStorage module - Handles file storage operations for objects"""

import os
import json
from datetime import datetime

from models.base_model import BaseModel
from models.engine.storage import Storage


class FileStorage(Storage):
    """FileStorage class - Handles file storage operations for objects"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Retrieve all objects stored in the storage instance.

        If no specific class is provided, returns all objects of all classes.
        If a class is provided, returns all objects of that class type.

        Parameters:
            cls (class, optional): The class type to filter the objects.
            If not provided, returns all objects regardless of class type.

        Returns:
            dict or None: A dictionary containing all objects if cls is None.
                If cls is provided, and it exists in the stored classes,
                returns a dictionary containing objects of the specified
                class type. Returns None if cls is provided but not found in
                the stored classes.
        """
        if not cls:
            return self.__objects

        if cls not in self.get_classes():
            return None

        return {key: obj for key, obj in self.__objects.items()
                if obj.__class__ == cls}

    def new(self, obj):
        """Adds a new object to the storage.

        Parameter:
            obj (BaseModel): The object to add.
        """
        if not obj or type(obj) not in self.get_classes():
            return

        class_name = obj.__class__.__name__
        key = self._get_obj_key(class_name, obj.id)

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

                FileStorage.__objects = {
                    key: self._deserialize(dictionary)
                    for key, dictionary in deserialized_objects.items()
                }

        except (OSError, json.JSONDecodeError):
            pass

    def delete(self, obj=None):
        """
        Delete the given object from storage if it exists.

        Parameters:
            obj (BaseModel, optional): The object to delete from storage.
                If not provided or if the object is not an instance of any
                class managed by the storage, the method does nothing.

        Returns:
            None
        """
        if not obj or type(obj) not in self.get_classes():
            return

        class_name = obj.__class__.__name__
        key = self._get_obj_key(class_name, obj.id)

        if key in self.__objects:
            del self.__objects[key]

    def find(self, class_name, _id):
        """
        Finds and returns an object by class name and ID
        Parameters:
            class_name (str): the name of the class
            _id (str): the ID of the object
        Returns:
            The object if found, otherwise None
        """
        if class_name not in self.get_classes_names() or not _id:
            return None

        key = self._get_obj_key(class_name, _id)
        if key not in self.__objects:
            print("** no instance found **")
            return None

        return self.__objects.get(key)

    def remove(self, class_name, _id):
        """
        Removes an object from storage by class name and ID
        Parameters:
            class_name (str): the name of the class
            _id (str): the ID of the object
        """
        obj = self.find(class_name, _id)
        if not obj:
            return

        key = self._get_obj_key(class_name, _id)

        del self.__objects[key]

    def find_all(self, class_name=""):
        """
        Finds and returns all objects of a given class
        Parameters:
            class_name (str): the name of the class
        Returns:
            A list of objects if found, otherwise an empty list
        """
        if not class_name:
            return [str(obj) for key, obj in self.__objects.items()]

        if class_name not in self.get_classes_names():
            return []

        return [str(obj) for key, obj in self.__objects.items()
                if obj.__class__.__name__ == class_name]

    def update(self, class_name, _id, **kwargs):
        """Updates attributes of an object identified by class name and ID.

        This function takes a class name (string), an object ID (str), and
        keyword arguments representing the attributes to update. It iterates
        through the keyword arguments and calls a separate
        function (presumably `update_obj_attribute`) to update each
        attribute of the specified object.

        Parameters:
            class_name (str): The name of the class the object belongs to.
            _id (str): The ID of the object to update.
            **kwargs: Keyword arguments where the key represents
            the attribute name and the value represents the new
            attribute value.
        """
        obj = self.find(class_name, _id)
        if not obj:
            return

        for key, value in kwargs.items():
            self._update_attribute(
                obj, attribute_name=key, attribute_value=value)

        obj.updated_at = datetime.now()

    @staticmethod
    def _update_attribute(obj, attribute_name, attribute_value):
        """
        Updates an attribute of an object
        Parameters:
            obj (BaseModel): the object to update
            attribute_name (str): the name of the attribute
            attribute_value (any): the new value of the attribute
        """
        if not obj or not isinstance(attribute_name, str):
            return

        if not hasattr(obj, attribute_name):
            raise AttributeError(f"{obj.__class__.__name__}"
                                 f"not have {attribute_name} attribute")

        if attribute_name.startswith("__") or attribute_name.startswith("_"):
            raise ValueError(f"can't assign {attribute_name}"
                             f"attribute to class {obj.__class__.__name__}")

        attribute = getattr(obj, attribute_name)
        if callable(attribute):
            raise ValueError(f"can't assign {attribute_name}"
                             f"attribute to class {obj.__class__.__name__}")

        attribute_type = type(attribute)
        if not isinstance(attribute_value, attribute_type):
            raise ValueError(f"{attribute_name}"
                             f"must by {attribute_type.__class.__name__}")

        setattr(obj, attribute_name, attribute_type(attribute_value))

    def count(self, class_name):
        """
        Count and returns number of objects of a given class name
        Parameters:
            class_name (str): the name of the class
        Returns:
            number of objects of a given model if found, otherwise None
        """
        if not class_name:
            return None

        if class_name not in self.get_classes_names():
            return None

        return sum(1 for key in self.__objects.keys()
                   if key.startswith(class_name))

    def close(self):
        """Clean up the storage connection"""
        pass

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

        class_name = dictionary.pop("__class__", None)
        if not class_name:
            return None

        _class = self.get_class(class_name)
        if not _class:
            return None

        return _class(**dictionary)
