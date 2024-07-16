#!/usr/bin/
"""test for File storage"""
import os
import unittest


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') == 'db', 'File Storage test')
class TestFileStorage(unittest.TestCase):
    """Tests the File Storage"""
    pass


if __name__ == '__main__':
    unittest.main()
