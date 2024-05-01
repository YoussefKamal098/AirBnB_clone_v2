#!/usr/bin/python3
"""
This module contains the BaseModel class, which serves
as the base class for all models in the application.
"""

from uuid import uuid4
from datetime import datetime
from copy import deepcopy
import models


class BaseModel:
    """
    Base class for all models.
    """

    __DATE_ATTRIBUTES = ["created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.

        Parameters:
        - *args: Variable-length argument list.
        - **kwargs: Arbitrary keyword arguments.
        """

        self.id = kwargs.pop("id", str(uuid4()))
        for attr in self.__DATE_ATTRIBUTES:
            value = kwargs.pop(attr, None)
            setattr(self, attr,
                    datetime.fromisoformat(value) if value
                    else datetime.now())

        for attr, value in deepcopy(kwargs).items():
            if attr.startswith("__") or attr.startswith("_"):
                del kwargs[attr]
                continue

            setattr(self, attr, value)

    def save(self):
        """
        Saves the current object state to storage.
        """

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the object.

        Returns:
        - dictionary (dict[str, any]): Dictionary containing object attributes.
        """

        dictionary = dict(self.__dict__)

        for attribute in self.__DATE_ATTRIBUTES:
            dictionary[attribute] = getattr(self, attribute).isoformat()

        dictionary["__class__"] = f"{self.__class__.__name__}"
        return dictionary

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
        - str: String representation of the object.
        """

        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
