#!/usr/bin/python3
"""
This module contains the BaseModel class, which serves
as the base class for all models in the application.
"""

from uuid import uuid4
from datetime import datetime
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

        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
            return

        self._assign_attributes(**kwargs)

    def _assign_attributes(self, **kwargs):
        """
        Assigns attributes to the object based on the provided kwargs.

        Parameters:
        - **kwargs: Arbitrary keyword arguments.
        """

        attributes = tuple(kwargs.keys())
        for attribute in attributes:
            if attribute.startswith("__") or attribute.startswith("_"):
                del kwargs[attribute]

        for attribute, value in kwargs.items():
            if attribute in self.__DATE_ATTRIBUTES:
                setattr(self, attribute, datetime.fromisoformat(value))
                continue

            setattr(self, attribute, value)

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
