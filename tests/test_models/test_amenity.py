#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenityInstantiation(unittest.TestCase):
    """Test cases for testing instantiation of the Amenity class."""

    def setUp(self):
        self.amenity_instance = Amenity()

    def test_instantiation_without_arguments(self):
        """Test that an Amenity instance is
        created successfully without arguments."""
        self.assertIsInstance(self.amenity_instance, Amenity)

    def test_instance_stored_in_objects(self):
        """Test that the newly created instance is stored
        in the class variable 'objects'."""
        self.assertIn(self.amenity_instance, models.storage.all().values())

    def test_id_is_str(self):
        """Test that the 'id' attribute of the Amenity instance is a string."""
        self.assertIsInstance(self.amenity_instance.id, str)

    def test_created_at_is_datetime(self):
        """Test that the 'created_at' attribute of the
        Amenity instance is a datetime object."""
        self.assertIsInstance(self.amenity_instance.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """Test that the 'updated_at' attribute of the
        Amenity instance is a datetime object."""
        self.assertIsInstance(self.amenity_instance.updated_at, datetime)

    def test_name_attribute_is_class_attribute(self):
        """Test that 'name' attribute is a class attribute
        and not an instance attribute."""
        self.assertIsInstance(Amenity.name, str)
        self.assertIn("name", dir(Amenity))
        self.assertNotIn("name", self.amenity_instance.__dict__)

    def test_unique_ids_for_two_instances(self):
        """Test that two instances of Amenity have unique IDs."""
        amenity_instance_2 = Amenity()
        self.assertNotEqual(self.amenity_instance.id, amenity_instance_2.id)

    def test_different_created_at_for_two_instances(self):
        """Test that two instances of Amenity have
        different 'created_at' timestamps."""
        sleep(0.05)
        amenity_instance_2 = Amenity()
        self.assertLess(self.amenity_instance.created_at,
                        amenity_instance_2.created_at)

    def test_different_updated_at_for_two_instances(self):
        """Test that two instances of Amenity have
        different 'updated_at' timestamps."""
        sleep(0.05)
        amenity_instance_2 = Amenity()
        self.assertLess(self.amenity_instance.updated_at,
                        amenity_instance_2.updated_at)

    def test_string_representation(self):
        """Test the string representation of the Amenity instance."""
        date = datetime.today()
        self.amenity_instance.id = "123456"
        self.amenity_instance.created_at = date
        self.amenity_instance.updated_at = date
        amenity_string = str(self.amenity_instance)
        self.assertIn("[Amenity] (123456)", amenity_string)
        self.assertIn("'id': '123456'", amenity_string)
        self.assertIn("'created_at': " + repr(date), amenity_string)
        self.assertIn("'updated_at': " + repr(date), amenity_string)

    def test_unused_arguments(self):
        """Test that passing arguments to the Amenity constructor
        that are not used doesn't raise an error."""
        am = Amenity(None)
        self.assertNotIn(None, am.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation of Amenity with keyword arguments."""
        date = datetime.today()
        date_isoformat = date.isoformat()
        amenity = Amenity(id="345", created_at=date_isoformat,
                          updated_at=date_isoformat)
        self.assertEqual(amenity.id, "345")
        self.assertEqual(amenity.created_at, date)
        self.assertEqual(amenity.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Test that instantiation of Amenity with None
        keyword arguments raises TypeError."""
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

    def tearDown(self):
        del self.amenity_instance


class TestAmenitySave(unittest.TestCase):
    """Test cases for testing the save method of the Amenity class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def setUp(self):
        self.amenity_instance = Amenity()

    def test_one_save(self):
        """Test saving a single Amenity instance."""
        first_updated_at = self.amenity_instance.updated_at
        self.amenity_instance.save()
        self.assertLess(first_updated_at, self.amenity_instance.updated_at)

    def test_two_saves(self):
        """Test saving two Amenity instances."""
        first_updated_at = self.amenity_instance.updated_at
        self.amenity_instance.save()
        second_updated_at = self.amenity_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        self.amenity_instance.save()
        self.assertLess(second_updated_at, self.amenity_instance.updated_at)

    def test_save_with_argument(self):
        """Test that passing an argument to the save
        method raises TypeError."""
        with self.assertRaises(TypeError):
            self.amenity_instance.save(None)

    def test_save_updates_file(self):
        """Test that saving an Amenity instance updates the JSON file."""
        self.amenity_instance.save()
        amid = "Amenity." + self.amenity_instance.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())

    def tearDown(self):
        del self.amenity_instance


class TestAmenityToDict(unittest.TestCase):
    """Test cases for testing the to_dict method of the Amenity class."""

    def setUp(self):
        self.amenity_instance = Amenity()

    def test_to_dict_type(self):
        """Test that the return value of to_dict is a dictionary."""
        self.assertIsInstance(self.amenity_instance.to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        """Test that the keys in the returned dictionary are correct."""
        expected_keys = ["id", "created_at", "updated_at", "__class__"]
        self.assertEqual(list(self.amenity_instance.to_dict().keys()),
                         expected_keys)

    def test_to_dict_contains_added_attributes(self):
        """Test that added attributes are included in
        the dictionary returned by to_dict."""
        self.amenity_instance.middle_name = "Holberton"
        self.amenity_instance.my_number = 98
        self.assertEqual("Holberton", self.amenity_instance.middle_name)
        self.assertIn("my_number", self.amenity_instance.to_dict())

    def test_to_dict_datetime_attributes_are_strings(self):
        """Test that datetime attributes in the returned
        dictionary are strings."""
        amenity_dict = self.amenity_instance.to_dict()
        self.assertIsInstance(amenity_dict["id"], str)
        self.assertIsInstance(amenity_dict["created_at"], str)
        self.assertIsInstance(amenity_dict["updated_at"], str)

    def test_to_dict_output(self):
        """Test the output of to_dict method."""
        date = datetime.today()
        self.amenity_instance.id = "123456"
        self.amenity_instance.created_at = date
        self.amenity_instance.updated_at = date
        dictionary = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat(),
        }
        self.assertEqual(self.amenity_instance.to_dict(), dictionary)

    def test_contrast_to_dict_dunder_dict(self):
        """Test that the dictionary returned by to_dict method
        is different from the instance __dict__."""
        self.assertNotEqual(self.amenity_instance.to_dict(),
                            self.amenity_instance.__dict__)

    def test_to_dict_with_arg(self):
        """Test that passing an argument to the
        to_dict method raises TypeError."""
        with self.assertRaises(TypeError):
            self.amenity_instance.to_dict(None)

    def tearDown(self):
        del self.amenity_instance


if __name__ == "__main__":
    unittest.main()
