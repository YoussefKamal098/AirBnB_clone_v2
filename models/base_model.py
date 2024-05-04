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

Base = declarative_base()


class BaseModel:
    """
    Base class for all models.
    """

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        id = Column(String(60), primary_key=True)
        created_at = Column(DATETIME, nullable=False,
                            default=datetime.utcnow)
        updated_at = Column(DATETIME, nullable=False,
                            default=datetime.utcnow,
                            onupdate=datetime.utcnow)

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

        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def save(self):
        """
        Saves the current object state to storage.
        """
        from models import storage

        self.updated_at = datetime.now()
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

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
        - str: String representation of the object.
        """
        dictionary = dict(self.__dict__)
        dictionary.pop("_sa_instance_state", None)

        return f"[{self.__class__.__name__}] ({self.id}) {dictionary}"
