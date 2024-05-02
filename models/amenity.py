"""
This module defines the Amenity class, which inherits
from the BaseModel class.
"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class represents amenities available in a place.
    """

    name: str = ""
