"""
This module defines the Amenity class, which inherits
from the BaseModel class.
"""
import os

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """
    Amenity class represents amenities available in a place.
    """

    __tablename__ = 'amenities'
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        name = Column(String(128), nullable=False)
        place_amenities = relationship('Place',
                                       secondary='place_amenity',
                                       back_populates='amenities')
    else:
        name: str = ""
