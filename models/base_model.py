#!/usr/bin/python3
"""
This module contains the BaseModel class, which serves
as the base class for all models in the application.
"""
import os
from uuid import uuid4
from datetime import datetime

from sqlalchemy import Column, String, DATETIME
from sqlalchemy.orm import declarative_base

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')

Base = declarative_base()


class BaseModel:
    """
    Base class for all models.
    """

    if STORAGE_TYPE == 'db':
        id = Column(String(60), primary_key=True)
        created_at = Column(DATETIME, nullable=False,
                            default=datetime.now)
        updated_at = Column(DATETIME, nullable=False,
                            default=datetime.now,
                            onupdate=datetime.now)

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.

        Parameters:
        - *args: Variable-length argument list.
        - **kwargs: Arbitrary keyword arguments.
        """
        self.id = kwargs.pop("id", str(uuid4()))

        value = kwargs.pop("updated_at", None)
        self.updated_at = datetime.fromisoformat(value) \
            if value else datetime.now()

        value = kwargs.pop("created_at", None)
        self.created_at = datetime.fromisoformat(value) \
            if value else datetime.now()

        kwargs.pop("__class__", None)

        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def save(self):
        """
        Saves the current object instance to persistent storage.

        This method uses the `storage` object from the `models` module to
        persist the current object's state. It performs the following actions:

        1. Calls `storage.new(self)` to register the object with
        the storage system.
        2. Calls `storage.save()` to commit the changes and save the object to
           persistent storage (e.g., database).

        Raises:
            Exception: Any exception raised by the underlying storage system
                       during the save operation.
        """
        from models import storage

        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the object.

        Returns:
        - dictionary (dict[str, any]): Dictionary containing object attributes.
        """

        dictionary = dict(self.__dict__)

        dictionary["created_at"] = getattr(self, "created_at").isoformat()
        dictionary["updated_at"] = getattr(self, "updated_at").isoformat()
        dictionary["__class__"] = f"{self.__class__.__name__}"

        dictionary.pop("_sa_instance_state", None)

        return dictionary

    def delete(self):
        from models import storage

        storage.delete(self)

    def update(self, **kwargs):
        from models import storage

        storage.update(self, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
        - str: String representation of the object.
        """
        dictionary = dict(self.__dict__)
        dictionary.pop("_sa_instance_state", None)

        return f"[{self.__class__.__name__}] ({self.id}) {dictionary}"

    if STORAGE_TYPE != 'db':
        def __setattr__(self, key, value):
            object.__setattr__(self, "updated_at", datetime.now())
            object.__setattr__(self, key, value)
