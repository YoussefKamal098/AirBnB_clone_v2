"""
This module defines the Amenity class, which inherits
from the BaseModel class.

Classes:
    - Amenity

Attributes:
    - name (str): The name of the Amenity.

Methods:
    - No additional methods.

"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class represents amenities available in a place.

    Attributes:
        - name (str): The name of the Amenity.

    Methods:
        - No additional methods.
    """

    name: str = ""
