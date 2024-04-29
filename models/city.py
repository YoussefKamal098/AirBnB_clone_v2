"""
This module defines the City class, which inherits
from the BaseModel class.

Classes:
    - City

Attributes:
    - name (str): The name of the city.
    - state_id (str): The ID of the state to which the city belongs.

Methods:
    - No additional methods.

"""

from models.base_model import BaseModel


class City(BaseModel):
    """
    City class represents a city within a state.

    Attributes:
        - name (str): The name of the city.
        - state_id (str): The ID of the state to which the city belongs.

    Methods:
        - No additional methods.
    """

    name: str = ""
    state_id: str = ""
