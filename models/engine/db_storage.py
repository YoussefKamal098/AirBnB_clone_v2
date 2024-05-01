#!/usr/bin/python3

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base
from models.engine.storage import Storage


class DBStorage(Storage):
    __engine = None
    __session = None

    def __init__(self):
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        hbnb_env = getenv('HBNB_ENV')

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db}", pool_pre_ping=True)

        if hbnb_env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        dictionary = {}
        
        if cls is None:
            for _class in self.get_classes():
                instances = _class.query.all()
                class_name = _class.__name__
                for instance in instances:
                    key = self._get_obj_key(class_name, instance.id)
                    dictionary[key] = instance
        else:
            instances = cls.query.all()
            class_name = cls.__name__
            for instance in instances:
                key = self._get_obj_key(class_name, instance.id)
                dictionary[key] = instance

        return dictionary

    def new(self, obj):
        if not obj:
            return

        try:
            self.__session.add(obj)
            self.__session.flush()
            self.__session.refresh(obj)
        except Exception as err:
            self.__session.rollback()
            raise err

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if not obj:
            return

        try:
            self.__session.delete(obj)
            self.__session.flush()
        except Exception as err:
            self.__session.rollback()
            raise err

    def reload(self):
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

        session = scoped_session(session_factory)
        Base.query = session.query_property()
        self.__session = session()

    def find(self, class_name, _id):
        _class = self.get_class(class_name)

        if not _class:
            return None

        return _class.query.filter_by(id=_id).first()

    def remove(self, class_name, _id):
        self.delete(self.find(class_name, _id))

    def find_all(self, class_name=""):
        _class = self.get_class(class_name)

        if not _class:
            return []

        return [str(instance) for instance in self.all(_class).values()]

    def update(self, class_name, _id, **kwargs):
        pass

    def count(self, class_name):
        pass

    def close(self):
        self.__session.close()
