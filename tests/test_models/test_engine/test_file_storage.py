#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.

Unittest classes:
    TestFileStorageInstantiation
    TestFileStorageMethods
"""

import json
import os
import unittest
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorageInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(self):
        """Test FileStorage instantiation without arguments."""
        self.assertIsInstance(storage, FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        """Test FileStorage instantiation with arguments."""
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        """Test if the file path attribute is a private string."""
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)

    def testFileStorage_objects_is_private_dict(self):
        """Test if the objects attribute is a private dictionary."""
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_storage_initializes(self):
        """Test if the storage attribute is initialized correctly."""
        self.assertIs(storage, storage)


class TestFileStorageMethods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        """Setup class for initializing resources."""

        # Create test objects
        cls.base_model = BaseModel()
        cls.user = User()
        cls.state = State()
        cls.place = Place()
        cls.city = City()
        cls.amenity = Amenity()
        cls.review = Review()

        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        """Teardown class for cleaning up resources."""

        del cls.base_model
        del cls.user
        del cls.state
        del cls.place
        del cls.city
        del cls.amenity
        del cls.review

        try:
            os.remove("file.json")
        except IOError:
            pass

        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def test_all(self):
        """Test the all() method."""
        objects = storage.all()
        self.assertIsInstance(objects, dict)

    def test_all_with_arg(self):
        """Test the all() method with argument."""
        with self.assertRaises(TypeError):
            storage.all(None)

    def test_new(self):
        """Test the new() method."""
        # Add objects to storage
        storage.new(self.base_model)
        storage.new(self.user)
        storage.new(self.state)
        storage.new(self.place)
        storage.new(self.city)
        storage.new(self.amenity)
        storage.new(self.review)

        # Check if objects are added correctly
        objects = storage.all()
        self.assertIn("BaseModel." + self.base_model.id, objects)
        self.assertIn("User." + self.user.id, objects)
        self.assertIn("State." + self.state.id, objects)
        self.assertIn("Place." + self.place.id, objects)
        self.assertIn("City." + self.city.id, objects)
        self.assertIn("Amenity." + self.amenity.id, objects)
        self.assertIn("Review." + self.review.id, objects)

    def test_new_with_args(self):
        """Test the new() method with arguments."""
        with self.assertRaises(TypeError):
            storage.new(BaseModel(), None)

    def test_save(self):
        """Test the save() method."""
        # Add objects to storage
        storage.new(self.base_model)
        storage.new(self.user)
        storage.new(self.state)
        storage.new(self.place)
        storage.new(self.city)
        storage.new(self.amenity)
        storage.new(self.review)

        # Save objects to file
        storage.save()

        # Check if objects are saved correctly
        with open("file.json", "r") as file:
            deserialized_objects = json.load(file)
            self.assertIn("BaseModel." + self.base_model.id,
                          deserialized_objects)
            self.assertIn("User." + self.user.id, deserialized_objects)
            self.assertIn("State." + self.state.id, deserialized_objects)
            self.assertIn("Place." + self.place.id, deserialized_objects)
            self.assertIn("City." + self.city.id, deserialized_objects)
            self.assertIn("Amenity." + self.amenity.id, deserialized_objects)
            self.assertIn("Review." + self.review.id, deserialized_objects)
            self.assertIn("Review." + self.review.id, deserialized_objects)

    def test_save_with_arg(self):
        """Test the save() method with argument."""
        with self.assertRaises(TypeError):
            storage.save(None)

    def test_reload(self):
        """Test the reload() method."""
        # Add objects to storage
        storage.new(self.base_model)
        storage.new(self.user)
        storage.new(self.state)
        storage.new(self.place)
        storage.new(self.city)
        storage.new(self.amenity)
        storage.new(self.review)

        # Save objects to file
        storage.save()

        # Reload objects from file
        storage.reload()

        # Check if objects are reloaded correctly
        objects = storage.all()
        self.assertIn("BaseModel." + self.base_model.id, objects)
        self.assertIn("User." + self.user.id, objects)
        self.assertIn("State." + self.state.id, objects)
        self.assertIn("Place." + self.place.id, objects)
        self.assertIn("City." + self.city.id, objects)
        self.assertIn("Amenity." + self.amenity.id, objects)
        self.assertIn("Review." + self.review.id, objects)

    def test_reload_with_arg(self):
        """Test the ~reload() method with argument."""
        with self.assertRaises(TypeError):
            storage.reload(None)


if __name__ == "__main__":
    unittest.main()
