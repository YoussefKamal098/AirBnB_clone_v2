"""
This module defines the Amenity class, which inherits
from the BaseModel class.
"""
import os

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
    Amenity class represents amenities available in a place.
    """

    __tablename__ = 'amenities'
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        name = Column(String(128), nullable=False)
        place_amenities = relationship('Place', secondary='place_amenity',
                                       viewonly=False,
                                       back_populates='amenities')
    else:
        name: str = ""
