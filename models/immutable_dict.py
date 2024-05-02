#!/usr/bin/python3
"""
This module defines the ImmutableDict class,
which wraps a dictionary to make it immutable.
"""


class ImmutableDict(object):
    """
    ImmutableDict class wraps a dictionary to make it immutable.
    """

    def __init__(self, d):
        """
        Initializes the ImmutableDict object with a dictionary.

        Parameters:
            - d (dict): The dictionary to be wrapped.
        """
        self._d = d

    def __getitem__(self, key):
        """
        Gets the value associated with the given key.

        Parameters:
            - key: The key whose value is to be retrieved.

        Returns:
            The value associated with the given key.
        """
        return self._d[key]

    def keys(self):
        """
        Returns a view object of the keys in the dictionary.
        """
        return self._d.keys()

    def values(self):
        """
        Returns a view object of the values in the dictionary.
        """
        return self._d.values()

    def items(self):
        """
        Returns a view object of the key-value pairs in the dictionary.
        """
        return self._d.items()

    def get(self, key, default=None):
        """
        Gets the value associated with the given key, with an
        optional default value.

        Parameters:
            - key: The key whose value is to be retrieved.
            - default: The default value to return if the key is not found.

        Returns:
            The value associated with the given key, or the default
            value if the key is not found.
        """
        return self._d.get(key, default)

    def __iter__(self):
        """
        Iterates over the keys in the dictionary.
        """
        return iter(self._d)

    def __len__(self):
        """
        Returns the number of items in the dictionary.
        """
        return len(self._d)

    def __repr__(self):
        """
        Returns a string representation of the ImmutableDict object.
        """
        return 'MappingProxyType({!r})'.format(self._d)
