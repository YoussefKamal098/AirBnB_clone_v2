#!/usr/bin/python3
"""FileStorage module - Handles file storage operations for objects"""

import json
import os

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
            return {}

        return {key: obj for key, obj in self.__objects.items()
                if obj.__class__ == cls}

    def new(self, obj):
        """Adds a new object to the storage.

        Parameter:
            obj (BaseModel): The object to add.
        """
        if not obj or type(obj) not in self.get_classes():
            return

        key = self._get_obj_key(obj.__class__.__name__, obj.id)
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

        key = self._get_obj_key(obj.__class__.__name__, obj.id)
        self.__objects.pop(key, None)

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
        return self.__objects.get(key, None)

    def find_all(self, class_name=""):
        """
        Finds and returns all objects of a given class
        Parameters:
            class_name (str): the name of the class
        Returns:
            A list of objects if found, otherwise an empty list
        """
        if not class_name:
            return [str(obj) for obj in self.__objects.values()]

        if class_name not in self.get_classes_names():
            return []

        return [str(obj) for key, obj in self.__objects.items()
                if obj.__class__.__name__ == class_name]

    def update(self, obj=None, **kwargs):
        """
        Updates attributes of a given object with new
        values provided in kwargs.

        This method takes an object and a set of keyword
        arguments representing attribute-value pairs.
        It updates the object's attributes with the provided values.

        Parameters:
            obj (BaseModel): The object to be updated. If None or the
                        object type is not among the recognized classes,
                        the method returns without making any changes.
            **kwargs: Arbitrary keyword arguments representing
                    the attribute names and their new values
                    to update on the object.
        """
        if not obj or type(obj) not in self.get_classes():
            return

        for attr, value in kwargs.items():
            setattr(obj, attr, value)

    def count(self, class_name):
        """
        Count and returns number of objects of a given class name
        Parameters:
            class_name (str): the name of the class
        Returns:
            number of objects of a given model if found, otherwise None
        """
        if not class_name or class_name not in self.get_classes_names():
            return 0

        return sum(1 for key in self.__objects.keys()
                   if key.startswith(class_name))

    def close(self):
        """
        Reload the object state from the database.

        This method is intended to refresh the current instance with the latest
        data from the database, ensuring that any changes made by other
        transactions are reflected in the current instance.
        """
        self.reload()

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

        class_name = dictionary.get("__class__", None)
        if not class_name:
            return None

        _class = self.get_class(class_name)
        if not _class:
            return None

        return _class(**dictionary)
