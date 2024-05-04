#!/usr/bin/python3

"""
DBStorage Module

This module defines the DBStorage class which is responsible for interacting
with the MySQL database using SQLAlchemy.

Classes:
    - DBStorage: Implements database storage using SQLAlchemy.

"""

import os

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base
from models.engine.storage import Storage


class DBStorage(Storage):
    """
    DBStorage class Represents the database storage system using SQLAlchemy.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize the DBStorage instance.
        Connects to the database and creates a session.
        """
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        hbnb_env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db}", pool_pre_ping=True)

        if hbnb_env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Retrieve all objects of a given class from the database.

        Parameters:
            cls (class): The class of objects to retrieve.

        Returns:
            dict: A dictionary of objects, where keys are object IDs.

        """
        dictionary = {}

        if cls is None:
            for _class in self.get_classes():
                instances = self.__session.query(_class).all()
                class_name = _class.__name__
                for instance in instances:
                    key = self._get_obj_key(class_name, instance.id)
                    dictionary[key] = instance
        else:
            instances = self.__session.query(cls).all()
            class_name = cls.__name__
            for instance in instances:
                key = self._get_obj_key(class_name, instance.id)
                dictionary[key] = instance

        return dictionary

    def new(self, obj):
        """
        Adds a new object to the database session.

        Parameters:
            obj: The object to add.

        Raises:
            Exception: If adding the object fails.

        """
        if not obj:
            return

        try:
            self.__session.add(obj)
            self.__session.flush()
        except Exception as err:
            self.__session.rollback()
            raise err

    def save(self):
        """
        Commits changes to the database.

        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the database.

        Parameters:
            obj: The object to delete.

        Raises:
            Exception: If deleting the object fails.

        """
        if not obj:
            return

        try:
            self.__session.delete(obj)
            self.__session.flush()
        except Exception as err:
            self.__session.rollback()
            raise err

    def reload(self):
        """
        Reloads objects from the database.

        """
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

        self.__session = scoped_session(session_factory)()

    def find(self, class_name, _id):
        """
        Finds an object in the database by its class name and ID.

        Parameters:
            class_name (str): The name of the class.
            _id (str): The ID of the object.

        Returns:
            object: The found object.

        """
        _class = self.get_class(class_name)
        if not _class:
            return None

        obj = self.__session.query(_class).filter_by(id=_id).first()
        if not obj:
            print("** no instance found **")
            return None

        self.__session.refresh(obj)
        return obj

    def remove(self, class_name, _id):
        """
        Removes an object from the database by its class name and ID.

        Parameters:
            class_name (str): The name of the class.
            _id (str): The ID of the object.

        """

        self.delete(self.find(class_name, _id))

    def find_all(self, class_name=""):
        """
        Finds all objects of a given class from the database.

        Parameters:
            class_name (str): The name of the class.

        Returns:
            list: A list of string representations of the objects.

        """
        if not class_name:
            return [str(instance) for instance in self.all().values()]

        _class = self.get_class(class_name)
        if not _class:
            return []

        return [str(instance) for instance in self.all(_class).values()]

    def update(self, class_name, _id, **kwargs):
        """
        Updates an object in the database.

        Parameters:
            class_name (str): The name of the class.
            _id (str): The ID of the object.
            kwargs: Keyword arguments representing updated attributes.

        Raises:
            Exception: If updating the object fails.

        """
        _class = self.get_class(class_name)
        if not _class:
            return

        obj = self.find(class_name, _id)
        if not obj:
            return

        try:
            self.__session.refresh(obj)
            self.__session.query(_class)\
                .filter_by(id=_id).update(kwargs)
            self.__session.flush()
        except Exception as err:
            self.__session.rollback()
            raise err

    def count(self, class_name):
        """
        Counts the number of objects of a given class in the database.

        Parameters:
            class_name (str): The name of the class.

        Returns:
            int: The count of objects.

        """
        _class = self.get_class(class_name)
        if not _class:
            return

        return self.__session.query(func.count(_class.id)).scalar()

    def close(self):
        """
        Closes the database session.

        """
        self.__session.close()
