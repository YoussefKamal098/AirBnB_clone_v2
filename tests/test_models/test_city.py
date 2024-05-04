#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
    TestCityInstantiation
    TestCitySave
    TestCityToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCityInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_instantiation_without_arguments(self):
        """Test that City can be instantiated without any arguments."""
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        """Test that a newly created City instance
        is stored in the storage."""
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_string(self):
        """Test that the id attribute of a
        City instance is a string."""
        self.assertEqual(str, type(City().id))

    def test_created_at_is_datetime(self):
        """Test that the created_at attribute of
        a City instance is a datetime object."""
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_datetime(self):
        """Test that the updated_at attribute of
        a City instance is a datetime object."""
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_string_attribute(self):
        """Test that state_id attribute of a City instance is a string."""
        city = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city))
        self.assertNotIn("state_id", city.__dict__)

    def test_name_is_string_attribute(self):
        """Test that name attribute of a City instance is a string."""
        city = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city))
        self.assertNotIn("name", city.__dict__)

    def test_unique_ids(self):
        """Test that two different City instances have unique ids."""
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def test_different_created_at(self):
        """Test that created_at attribute of two
        different City instances is different."""
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)

    def test_different_updated_at(self):
        """Test that updated_at attribute of two
        different City instances is different."""
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.updated_at, city2.updated_at)

    def test_string_representation(self):
        """Test the string representation of a City instance."""
        date = datetime.today()
        date_representation = repr(date)
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = date
        city_string = city.__str__()
        self.assertIn("[City] (123456)", city_string)
        self.assertIn("'id': '123456'", city_string)
        self.assertIn("'created_at': " + date_representation, city_string)
        self.assertIn("'updated_at': " + date_representation, city_string)

    def test_unused_args(self):
        """Test that City instantiation with None
        argument does not add None to instance's __dict__."""
        city = City(None)
        self.assertNotIn(None, city.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation of City with keyword arguments."""
        date = datetime.today()
        date_isoformat = date.isoformat()
        city = City(id="345", created_at=date_isoformat,
                    updated_at=date_isoformat)
        self.assertEqual(city.id, "345")
        self.assertEqual(city.created_at, date)
        self.assertEqual(city.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Test that City instantiation with None
        keyword arguments raises TypeError."""
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCitySave(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def setUp(cls):
        """Set up before running tests."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(cls):
        """Clean up after running tests."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save_once(self):
        """Test that save method updates the
        updated_at attribute of a City instance."""
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        self.assertLess(first_updated_at, city.updated_at)

    def test_save_twice(self):
        """Test that save method updates the updated_at
        attribute of a City instance when called twice."""
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        second_updated_at = city.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city.save()
        self.assertLess(second_updated_at, city.updated_at)

    def test_save_with_arg(self):
        """Test that save method with argument raises TypeError."""
        city = City()
        with self.assertRaises(TypeError):
            city.save(None)

    def test_save_updates_file(self):
        """Test that save method updates the file storage."""
        city = City()
        city.save()
        city_id = "City." + city.id
        with open("file.json", "r") as file:
            self.assertIn(city_id, file.read())


class TestCityToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def setUp(self):
        """Set up before running each test."""
        self.city_instance = City()

    def test_to_dict_type(self):
        """Test that the return type of to_dict method is a dictionary."""
        self.assertTrue(dict, type(self.city_instance.to_dict()))

    def test_to_dict_contains_keys(self):
        """Test that the dictionary returned
        by to_dict method contains correct keys."""
        city_dict = self.city_instance.to_dict()
        self.assertIn("id", city_dict)
        self.assertIn("created_at", city_dict)
        self.assertIn("updated_at", city_dict)
        self.assertIn("__class__", city_dict)

    def test_to_dict_contains_added_attributes(self):
        """Test that the dictionary returned by to_dict
        method contains added attributes."""
        self.city_instance.middle_name = "Holberton"
        self.city_instance.my_number = 98
        self.assertEqual("Holberton", self.city_instance.middle_name)
        self.assertIn("my_number", self.city_instance.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that datetime attributes in the
        dictionary returned by to_dict method are strings."""
        city_dict = self.city_instance.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of to_dict method."""
        dt = datetime.today()
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = dt
        expected_dict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(city.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test that the dictionary returned by to_dict
        method is different from the instance's __dict__."""
        city = City()
        self.assertNotEqual(city.to_dict(), city.__dict__)

    def test_to_dict_with_arg(self):
        """Test that to_dict method with argument raises TypeError."""
        city = City()
        with self.assertRaises(TypeError):
            city.to_dict(None)


if __name__ == "__main__":
    unittest.main()
