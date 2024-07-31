#!/usr/bin/python3
"""
This module defines a set of commands used in an AirBnB application.
"""
from abc import ABC, abstractmethod

from models.dict_wrapper import FrozenDict, SealedDict
from utils import parse_value, parse_params


class AirBnBCommand(ABC):
    """
    Abstract base class representing an Airbnb command.

    Methods:
        __init__(storage): Initializes the command with a storage system.
        execute(): Abstract method to execute the command.
        reset_tokens(): Abstract method to reset command tokens.
        set_tokens(tokens): Abstract method to set command tokens.
        get_class_name(tokens): Static method to extract class name
            from command tokens.
        get_instance_id(tokens): Static method to extract instance
            ID from command tokens.
        get_attribute_name_value_pair(tokens): Static method to extract
            attribute name-value pair from command tokens.
        get_class(tokens): Method to retrieve the class based on class name
            from command tokens.
        get_class_instance_pair(tokens): Method to retrieve the class
            and instance based on class name and instance ID from command
            tokens.
    """

    def __init__(self, storage):
        """
        Initializes the AirBnBCommand with a storage system.

        Parameters:
            storage: The storage system to interact with.
        """
        self._storage = storage

    @abstractmethod
    def execute(self):
        """
        Abstract method to execute the command.
        """
        pass

    @abstractmethod
    def reset_tokens(self):
        """
        Abstract method to reset command tokens.
        """
        pass

    @abstractmethod
    def set_tokens(self, tokens):
        """
        Abstract method to set command tokens.

        Parameters:
            tokens (list[str]): list containing command tokens.
        """
        pass

    @staticmethod
    def get_class_name(tokens):
        """
        Static method to extract class name from command tokens.

        Parameters:
            tokens (SealedDict): Dictionary containing command tokens.

        Returns:
            str: The class name extracted from the tokens,
            or None if not found.
        """
        class_name = tokens['class_name']

        if not class_name:
            print("** class name missing **")
            return None

        return class_name

    @staticmethod
    def get_instance_id(tokens):
        """
        Static method to extract instance ID from command tokens.

        Parameters:
            tokens (SealedDict): Dictionary containing command tokens.

        Returns:
            str: The instance ID extracted from the tokens,
            or None if not found.
        """
        _id = tokens['instance_id']

        if not _id:
            print("** instance id missing **")
            return None

        return _id

    @staticmethod
    def get_attribute_name_value_pair(tokens):
        """
        Static method to extract attribute name-value pair from command tokens.

        Parameters:
            tokens (SealedDict): Dictionary containing command tokens.

        Returns:
            tuple: A tuple containing the attribute name and
                value extracted from the tokens, or None if either the
                attribute name or value is missing or invalid.
        """
        attribute_name = tokens['attribute_name']
        attribute_value = tokens['attribute_value']

        if not attribute_name:
            print("** attribute name missing **")
            return None
        if not attribute_value:
            print("** value missing **")
            return None

        attribute_value = parse_value(attribute_value)

        if not attribute_value:
            return None

        return attribute_name, attribute_value

    def get_class(self, tokens):
        """
        Method to retrieve the class based on class name from command tokens.

        Parameters:
            tokens (SealedDict): Dictionary containing command tokens.

        Returns:
            class: The class corresponding to the class name
                extracted from the tokens, or None if the class doesn't exist.
        """
        class_name = self.get_class_name(tokens)
        if not class_name:
            return None

        _class = self._storage.get_class(class_name)
        if not _class:
            print("** class doesn't exist **")
            return None

        return _class

    def get_instance(self, tokens):
        """
        Method to retrieve the class and instance based on class name
        and instance ID from command tokens.

        Parameters:
            tokens (SealedDict): Dictionary containing command tokens.

        Returns:
            (BaseModel): An instance corresponding
                    to the class name and instance ID extracted from the
                    tokens, or None if either the class or instance is
                    not found.
        """
        _class = self.get_class(tokens)
        if not _class:
            return None

        _id = self.get_instance_id(tokens)
        if not _id:
            return None

        instance = self._storage.find(_class.__name__, _id)
        if not instance:
            print("** no instance found **")
            return None

        return instance


class CreateCommand(AirBnBCommand):
    """
    CreateCommand is a concrete subclass of AirBnBCommand for creating objects.

    Methods:
        __init__(storage): Initializes the CreateCommand with a storage system.
        set_tokens(tokens): Sets command tokens for creating objects.
        reset_tokens(): Resets command tokens.
        execute(): Executes the create command.
    """

    def __init__(self, storage):
        """
        Initializes the CreateCommand with a storage system.

        Parameters:
            storage: The storage system to interact with.
        """
        super().__init__(storage)
        self.__tokens = SealedDict({'class_name': "", 'params': ()})

    def set_tokens(self, tokens):
        """
        Sets command tokens for creating objects.

        Parameters:
            tokens (list): A list of tokens representing the object to create.
        """
        for key, value in zip(self.__tokens,
                              ["".join(tokens[:1]), tuple(tokens[1:])]):
            self.__tokens[key] = value

    def reset_tokens(self):
        """Resets command tokens."""
        self.__tokens['class_name'] = ""
        self.__tokens['params'] = ()

    def execute(self):
        """Executes the create command."""
        _class = self.get_class(self.__tokens)
        if not _class:
            return

        params = parse_params(self.__tokens['params'])

        instance = _class(**params)
        print(instance.id)

        instance.save()


class ShowCommand(AirBnBCommand):
    """
    ShowCommand is a concrete subclass of AirBnBCommand for showing objects.

    Methods:
        __init__(storage): Initializes the ShowCommand with a storage system.
        set_tokens(tokens): Sets command tokens for showing objects.
        reset_tokens(): Resets command tokens.
        execute(): Executes the show command.
    """

    def __init__(self, storage):
        """
        Initializes the ShowCommand with a storage system.

        Parameters:
            storage: The storage system to interact with.
        """
        super().__init__(storage)
        self.__tokens = SealedDict({'class_name': "", 'instance_id': ""})

    def set_tokens(self, tokens):
        """
        Sets command tokens for showing objects.

        Parameters:
            tokens (list): A list of tokens representing the object to show.
        """
        for key, value in zip(self.__tokens, tokens):
            self.__tokens[key] = value

    def reset_tokens(self):
        """Resets command tokens."""
        self.__tokens['class_name'] = ""
        self.__tokens['instance_id'] = ""

    def execute(self):
        """Executes the show command."""
        instance = self.get_instance(self.__tokens)
        if not instance:
            return

        print(instance)


class DestroyCommand(AirBnBCommand):
    """
    DestroyCommand is a concrete subclass of AirBnBCommand for
    deleting objects.

    Methods:
        __init__(storage): Initializes the DestroyCommand with a
        storage system.
        set_tokens(tokens): Sets command tokens for deleting objects.
        reset_tokens(): Resets command tokens.
        execute(): Executes the destroy command.
    """

    def __init__(self, storage):
        """
        Initializes the DestroyCommand with a storage system.

        Parameters:
            storage: The storage system to interact with.
        """
        super().__init__(storage)
        self.__tokens = SealedDict({'class_name': "", 'instance_id': ""})

    def set_tokens(self, tokens):
        """
        Sets command tokens for deleting objects.

        Parameters:
            tokens (list): A list of tokens representing the object to delete.
        """
        for key, value in zip(self.__tokens, tokens):
            self.__tokens[key] = value

    def reset_tokens(self):
        """Resets command tokens."""
        self.__tokens['class_name'] = ""
        self.__tokens['instance_id'] = ""

    def execute(self):
        """Executes the destroy command."""
        instance = self.get_instance(self.__tokens)
        if not instance:
            return

        instance.delete()
        self._storage.save()


class AllCommand(AirBnBCommand):
    """
    AllCommand is a concrete subclass of AirBnBCommand for
    retrieving all objects.

    Methods:
        __init__(storage): Initializes the AllCommand with a storage system.
        set_tokens(tokens): Sets command tokens for retrieving objects.
        reset_tokens(): Resets command tokens.
        execute(): Executes the command to retrieve all objects.
    """

    def __init__(self, storage):
        """
        Initializes the AllCommand with a storage system.

        Parameters:
            storage: The storage system to interact with.
        """
        super().__init__(storage)
        self.__tokens = SealedDict({'class_name': ""})

    def set_tokens(self, tokens):
        """
        Sets command tokens for retrieving objects.

        Parameters:
            tokens (list): A list of tokens representing
            the object to retrieve.
        """
        for key, value in zip(self.__tokens, tokens):
            self.__tokens[key] = value

    def reset_tokens(self):
        """Resets command tokens."""
        self.__tokens['class_name'] = ""

    def execute(self):
        """Executes the command to retrieve all objects."""
        class_name = self.__tokens['class_name']
        if not class_name:
            print(self._storage.find_all())
            return

        _class = self.get_class(self.__tokens)
        if not _class:
            return

        print(self._storage.find_all(class_name=_class.__name__))


class AbstractUpdateCommand(AirBnBCommand, ABC):
    """
    AbstractUpdateCommand is an abstract class inheriting from
    AirBnBCommand and ABC. It defines the structure of an update
    command and specifies the check_tokens method.

    Methods:
        check_tokens(tokens): Abstract method to check if
        the provided tokens are valid.
    """

    @abstractmethod
    def check_tokens(self, tokens):
        """
        Check if the provided tokens are valid for the update command.

        Parameters:
            tokens (list): List of tokens representing the update command.

        Returns:
            bool: True if the tokens are valid, False otherwise.
        """
        pass


class UpdateCommand(AbstractUpdateCommand):
    """
    UpdateCommand is a concrete subclass of AbstractUpdateCommand.
    It coordinates different update strategies based on the provided tokens.

    Methods:
        check_tokens(tokens): Checks if the provided tokens are valid.
        set_tokens(tokens): Sets the tokens for the update command.
        reset_tokens(): Resets the tokens.
        execute(): Executes the update command.
    """

    def __init__(self, storage):
        """
        Initializes the UpdateCommand with a storage system.

        Parameters:
            storage: The storage system to interact with.
        """
        super().__init__(storage)

        self.__update_commands = FrozenDict({
            "update_with_key_value_pair":
                UpdateWithNameValuePairCommand(storage),
            "update_with_dict":
                UpdateWithDictCommand(storage)
        })

        default = self.__update_commands["update_with_key_value_pair"]
        self.__default_update_command = default
        self.__current_update_command = None

    def check_tokens(self, tokens):
        """
        Checks if the provided tokens are valid for the update command.

        Parameters:
            tokens (list): List of tokens representing the update command.

        Returns:
            bool: True if the tokens are valid, False otherwise.
        """
        return False

    def set_tokens(self, tokens):
        """
        Sets the tokens for the update command.

        Parameters:
            tokens (list): List of tokens representing the update command.
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
        """Resets the tokens."""
        if not self.__current_update_command:
            self.__default_update_command.reset_tokens()
            return

        self.__current_update_command.reset_tokens()
        self.__current_update_command = None

    def execute(self):
        """Executes the update command."""
        if not self.__current_update_command:
            self.__default_update_command.execute()
            return

        self.__current_update_command.execute()


class UpdateWithNameValuePairCommand(AbstractUpdateCommand):
    """
    UpdateWithNameValuePairCommand is a concrete subclass of
    AbstractUpdateCommand. It updates an object's attribute
    with a new value based on the provided tokens.

    Methods:
        check_tokens(tokens): Checks if the provided tokens are valid.
        set_tokens(tokens): Sets the tokens for the update command.
        reset_tokens(): Resets the tokens.
        execute(): Executes the update command.
    """

    def __init__(self, storage):
        """
        Initializes the UpdateWithNameValuePairCommand with a storage system.

        Parameters:
            storage: The storage system to interact with.
        """
        super().__init__(storage)

        self.__tokens = SealedDict({
            'class_name': "",
            'instance_id': "",
            'attribute_name': "",
            'attribute_value': "",
        })

    def check_tokens(self, tokens):
        """
        Checks if the provided tokens are valid for the update command.

        Parameters:
            tokens (list): List of tokens representing the update command.

        Returns:
            bool: True if the tokens are valid, False otherwise.
        """
        return len(tokens) >= 4 and type(tokens[2]) is str

    def set_tokens(self, tokens):
        """
        Sets the tokens for the update command.

        Parameters:
            tokens (list): List of tokens representing the update command.
        """
        for key, value in zip(self.__tokens, tokens):
            self.__tokens[key] = value

    def reset_tokens(self):
        """Resets the tokens."""
        self.__tokens['class_name'] = ""
        self.__tokens['instance_id'] = ""
        self.__tokens['attribute_name'] = ""
        self.__tokens['attribute_value'] = ""

    def execute(self):
        """Executes the update command."""
        instance = self.get_instance(self.__tokens)
        if not instance:
            return

        attribute_name_value_pair = self.get_attribute_name_value_pair(
            self.__tokens)

        if not attribute_name_value_pair:
            return

        name, value = attribute_name_value_pair

        instance.update(**{name: value})
        self._storage.save()


class UpdateWithDictCommand(AbstractUpdateCommand):
    """
    UpdateWithDictCommand is a concrete subclass of AbstractUpdateCommand.
    It updates an object's attributes with values from a dictionary
    based on the provided tokens.

    Methods:
        check_tokens(tokens): Checks if the provided tokens are valid.
        set_tokens(tokens): Sets the tokens for the update command.
        reset_tokens(): Resets the tokens.
        execute(): Executes the update command.
    """

    def __init__(self, storage):
        """
        Initializes the UpdateWithDictCommand with a storage system.

        Parameters:
            storage: The storage system to interact with.
        """
        super().__init__(storage)

        self.__tokens = SealedDict({
            'class_name': "",
            'instance_id': "",
            'dictionary': {}
        })

    def check_tokens(self, tokens):
        """
        Checks if the provided tokens are valid for the update command.

        Parameters:
            tokens (list): List of tokens representing the update command.

        Returns:
            bool: True if the tokens are valid, False otherwise.
        """
        return len(tokens) >= 3 and type(tokens[2]) is dict

    def set_tokens(self, tokens):
        """
        Sets the tokens for the update command.

        Parameters:
            tokens (list): List of tokens representing the update command.
        """
        for key, value in zip(self.__tokens, tokens):
            self.__tokens[key] = value

    def reset_tokens(self):
        """Resets the tokens."""
        self.__tokens['class_name'] = ""
        self.__tokens['instance_id'] = ""
        self.__tokens['dictionary'] = {}

    def execute(self):
        """Executes the update command."""
        instance = self.get_instance(self.__tokens)
        if not instance:
            return

        dictionary = self.__tokens['dictionary']
        if not dictionary:
            return

        instance.update(**dictionary)
        self._storage.save()


class CountCommand(AirBnBCommand):
    """
    CountCommand is a concrete subclass of AirBnBCommand for counting
    the number of class objects in storage.

    Methods:
        set_tokens(tokens): Sets the tokens for the command.
        reset_tokens(): Resets the tokens.
        execute(): Executes the command.
    """

    def __init__(self, storage):
        """
        Initializes the CountCommand with a storage system.

        Parameters:
            storage(Storage): The storage system to interact with.
        """
        super().__init__(storage)
        self.__tokens = SealedDict({'class_name': ""})

    def set_tokens(self, tokens):
        """
        Sets the tokens for the command.

        Parameters:
            tokens (list): List of tokens representing the command.
        """
        for key, value in zip(self.__tokens, tokens):
            self.__tokens[key] = value

    def reset_tokens(self):
        """Resets the tokens."""
        self.__tokens['class_name'] = ""

    def execute(self):
        """Executes the command."""
        _class = self.get_class(self.__tokens)
        if not _class:
            return

        print(self._storage.count(class_name=_class.__name__))
