#!/usr/bin/python3
"""
This module defines a set of commands used in an AirBnB application.
"""
from copy import deepcopy
from abc import ABC, abstractmethod
from utils import parse_value, parse_params


class Tokens:
    """
    Tokens class manages token values and provides methods
    to set, reset, and access them.

    Attributes:
        _default_values (dict): Default values for token attributes.

    Methods:
        __init__(**kwargs): Initializes Tokens object with optional
        initial token values.
        reset_tokens(): Resets all attributes to their default values.
        set_tokens(values): Sets token values from a dictionary of
        key-value pairs.
        __setattr__(key, value): Sets the value of a token attribute.
        __delattr__(key): Raises an AttributeError when attempting
        to delete a token.
    """

    def __init__(self, **kwargs):
        """
        Initialize Tokens object with optional initial token values.

        Args:
            **kwargs: Arbitrary keyword arguments representing token
            attributes.
        """
        kwargs.update({"_default_values": deepcopy(kwargs)})
        self.__dict__.update(kwargs)

    def reset_tokens(self):
        """
        Reset all attributes to their default values.
        """
        self.__dict__.update(
            deepcopy(self.__dict__.get("_default_values", {})))

    def set_tokens(self, values):
        """
        Set token values from a dictionary of key-value pairs.

        Args:
            values (dict): A dictionary of key-value pairs
            representing token attributes.
        """
        for key, value in values.items():
            setattr(self, key, value)

    def __setattr__(self, key, value):
        """
        Set the value of a token attribute.

        Raises:
            AttributeError: If attempting to add a new token.
            TypeError: If the assigned value's type does
            not match the token's type.

        Args:
            key (str): Name of the token attribute.
            value (any): Value to assign to the token attribute.
        """
        if key not in self.__dict__:
            raise AttributeError("Cannot add new token")
        elif type(self.__dict__[key]) != type(value):
            raise TypeError(
                f"Cannot assign value of type {type(value).__name__} "
                f"to token of type {type(self.__dict__[key]).__name__}"
            )
        self.__dict__[key] = value

    def __delattr__(self, key):
        """
        Raise an AttributeError when attempting to delete a token.

        Args:
            key (str): Name of the token attribute.
        """
        raise AttributeError("Cannot delete token")


class AirBnBCommand(ABC):
    """
    AirBnBCommand is an abstract base class for defining
    command objects in an AirBnB application.
    """

    def __init__(self, storage):
        """
        Initializes a new instance of the AirBnBCommand class.

        Parameters:
            storage (FileStorage): A storage object used to interact with
            the FileStorage.

        """
        self._storage = storage

    @abstractmethod
    def execute(self):
        """
        Abstract method to execute the specific command logic.

        Subclasses must implement this method to define the behavior
        of their respective commands (e.g., create, show, update, etc.).
        """
        pass

    @abstractmethod
    def reset_tokens(self):
        """
        Abstract method to reset any internal tokens used by the command.

        Subclasses might use tokens to store parsed information from the
        command line input. This method ensures proper cleanup after execution.
        """
        pass

    @abstractmethod
    def set_tokens(self, tokens):
        """
        Abstract method to set internal tokens based on parsed command
        line arguments.

        Subclasses might use this method to store information extracted
        from the command line for later usage during execution.

        Parameters:
            tokens (list[str]): A list of tokens parsed from the command
            line input.
        """
        pass

    @staticmethod
    def get_class_name(tokens):
        """
        Retrieves the class name token.

        Parameters:
            tokens (Tokens): command tokens
            from the command line input.
        Returns:
            Union: The class name token.
        """
        class_name = tokens.class_name

        if not class_name:
            print("** class name missing **")
            return None

        return class_name

    @staticmethod
    def get_instance_id(tokens):
        """
        Retrieves the instance ID token.

        Parameters:
            tokens (Tokens): command tokens
            from the command line input.
        Returns:
            str: The instance ID token.
        """
        _id = tokens.instance_id

        if not _id:
            print("** instance id missing **")
            return None

        return _id

    @staticmethod
    def get_attribute_name_value_pair(tokens):
        """
        Retrieves attribute name-value pair tokens.

        Parameters:
            tokens (Tokens): command tokens
            from the command line input.
        Returns:
            dict: A dictionary containing attribute name-value pair.
        """
        attribute_name = tokens.attribute_name
        attribute_value = tokens.attribute_value

        if not attribute_name:
            print("** attribute name missing **")
            return None
        if not attribute_value:
            print("** value missing **")
            return None

        attribute_value = parse_value(attribute_value)

        if not attribute_value:
            return None

        return {"attribute_name": attribute_name,
                "attribute_value":  attribute_value}

    def get_class(self, tokens):
        """
        Retrieves the class based on the class name.

         Parameters:
            tokens (Tokens): command tokens
            from the command line input.
        Returns:
            class: The model class.
        """
        class_name = self.get_class_name(tokens)
        if not class_name:
            return None

        _class = self._storage.get_class(class_name)
        if not _class:
            return None

        return _class

    def get_class_instance(self, tokens):
        """
        Retrieves the class instance based on the class and instance ID.

         Parameters:
            tokens (Tokens): command tokens
            from the command line input.
        Returns:
            tuple: A tuple containing the class and class instance.
        """
        _class = self.get_class(tokens)
        if not _class:
            return None

        _id = self.get_instance_id(tokens)
        if not _id:
            return None

        instance = self._storage.find(_class.__name__, _id)
        if not instance:
            return None

        return _class, instance


class CreateCommand(AirBnBCommand):
    """
    CreateCommand is a concrete subclass of AirBnBCommand for
    creating new objects.
    """

    def __init__(self, storage):
        super().__init__(storage)
        self.__tokens = Tokens(class_name="", params=())

    def set_tokens(self, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list[str]): A list of token values.

        """
        self.__tokens.set_tokens(dict(zip(
            ("class_name", "params"), (tokens[0], tuple(tokens[1:])))))

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        self.__tokens.reset_tokens()

    def execute(self):
        """
        Executes the create command.
        """
        _class = self.get_class(self.__tokens)
        if not _class:
            return

        kwargs = parse_params(self.__tokens.params)
        for attr in ["id", "created_at", "updated_at"]:
            kwargs.pop(attr, None)

        instance = _class(**kwargs)
        print(instance.id)

        instance.save()


class ShowCommand(AirBnBCommand):
    """
    ShowCommand is a concrete subclass of AirBnBCommand for
    displaying object details.
    """

    def __init__(self, storage):
        super().__init__(storage)
        self.__tokens = Tokens(class_name="", instance_id="")

    def set_tokens(self, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list[str]): A list of token values.

        """
        self.__tokens.set_tokens(
            dict(zip(("class_name", "instance_id"), tokens)))

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        self.__tokens.reset_tokens()

    def execute(self):
        """
        Executes the show command.
        """
        class_instance = self.get_class_instance(self.__tokens)
        if not class_instance:
            return

        _, instance = class_instance
        print(instance)


class DestroyCommand(AirBnBCommand):
    """
    DestroyCommand is a concrete subclass of AirBnBCommand for
    deleting objects.
    """

    def __init__(self, storage):
        super().__init__(storage)
        self.__tokens = Tokens(class_name="", instance_id="")

    def set_tokens(self, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list[str]): A list of token values.

        """
        self.__tokens.set_tokens(
            dict(zip(("class_name", "instance_id"), tokens)))

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        self.__tokens.reset_tokens()

    def execute(self):
        """
        Executes the destroy command.
        """
        class_instance = self.get_class_instance(self.__tokens)
        if not class_instance:
            return

        _class, instance = class_instance
        self._storage.remove(_class.__name__, instance.id)
        self._storage.save()


class AllCommand(AirBnBCommand):
    """
    AllCommand is a concrete subclass of AirBnBCommand for
    displaying all objects or objects of a specific type.
    """

    def __init__(self, storage):
        super().__init__(storage)
        self.__tokens = Tokens(class_name="")

    def set_tokens(self, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list[str]): A list of token values.

        """
        self.__tokens.set_tokens(dict(zip(("class_name", ), tokens)))

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        self.__tokens.reset_tokens()

    def execute(self):
        """
        Executes the all command.
        """
        class_name = self.__tokens.class_name
        if not class_name:
            print(self._storage.find_all())
            return

        _class = self.get_class(self.__tokens)
        if not _class:
            return

        print(self._storage.find_all(class_name=_class.__name__))


class AbstractUpdateCommand(AirBnBCommand, ABC):
    """Abstract base class for update commands in the AirBnB application.

    This abstract class defines the interface for update commands,
    enforcing a common structure and behavior for updating
    entities within the AirBnB system.

    Subclasses must implement the `check_tokens`
    method to validate the user input provided for update operations.
    """
    @abstractmethod
    def check_tokens(self, tokens):
        """Checks user input for an update command.

        This abstract method enforces validation of tokens
        (user input) required for specific update operations within
        the AirBnB system. Each subclass implementing `AbstractUpdateCommand`
        must define the logic for checking the validity and completeness of
        tokens relevant to the specific update operation it represents.

        Parameter:
            tokens (dict): A dictionary containing user input for the update.
            The specific keys and their expected values will vary depending on
            the update operation.

        Returns:
            bool: True if the tokens are valid and complete, False otherwise.
        """
        pass


class UpdateCommand(AbstractUpdateCommand):
    """
    UpdateCommand is a concrete subclass of AirBnBCommand for
    updating attributes of an object.
    """

    def __init__(self, storage):
        super().__init__(storage)

        self.__update_commands = {
            "update_with_key_value_pair":
                UpdateWithNameValuePairCommand(storage),
            "update_with_dict":
                UpdateWithDictCommand(storage)
        }

        default = self.__update_commands["update_with_key_value_pair"]
        self.__default_update_command = default
        self.__current_update_command = None

    def check_tokens(self, tokens):
        """
        Checks if the provided command line arguments meet the expected format.
        (Override Method)

        This method validates the number of tokens and the type
        of the third token (assuming a specific format for certain commands).
        It returns True if the tokens adhere to the expected format,
        False otherwise.

         Parameters:
            tokens (dict[str, any]): A list of tokens parsed from the
            command line input.

        Returns:
            bool: True if the tokens meet the expected format, False otherwise.
        """
        return False

    def set_tokens(self, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list): A list of token values.
        """

        for update_command in self.__update_commands.values():
            if update_command.check_tokens(tokens):
                self.__current_update_command = update_command
                break

        if self.__current_update_command:
            self.__current_update_command.set_tokens(tokens)
        else:
            self.__default_update_command.set_tokens(tokens)

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        if not self.__current_update_command:
            self.__default_update_command.reset_tokens()
            return

        self.__current_update_command.reset_tokens()
        self.__current_update_command = None

    def execute(self):
        """
        Executes the update command.
        """
        if not self.__current_update_command:
            self.__default_update_command.execute()
            return

        self.__current_update_command.execute()


class UpdateWithNameValuePairCommand(AbstractUpdateCommand):
    """
    UpdateCommand is a concrete subclass of AirBnBCommand for
    updating attributes of an object with one key value pair.
    """

    def __init__(self, storage):
        super().__init__(storage)

        self.__tokens = Tokens(
            class_name="",
            instance_id="",
            attribute_name="",
            attribute_value="",
        )

    def check_tokens(self, tokens):
        """
        Checks if the provided command line arguments meet the expected format.

        This method validates the number of tokens and the type
        of the third token (assuming a specific format for certain commands).
        It returns True if the tokens adhere to the expected format,
        False otherwise.

        Parameters:
            tokens (list[any]): A list of tokens parsed from the
            command line input.

        Returns:
            bool: True if the tokens meet the expected format, False otherwise.
        """
        return len(tokens) >= 4 and type(tokens[2]) is str

    def set_tokens(self, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list[str]): A list of token values.

        """
        self.__tokens.set_tokens(dict(zip(("class_name",
                                           "instance_id",
                                           "attribute_name",
                                           "attribute_value"
                                           ), tokens)))

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        self.__tokens.reset_tokens()

    def execute(self):
        """
        Executes the update command.
        """
        class_instance = self.get_class_instance(self.__tokens)
        if not class_instance:
            return

        attribute_name_value_pair = self.get_attribute_name_value_pair(
                                                        self.__tokens)

        if not attribute_name_value_pair:
            return

        name = attribute_name_value_pair["attribute_name"]
        value = attribute_name_value_pair["attribute_value"]

        if name in ["id", "created_at", "updated_at"]:
            return

        _class, instance = class_instance
        self._storage.update(_class.__name__, instance.id, **{name: value})
        self._storage.save()


class UpdateWithDictCommand(AbstractUpdateCommand):
    """
    UpdateCommand is a concrete subclass of AirBnBCommand for
    updating attributes of an object with dictionary.
    """

    def __init__(self, storage):
        super().__init__(storage)

        self.__tokens = Tokens(
            class_name="",
            instance_id="",
            dictionary={}
        )

    def check_tokens(self, tokens):
        """
        Checks if the provided command line arguments meet the expected format.

        This method validates the number of tokens and the type
        of the third token (assuming a specific format for certain commands).
        It returns True if the tokens adhere to the expected format,
        False otherwise.

         Parameters:
            tokens (list[any]): A list of tokens parsed from the
            command line input.

        Returns:
            bool: True if the tokens meet the expected format, False otherwise.
        """
        return len(tokens) >= 3 and type(tokens[2]) is dict

    def set_tokens(self, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list[str]): A list of token values.

        """
        self.__tokens.set_tokens(dict(zip(("class_name",
                                           "instance_id",
                                           "dictionary",
                                           ), tokens)))

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        self.__tokens.reset_tokens()

    def execute(self):
        """
        Executes the update command.
        """
        class_instance = self.get_class_instance(self.__tokens)
        if not class_instance:
            return

        dictionary = self.__tokens.dictionary
        if not dictionary:
            return

        for attr in ["id", "created_at", "updated_at"]:
            dictionary.pop(attr, None)

        _class, instance = class_instance
        self._storage.update(
            _class.__name__, instance.id, **dictionary)
        self._storage.save()


class CountCommand(AirBnBCommand):
    """
    CountCommand is a concrete subclass of AirBnBCommand for
    counting the number of class Object in storage.
    """

    def __init__(self, storage):
        super().__init__(storage)
        self.__tokens = Tokens(class_name="")

    def set_tokens(self, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list[str]): A list of token values.

        """
        self.__tokens.set_tokens(dict(zip(("class_name", ), tokens)))

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        self.__tokens.reset_tokens()

    def execute(self):
        """
        Executes the update command.
        """
        _class = self.get_class(self.__tokens)
        if not _class:
            return

        print(self._storage.count(class_name=_class.__name__))
