#!/usr/bin/python3
"""
This module defines the Place class, which inherits from the BaseModel class.
"""
import os
from typing import List

from sqlalchemy import Column, Float, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')

parent_classes = (
    BaseModel,
    Base if STORAGE_TYPE == "db" else object
)


class Place(*parent_classes):
    """
    Place class represents a lodging place.
    """
    if STORAGE_TYPE == "db":
        __tablename__ = 'places'

        city_id = Column(String(60),
                         ForeignKey('cities.id', ondelete="CASCADE"),
                         nullable=False)
        user_id = Column(String(60),
                         ForeignKey('users.id', ondelete="CASCADE"),
                         nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        user = relationship('User', back_populates='places')
        city = relationship('City', back_populates='places')
        reviews = relationship('Review', back_populates='place',
                               passive_deletes=True)
        amenities = relationship('Amenity', secondary='place_amenity',
                                 back_populates='place_amenities')

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
            """
            Retrieves the reviews associated with the place.

            Returns:
                list: A list of Review objects associated with the place.
            """
            from models import storage

            related_reviews = []
            reviews = storage.all(Review)

            for review in reviews.values():
                if review.place_id == self.id:
                    related_reviews.append(review)

            return related_reviews

        @property
        def amenities(self):
            """
            Retrieves the amenities associated with the place.

            Returns:
                list: A list of Amenity objects associated with the place.
            """
            from models import storage

            amenities = storage.all(Amenity)
            related_places = []

            for amenity in amenities.values():
                if amenity.id in self.amenity_ids:
                    related_places.append(amenity)

            return related_places

        @amenities.setter
        def amenities(self, obj):
            """
            adding an amenity object to place,
            accepts only Amenity objects

            Parameters:
                obj: An Amenity object to be associated with the place.
            """
            if not obj:
                return
            if not isinstance(obj, Amenity):
                return

            if obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)


if STORAGE_TYPE == "db":
    place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column(
            'place_id', String(60),
            ForeignKey('places.id'),
            primary_key=True
        ),
        Column(
            'amenity_id', String(60),
            ForeignKey('amenities.id'),
            primary_key=True
        )
    )
