#!/usr/bin/python3
"""
This Module contains tests for the Console
"""

import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage


class TestConsole(unittest.TestCase):
    """Tests the Console application"""
    @classmethod
    def setUpClass(cls):
        """sets up the test console"""
        cls.models = storage.get_models_names()
        try:
            os.rename("file.json", "tmp")
        except OSError:
            pass

        cls.cmd = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """removes the file.json temporary file"""
        try:
            os.remove("file.json")
        except OSError:
            pass

        try:
            os.rename("tmp", "file.json")
        except OSError:
            pass

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertFalse(HBNBCommand().onecmd("            "))
            self.assertEqual("", output.getvalue())

    def test_help(self):
        commands = ['EOF', 'quit', 'destroy',
                    'create', 'update', 'show',
                    'count', 'all']

        for command in commands:
            with self.subTest(command=command):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.assertFalse(HBNBCommand().onecmd(f"help {command}"))
                    self.assertNotEqual(f"*** No help on {command}",
                                        output.getvalue().strip())

    def test_create_displays_class_name_error(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create')
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_create_displays_class_does_not_exist_error(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BModel')
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_create_creates_an_instance(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue()
                    self.assertNotIn(_id, [None, ""])

                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'show {model} {_id}')
                    self.assertIn(_id.strip('\n'), output.getvalue())

    def test_show_displays_class_name_error(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('show')
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_show_displays_class_does_not_exist_error(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('show BModel')
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_show_displays_an_instance(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    self.cmd.onecmd(f'show {model} {_id}')
                    self.assertIn(model, output.getvalue())

    def test_destroy_displays_class_name_error(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy')
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_destroy_displays_class_does_not_exist(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy BModel')
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_count_displays_class_does_not_exist(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('count BModel')
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_destroy_displays_instance_not_found(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy BaseModel "id that doesn\'t exists"')
            self.assertIn("** no instance found **", output.getvalue())

    def test_destroy_deletes_an_instance(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    self.cmd.onecmd(f'destroy {model} {_id}')
                    self.cmd.onecmd(f'show {model} {_id}')
                    self.assertIn("** no instance found **", output.getvalue())

    def test_all_displays_all_instance(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    self.cmd.onecmd(f'create {model}')
                    self.cmd.onecmd(f'all {model}')
                    self.assertIn(model, output.getvalue())
                    self.assertGreaterEqual(output.getvalue().count(model), 2)

    def test_instances_count(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()):
                    for _ in range(10):
                        self.cmd.onecmd(f'create {model}')

                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'count {model}')
                    self.assertLessEqual(10, int(output.getvalue()))

    def test_all_displays_specific_class_instances(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    self.cmd.onecmd('create BaseModel')
                    self.cmd.onecmd(f'all {model}')
                    self.assertIn(model, output.getvalue())

                for other_model in self.models:
                    if other_model == model:
                        continue
                    self.assertNotIn(other_model, output.getvalue())

    def test_update_attribute_name_missing_error(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    self.cmd.onecmd(f'update {model} {_id}')
                    self.assertIn(
                        "** attribute name missing **", output.getvalue())

    def test_update_attribute_value_missing_error(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    self.cmd.onecmd(f'update {model} {_id} first_name')
                    self.assertIn("** value missing **", output.getvalue())

    def test_update_updates_instance(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    self.cmd.onecmd(f'update {model} {_id} attr value')
                    self.cmd.onecmd(f'show {model} {_id}')
                    self.assertIn('attr', output.getvalue())
                    self.assertIn('value', output.getvalue())

    def test_class_name_create_creates_an_instance(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'{model}.create()')
                    _id = output.getvalue()
                    self.assertNotIn(_id, [None, ""])

                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'show {model} {_id}')
                    self.assertIn(_id.strip('\n'), output.getvalue())

    def test_class_name_all_displays_instances(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    self.cmd.onecmd(f'create {model}')
                    self.cmd.onecmd(f'{model}.all()')
                    self.assertIn(model, output.getvalue())
                    self.assertGreaterEqual(output.getvalue().count(model), 2)

    def test_class_name_instances_count(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()):
                    for _ in range(10):
                        self.cmd.onecmd(f'create {model}')

                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'{model}.count()')
                    self.assertLessEqual(10, int(output.getvalue()))

    def test_class_name_instance_show(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    self.cmd.onecmd(f'{model}.show("{_id}")')
                    self.assertIn(model, output.getvalue())

    def test_class_name_instance_destroy(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    self.cmd.onecmd(f'{model}.destroy("{_id}")')
                    self.cmd.onecmd(f'show {model} {_id}')
                    self.assertIn('** no instance found **', output.getvalue())

    def test_class_name_instance_update_with_key_value_pair(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    key, value = "name", "Julia"
                    self.cmd.onecmd(
                        f'{model}.update("{_id}", "{key}", "{value}")')
                    self.cmd.onecmd(f'show {model} {_id}')
                    self.assertIn('name', output.getvalue())
                    self.assertIn('Julia', output.getvalue())

    def test_class_name_instance_update_with_dict(self):
        for model in self.models:
            with self.subTest(model=model):
                with patch('sys.stdout', new=StringIO()) as output:
                    self.cmd.onecmd(f'create {model}')
                    _id = output.getvalue().strip('\n')
                    dict_attr = "{ 'name' : 'Julia', 'age' : 25}"
                    self.cmd.onecmd(f'{model}.update("{_id}", {dict_attr})')
                    self.cmd.onecmd(f'show {model} {_id}')
                    self.assertIn('name', output.getvalue())
                    self.assertIn('25', output.getvalue())
                    self.assertIn('Julia', output.getvalue())
                    self.assertIn('age', output.getvalue())


if __name__ == "__main__":
    unittest.main()
