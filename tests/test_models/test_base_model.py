#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModelInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        base_model1 = BaseModel()
        base_model2 = BaseModel()
        self.assertNotEqual(base_model1.id, base_model2.id)

    def test_two_models_different_created_at(self):
        base_model1 = BaseModel()
        sleep(0.05)
        base_model2 = BaseModel()

        self.assertLess(base_model1.created_at, base_model2.created_at)

    def test_two_models_different_updated_at(self):
        base_model1 = BaseModel()
        sleep(0.05)
        base_model2 = BaseModel()

        self.assertLess(base_model1.updated_at, base_model2.updated_at)

    def test_str_representation(self):
        date = datetime.today()
        date_representation = repr(date)
        base_model = BaseModel()
        base_model.id = "123456"
        base_model.created_at = base_model.updated_at = date
        base_model_string_representation = base_model.__str__()

        self.assertIn("[BaseModel] (123456)", base_model_string_representation)
        self.assertIn("'id': '123456'", base_model_string_representation)
        self.assertIn("'created_at': " + date_representation,
                      base_model_string_representation)

        self.assertIn("'updated_at': " + date_representation,
                      base_model_string_representation)

    def test_args_unused(self):
        base_model = BaseModel(None)

        self.assertNotIn(None, base_model.__dict__.values())

    def test_instantiation_with_kwargs(self):
        date = datetime.today()
        date_isoformat = date.isoformat()

        base_model = BaseModel(id="345",
                               created_at=date_isoformat,
                               updated_at=date_isoformat)
        self.assertEqual(base_model.id, "345")
        self.assertEqual(base_model.created_at, date)
        self.assertEqual(base_model.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        date = datetime.today()
        date_isoformat = date.isoformat()

        base_model = BaseModel("12", id="345",
                               created_at=date_isoformat,
                               updated_at=date_isoformat
                               )
        self.assertEqual(base_model.id, "345")
        self.assertEqual(base_model.created_at, date)
        self.assertEqual(base_model.updated_at, date)


class TestBaseModelSave(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        base_model = BaseModel()
        sleep(0.05)
        first_updated_at = base_model.updated_at
        base_model.save()

        self.assertLess(first_updated_at, base_model.updated_at)

    def test_two_saves(self):
        base_model = BaseModel()
        sleep(0.05)
        first_updated_at = base_model.updated_at
        base_model.save()
        second_updated_at = base_model.updated_at

        self.assertLess(first_updated_at, second_updated_at)

        sleep(0.05)
        base_model.save()

        self.assertLess(second_updated_at, base_model.updated_at)

    def test_save_with_arg(self):
        base_model = BaseModel()

        with self.assertRaises(TypeError):
            base_model.save(None)

    def test_save_updates_file(self):
        base_model = BaseModel()
        base_model.save()
        base_model_id = "BaseModel." + base_model.id

        with open("file.json", "r") as f:
            self.assertIn(base_model_id, f.read())


class TestBaseModelToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        base_model = BaseModel()

        self.assertTrue(dict, type(base_model.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        base_model = BaseModel()

        self.assertIn("id", base_model.to_dict())
        self.assertIn("created_at", base_model.to_dict())
        self.assertIn("updated_at", base_model.to_dict())
        self.assertIn("__class__", base_model.to_dict())

    def test_to_dict_contains_added_attributes(self):
        base_model = BaseModel()
        base_model.name = "Holberton"
        base_model.my_number = 98

        self.assertIn("name", base_model.to_dict())
        self.assertIn("my_number", base_model.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        base_model = BaseModel()
        base_model_dict = base_model.to_dict()

        self.assertEqual(str, type(base_model_dict["created_at"]))
        self.assertEqual(str, type(base_model_dict["updated_at"]))

    def test_to_dict_output(self):
        date = datetime.today()
        base_model = BaseModel()
        base_model.id = "123456"
        base_model.created_at = base_model.updated_at = date

        dictionary = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat()
        }

        self.assertDictEqual(base_model.to_dict(), dictionary)

    def test_contrast_to_dict_dunder_dict(self):
        base_model = BaseModel()

        self.assertNotEqual(base_model.to_dict(), base_model.__dict__)

    def test_to_dict_with_arg(self):
        base_model = BaseModel()

        with self.assertRaises(TypeError):
            base_model.to_dict(None)


if __name__ == "__main__":
    unittest.main()
