"""
This module defines the User class, which inherits from the BaseModel class.

Classes:
    - User

Attributes:
    - email (str): The email address of the user.
    - password (str): The password of the user.
    - first_name (str): The first name of the user.
    - last_name (str): The last name of the user.

Methods:
    - No additional methods.

"""
import os

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """
    User class represents a user.

    Attributes:
        - email (str): The email address of the user.
        - password (str): The password of the user.
        - first_name (str): The first name of the user.
        - last_name (str): The last name of the user.

    Methods:
        - No additional methods.
    """
    __tablename__ = 'users'

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        email = Column(String(128), nullable=False, unique=True, index=True)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True, index=True)
        last_name = Column(String(128), nullable=True, index=True)
        places = relationship('Place', back_populates='user', passive_deletes=True)
        reviews = relationship('Review', back_populates='user', passive_deletes=True)

    else:
        email: str = ""
        password: str = ""
        first_name: str = ""
        last_name: str = ""
