#!/usr/bin/python3
"""
This module defines a dictionary of classes used in the application.
"""

from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.dict_wrapper import FrozenDict

CLASSES = FrozenDict({
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
})
