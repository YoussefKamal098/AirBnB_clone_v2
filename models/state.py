#!/usr/bin/python3
"""
This module defines the State class, which inherits from the BaseModel class.
"""

import os

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base
from models.city import City

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')

parent_classes = (
    BaseModel,
    Base if STORAGE_TYPE == "db" else object
)


class State(*parent_classes):
    """
    State class represents a state.
    """

    if STORAGE_TYPE == "db":
        __tablename__ = 'states'

        name = Column(String(128), nullable=False, index=True)
        cities = relationship('City', back_populates='state',
                              passive_deletes=True)
    else:
        name = ""

        @property
        def cities(self):
            """
            Retrieves the cities associated with the state.

            Returns:
                list: A list of City objects associated with the state.
            """
            from models import storage

            related_cities = []
            cities = storage.all(City)

            for city in cities.values():
                if city.state_id == self.id:
                    related_cities.append(city)

            return related_cities
