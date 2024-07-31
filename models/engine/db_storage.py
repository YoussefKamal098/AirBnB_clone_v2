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
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base
from models.engine.storage import Storage


class DBStorage(Storage):
    """
    DBStorage class represents the database storage system using SQLAlchemy.
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

        missing_vars = [var_name for var_name, var_value in [
            ('HBNB_MYSQL_USER', user),
            ('HBNB_MYSQL_PWD', pwd),
            ('HBNB_MYSQL_HOST', host),
            ('HBNB_MYSQL_DB', db)
        ] if not var_value]

        if missing_vars:
            raise ValueError(f"Missing the following environment "
                             f"variables for database connection: "
                             f"{', '.join(missing_vars)}")

        self._connect(user, pwd, host, db)

        if hbnb_env == 'test':
            Base.metadata.drop_all(self.__engine)

    @classmethod
    def _connect(cls, user, pwd, host, db, pool_pre_ping=True):
        """
        Creates a database engine connection using SQLAlchemy.
        """
        cls.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db}",
            pool_pre_ping=pool_pre_ping
        )

    def all(self, cls=None):
        """
        Retrieve all objects of a given class from the database.

        Parameters:
            cls (class): The class of objects to retrieve.

        Returns:
            dict: A dictionary of objects, where keys are object IDs.
        """
        dictionary = {}
        try:
            if cls is None:
                for _class in self.get_classes():
                    instances = self.__session.query(_class).all()
                    dictionary.update(
                        self._class_to_dict(_class.__name__, instances))
            else:
                instances = self.__session.query(cls).all()
                dictionary.update(
                    self._class_to_dict(cls.__name__, instances))
        except SQLAlchemyError as err:
            self.__session.rollback()
            raise err

        return dictionary

    def new(self, obj):
        """
        Adds a new object to the database session.

        Parameters:
            obj: The object to add.
        """
        if not obj:
            return

        try:
            self.__session.add(obj)
            self.__session.flush()
        except SQLAlchemyError as err:
            self.__session.rollback()
            raise err

    def save(self):
        """
        Commits changes to the database.
        """
        try:
            self.__session.commit()
        except SQLAlchemyError as err:
            self.__session.rollback()
            raise err

    def delete(self, obj=None):
        """
        Deletes an object from the database.

        Parameters:
            obj: The object to delete.
        """
        if not obj:
            return

        try:
            self.__session.delete(obj)
            self.__session.flush()
        except SQLAlchemyError as err:
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

        DBStorage.__session = scoped_session(session_factory)

    def find(self, class_name, _id):
        """
        Finds an object in the database by its class name and ID.

        Parameters:
            class_name (str): The name of the class.
            _id (str): The ID of the object.

        Returns:
            object: The found object, or None if not found.
        """
        _class = self.get_class(class_name)
        if not _class:
            return None

        try:
            obj = self.__session.query(_class).filter_by(id=_id).first()
            if obj:
                self.__session.refresh(obj)
            return obj
        except SQLAlchemyError as err:
            self.__session.rollback()
            raise err

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

    def update(self, obj=None, **kwargs):
        """
        Updates attributes of a given object with new values
        provided in kwargs.

        This method updates the specified attributes of an
        object in the database using the provided keyword arguments.
        The method queries the object's class in the session and applies
        the updates to the object with the matching ID. Changes are flushed
        to the session but not committed.

        Parameters:
            obj (BaseModel): The object to be updated. If None,
                        the method returns without making any changes.
            **kwargs: Arbitrary keyword arguments representing the
                    attribute names and their new values to update
                    on the object.

        Raises:
            SQLAlchemyError: If an error occurs during the update process, it
                             rolls back the session and raises the exception.

        Note:
            The method flushes changes to the session but does not commit them.
            After calling this method, you should call the save method
            to commit the changes to the database.
        """
        if not obj:
            return

        try:
            self.__session.refresh(obj)
            self.__session.query(obj.__class__) \
                .filter_by(id=obj.id).update(kwargs)
            self.__session.flush()
        except SQLAlchemyError as err:
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
            return 0

        try:
            return self.__session.query(func.count(_class.id)).scalar()
        except SQLAlchemyError as err:
            self.__session.rollback()
            raise err

    def close(self):
        """
        Remove the current SQLAlchemy session.

        This method is intended to close the current SQLAlchemy session,
        ensuring that any resources held by the session are released.
        """
        self.__session.remove()

    def _class_to_dict(self, class_name, instances):
        """
        Helper method to convert a list of instances to a dictionary.

        Parameters:
            class_name (str): The name of the class.
            instances (list): The list of instances.

        Returns:
            dict: A dictionary of object instances.
        """
        return {
            self._get_obj_key(class_name, instance.id): instance
            for instance in instances
        }
