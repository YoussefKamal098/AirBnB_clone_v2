#!/usr/bin/python3
"""
This module defines the City class,
which represents a city in the context of a geographic location.
"""
import os

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """
    City class represents a city within a geographic location.
    """
    __tablename__ = 'cities'

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        name = Column(String(128), nullable=False, index=True)
        state_id = Column(String(60),
                          ForeignKey('states.id', ondelete="CASCADE"),
                          nullable=False)
        state = relationship("State", back_populates="cities")
        places = relationship('Place', back_populates='cities',
                              passive_deletes=True)

        __table_args__ = (
            UniqueConstraint('name', 'state_id', name='_name_state_id_uc'),
        )
    else:
        name: str = ""
        state_id: str = ""
