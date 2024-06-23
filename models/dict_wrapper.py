#!/usr/bin/python3

"""
This module defines two custom dictionary classes: FrozenDict and SealedDict.

- **FrozenDict:** Represents a read-only dictionary that prevents
  modification of existing key-value pairs after initialization.
  It's effectively immutable.

- **SealedDict:** Inherits from FrozenDict and adds further restrictions.
  It enforces the same data type for existing keys when attempting
  to update their values and prevents adding new keys.

These classes provide a level of immutability and data integrity
for dictionaries in scenarios where you want to ensure no changes
are made to the dictionary contents after creation, or when you want to
enforce strict data typing for existing keys.
"""

from copy import deepcopy


class FrozenDict:
    """
    Represents a read-only dictionary that prevents modification
    of existing key-value pairs and restricts adding or
    deleting attributes after initialization.
    """

    _frozen = False

    def __init__(self, d):
        """
        Initialize a FrozenDict instance.

        Parameters:
            d (dict): The dictionary to initialize the FrozenDict with.

        Raises:
            ValueError: If the input object is not a dictionary.
        """
        if type(d) is not dict:
            raise ValueError("The object must be a dict")

        self._d = {}

        for key, value in d.items():
            try:
                self._d[key] = deepcopy(value)
            except TypeError:
                self._d[key] = value

        self._frozen = True

    def __getitem__(self, key):
        """
        Retrieve the value associated with the given key.

        Parameters:
            key: The key to retrieve the value for.

        Returns:
            Any: The value associated with the given key.

        Raises:
            KeyError: If the key is not found in the dictionary.
        """
        return self._d[key]

    def __setitem__(self, key, value):
        """
        Prevent setting new key-value pairs.

        Parameters:
            key: The key to set.
            value: The value to associate with the key.

        Raises:
            AttributeError: Always raised to indicate
            that setting is not allowed.
        """
        raise AttributeError(f"Can't set The '{key}' key, dict is immutable")

    def keys(self):
        """
        Get a view object that displays a list of all the keys in
        the dictionary.

        Returns:
            dict_keys: A view object that displays a list of all the keys.
        """
        return self._d.keys()

    def values(self):
        """
        Get a view object that displays a list
        of all the values in the dictionary.

        Returns:
            dict_values: A view object that displays a list
            of all the values.
        """
        return self._d.values()

    def items(self):
        """
        Get a view object that displays a list of key-value
        tuple pairs in the dictionary.

        Returns:
            dict_items: A view object that displays
            a list of key-value tuple pairs.
        """
        return self._d.items()

    def get(self, key, default=None):
        """
        Retrieve the value associated with the given key,
        with optional default value.

        Parameters:
            key: The key to retrieve the value for.
            default: The default value to return if the
            key is not found (default: None).

        Returns:
            Any: The value associated with the given key,
            or the default value if key not found.
        """
        return self._d.get(key, default)

    def __iter__(self):
        """
        Return an iterator over the keys of the dictionary.

        Returns:
            iterator: An iterator over the keys of the dictionary.
        """
        return iter(self._d)

    def __len__(self):
        """
        Return the number of items in the dictionary.

        Returns:
            int: The number of items in the dictionary.
        """
        return len(self._d)

    def __repr__(self):
        """
        Return a string representation of the FrozenDict.

        Returns:
            str: String representation of the FrozenDict.
        """
        return f'{self.__class__.__name__}({self._d})'

    def __setattr__(self, key, value):
        """
        Prevent adding new attributes to the dictionary.

        Parameters:
            key: The attribute name.
            value: The attribute value.

        Raises:
            AttributeError: If attempting to add an attribute
            while the dictionary is frozen.
        """
        if self._frozen:
            raise AttributeError("Can't add an attribute to the dict")
        else:
            object.__setattr__(self, key, value)

    def __delattr__(self, item):
        """
        Prevent deleting attributes from the dictionary.

        Parameters:
            item: The attribute name to delete.

        Raises:
            AttributeError: Always raised to indicate
            that deletion is not allowed.
        """
        raise AttributeError("Can't delete an attribute from the dict")


class SealedDict(FrozenDict):
    """
    Represents a sealed dictionary that enforces the same data type
    for existing keys when attempting to update their values and
    prevents adding new keys.
    """

    def __setitem__(self, key, value):
        """
        Prevent adding new keys and enforce data
        type consistency for existing keys.

        Parameters:
            key: The key to set.
            value: The value to associate with the key.

        Raises:
            AttributeError: If the key is not found or
                if the value has an incompatible type.
        """
        if key not in self.keys():
            raise AttributeError(f"The dict doesn't contain '{key}' key")
        elif type(self[key]) is not type(value):
            raise AttributeError(f"The '{key}' key must be "
                                 f"'{self[key].__class__.__name__}' type")

        self._d[key] = value
