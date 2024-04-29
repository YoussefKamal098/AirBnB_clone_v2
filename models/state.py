"""
This module defines the State class, which inherits from the BaseModel class.

Classes:
    - State

Attributes:
    - name (str): The name of the state.

Methods:
    - No additional methods.

"""

from models.base_model import BaseModel


class State(BaseModel):
    """
    State class represents a state.

    Attributes:
        - name (str): The name of the state.

    Methods:
        - No additional methods.
    """

    name: str = ""
