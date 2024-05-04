#!/usr/bin/python3
"""test for DB storage"""
import os
import unittest


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != 'db', 'DB Storage test')
class TestDBStorage(unittest.TestCase):
    """Tests the DB Storage"""
    pass


if __name__ == "__main__":
    unittest.main()
