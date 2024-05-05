#!/usr/bin/python3
"""
This module defines the Amenity class, which inherits
from the BaseModel class.
"""
import os

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base

parent_classes = (
    BaseModel,
    Base if os.getenv('HBNB_TYPE_STORAGE') == "db" else object
)


class Amenity(*parent_classes):
    """
    Amenity class represents amenities available in a place.
    """

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = 'amenities'

        name = Column(String(128), nullable=False)
        place_amenities = relationship('Place',
                                       secondary='place_amenity',
                                       back_populates='amenities')
    else:
        name: str = ""
