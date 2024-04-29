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

from models.base_model import BaseModel


class User(BaseModel):
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

    email: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""
