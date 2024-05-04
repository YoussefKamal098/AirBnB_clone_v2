"""
This module defines the User class, which inherits from the BaseModel class.
"""
import os

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base

parent_classes = (
    BaseModel,
    Base if os.getenv('HBNB_TYPE_STORAGE') == "db" else object
)


class User(*parent_classes):
    """
    User class represents a user.
    """

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = 'users'

        email = Column(String(128), nullable=False, unique=True, index=True)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True, index=True)
        last_name = Column(String(128), nullable=True, index=True)
        places = relationship('Place', back_populates='user',
                              passive_deletes=True)
        reviews = relationship('Review', back_populates='user',
                               passive_deletes=True)

    else:
        email: str = ""
        password: str = ""
        first_name: str = ""
        last_name: str = ""
