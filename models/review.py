#!/usr/bin/python3
"""
This module defines the Review class, which inherits from the BaseModel class.
"""
import os

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')

parent_classes = (
    BaseModel,
    Base if STORAGE_TYPE == "db" else object
)


class Review(*parent_classes):
    """
    Review class represents a review of a place.
    """
    if STORAGE_TYPE == "db":
        __tablename__ = 'reviews'

        text = Column(String(1024), nullable=False)
        place_id = Column(String(60),
                          ForeignKey('places.id', ondelete="CASCADE"),
                          nullable=False)
        user_id = Column(String(60),
                         ForeignKey('users.id', ondelete="CASCADE"),
                         nullable=False)
        user = relationship('User', back_populates='reviews')
        place = relationship('Place', back_populates='reviews')

    else:
        place_id: str = ""
        user_id: str = ""
        text: str = ""
