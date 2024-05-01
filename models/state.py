#!/usr/bin/python3
import os

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base
from models.city import City
import models


class State(BaseModel, Base):
    __tablename__ = 'states'

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        name = Column(String(128), nullable=False, index=True)
        cities = relationship('City', back_populates='state', passive_deletes=True)
    else:
        name: str = ""

        @property
        def cities(self):
            related_cities = []
            cities = models.storage.all(City)

            for city in cities.values():
                if city.state_id == self.id:
                    related_cities.append(city)

            return related_cities

