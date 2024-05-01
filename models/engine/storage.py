#!/usr/bin/python3

from abc import ABC, abstractmethod

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class Storage(ABC):
    __CLASSES = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    @abstractmethod
    def all(self, cls=None):
        pass

    @abstractmethod
    def new(self, obj):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def reload(self):
        pass

    @abstractmethod
    def delete(self, obj=None):
        pass

    @abstractmethod
    def find(self, class_name, _id):
        pass

    @abstractmethod
    def remove(self, class_name, _id):
        pass

    @abstractmethod
    def find_all(self, class_name=""):
        pass

    @abstractmethod
    def update(self, class_name, _id, **kwargs):
        pass

    @abstractmethod
    def count(self, class_name):
        pass

    @staticmethod
    def _get_obj_key(class_name, _id):
        """
        Generates a unique key for an object based on class name and ID
        Parameters:
            class_name (str): the name of the class
            _id (str): the ID of the object
        Returns:
            The generated key (str)
        """
        if not class_name or not _id:
            return None

        return f"{class_name}.{_id}"

    def get_classes(self):
        """Returns a tuple of classes"""
        return tuple(self.__CLASSES.values())

    def get_classes_names(self):
        """Returns a tuple of model names"""
        return tuple(self.__CLASSES.keys())

    def get_class(self, class_name):
        """
        Returns the class corresponding to a class name
        Parameters:
            class_name (str): the name of the class
        Returns:
            The class if found (BaseModel), otherwise None
        """
        if class_name not in self.get_classes_names():
            print("** class doesn't exist **")
            return None

        return self.__CLASSES.get(class_name)
