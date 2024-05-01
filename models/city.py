#!/usr/bin/python3
import os

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    __tablename__ = 'cities'

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        name = Column(String(128), nullable=False, index=True)
        state_id = Column(String(60), ForeignKey('states.id', ondelete="CASCADE"), nullable=False)
        state = relationship("State", back_populates="cities")

    else:
        name: str = ""
        state_id: str = ""
