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
import os
from typing import List

from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base
from models.review import Review
import models


class Place(BaseModel, Base):
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
    __tablename__ = 'places'
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        city_id = Column(String(60), ForeignKey('cities.id', ondelete="CASCADE"), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        user = relationship('User', back_populates='places')
        cities = relationship('City', back_populates='places')
        reviews = relationship('Review', back_populates='place', passive_deletes=True)

    else:
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

        @property
        def reviews(self):
            related_reviews = []
            reviews = models.storage.all(Review)

            for review in reviews.values():
                if review.place_id == self.id:
                    related_reviews.append(review)

            return related_reviews
