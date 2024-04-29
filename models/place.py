"""
This module defines the Place class, which inherits from the BaseModel class.

Classes:
    - Place

Attributes:
    - city_id (str): The ID of the city where the place is located.
    - user_id (str): The ID of the user who owns the place.
    - name (str): The name of the place.
    - description (str): A description of the place.
    - number_rooms (int): The number of rooms in the place.
    - number_bathrooms (int): The number of bathrooms in the place.
    - max_guest (int): The maximum number of guests allowed in the place.
    - price_by_night (int): The price per night to stay at the place.
    - latitude (float): The latitude coordinate of the place.
    - longitude (float): The longitude coordinate of the place.
    - amenity_ids (List[str]): A list of IDs of amenities available
    at the place.

Methods:
    - No additional methods.

"""

from models.base_model import BaseModel
from typing import List


class Place(BaseModel):
    """
    Place class represents a lodging place.

    Attributes:
        - city_id (str): The ID of the city where the place is located.
        - user_id (str): The ID of the user who owns the place.
        - name (str): The name of the place.
        - description (str): A description of the place.
        - number_rooms (int): The number of rooms in the place.
        - number_bathrooms (int): The number of bathrooms in the place.
        - max_guest (int): The maximum number of guests allowed in the place.
        - price_by_night (int): The price per night to stay at the place.
        - latitude (float): The latitude coordinate of the place.
        - longitude (float): The longitude coordinate of the place.
        - amenity_ids (List[str]): A list of IDs of amenities available
        at the place.

    Methods:
        - No additional methods.
    """

    city_id: str = ""
    user_id: str = ""
    name: str = ""
    description: str = ""
    number_rooms: int = 0
    number_bathrooms: int = 0
    max_guest: int = 0
    price_by_night: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    amenity_ids: List[str] = []
