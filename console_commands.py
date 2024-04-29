#!/usr/bin/python3
"""
This module defines a set of commands used in an AirBnB application.
"""

from abc import ABC, abstractmethod


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
    def get_model_name(tokens):
        """
        Retrieves the model name token.

        Parameters:
            tokens (dict[str, any]): A dictionary of tokens parsed
            from the command line input.
        Returns:
            str: The model name token.
        """
        model_name = tokens.get("model_name", None)

        if not model_name:
            print("** class name missing **")
            return None

        return model_name

    @staticmethod
    def get_instance_id(tokens):
        """
        Retrieves the instance ID token.

        Parameters:
            tokens (dict[str, any]): A dictionary of tokens parsed
            from the command line input.
        Returns:
            str: The instance ID token.
        """
        _id = tokens.get("instance_id", None)

        if not _id:
            print("** instance id missing **")
            return None

        return _id

    @staticmethod
    def get_attribute_name_value_pair(tokens):
        """
        Retrieves attribute name-value pair tokens.

        Parameters:
            tokens (dict[str, any]): A dictionary of tokens parsed
            from the command line input.
        Returns:
            dict: A dictionary containing attribute name-value pair.
        """
        attribute_name = tokens.get("attribute_name", None)
        attribute_value = tokens.get("attribute_value", None)

        if not attribute_name:
            print("** attribute name missing **")
            return None
        if not attribute_value:
            print("** value missing **")
            return None

        return {"attribute_name": attribute_name,
                "attribute_value": attribute_value}

    def get_model_class(self, tokens):
        """
        Retrieves the model class based on the model name.

         Parameters:
            tokens (dict[str, any]): A dictionary of tokens parsed
            from the command line input.
        Returns:
            class: The model class.
        """
        model_name = self.get_model_name(tokens)
        if not model_name:
            return None

        model_class = self._storage.get_model_class(model_name)
        if not model_class:
            return None

        return model_class

    def get_model_instance(self, tokens):
        """
        Retrieves the model instance based on the model class and instance ID.

         Parameters:
            tokens (dict[str, any]): A dictionary of tokens parsed
            from the command line input.
        Returns:
            tuple: A tuple containing the model class and model instance.
        """
        model_class = self.get_model_class(tokens)
        if not model_class:
            return None

        _id = self.get_instance_id(tokens)
        if not _id:
            return None

        instance = self._storage.find_obj(model_class.__name__, _id)
        if not instance:
            return None

        return model_class, instance


class CreateCommand(AirBnBCommand):
    """
    CreateCommand is a concrete subclass of AirBnBCommand for
    creating new objects.
    """

    def __init__(self, storage):
        super().__init__(storage)

        self.__tokens = {
            "model_name": None,
        }

    def set_tokens(self, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list[str]): A list of token values.

        """
        for key, value in zip(self.__tokens, tokens):
            self.__tokens[key] = value

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        for key in self.__tokens.keys():
            self.__tokens[key] = None

    def execute(self):
        """
        Executes the create command.
        """
        model_class = self.get_model_class(self.__tokens)
        if not model_class:
            return

        instance = model_class()
        print(instance.id)

        instance.save()


class ShowCommand(AirBnBCommand):
    """
    ShowCommand is a concrete subclass of AirBnBCommand for
    displaying object details.
    """

    def __init__(self, storage):
        super().__init__(storage)

        self.__tokens = {
            "model_name": None,
            "instance_id": None,
        }

    def set_tokens(self, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list[str]): A list of token values.

        """
        for key, value in zip(self.__tokens, tokens):
            self.__tokens[key] = value

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        for key in self.__tokens.keys():
            self.__tokens[key] = None

    def execute(self):
        """
        Executes the show command.
        """
        model_instance = self.get_model_instance(self.__tokens)
        if not model_instance:
            return

        _, instance = model_instance
        print(instance)


class DestroyCommand(AirBnBCommand):
    """
    DestroyCommand is a concrete subclass of AirBnBCommand for
    deleting objects.
    """

    def __init__(self, storage):
        super().__init__(storage)

        self.__tokens = {
            "model_name": None,
            "instance_id": None,
        }

    def set_tokens(self, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list[str]): A list of token values.
        """
        for key, value in zip(self.__tokens, tokens):
            self.__tokens[key] = value

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        for key in self.__tokens.keys():
            self.__tokens[key] = None

    def execute(self):
        """
        Executes the destroy command.
        """
        model_instance = self.get_model_instance(self.__tokens)
        if not model_instance:
            return

        model_class, instance = model_instance
        self._storage.remove_obj(model_class.__name__, instance.id)


class AllCommand(AirBnBCommand):
    """
    AllCommand is a concrete subclass of AirBnBCommand for
    displaying all objects or objects of a specific type.
    """

    def __init__(self, storage):
        super().__init__(storage)

        self.__tokens = {
            "model_name": None,
        }

    def set_tokens(self, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list[str]): A list of token values.
        """
        for key, value in zip(self.__tokens, tokens):
            self.__tokens[key] = value

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        for key in self.__tokens.keys():
            self.__tokens[key] = None

    def execute(self):
        """
        Executes the all command.
        """
        model_name = self.__tokens.get("model_name", None)
        if not model_name:
            print(self._storage.find_all())
            return

        model_class = self.get_model_class(self.__tokens)
        if not model_class:
            return

        print(self._storage.find_all(model_name=model_class.__name__))


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

        self.__tokens = {
            "model_name": None,
            "instance_id": None,
            "attribute_name": None,
            "attribute_value": None,
        }

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
            tokens (list): A list of token values.
        """
        for key, value in zip(self.__tokens, tokens):
            self.__tokens[key] = value

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        for key in self.__tokens.keys():
            self.__tokens[key] = None

    def execute(self):
        """
        Executes the update command.
        """
        model_instance = self.get_model_instance(self.__tokens)
        if not model_instance:
            return

        attribute_name_value_pair = self.get_attribute_name_value_pair(
                                                        self.__tokens)

        if not attribute_name_value_pair:
            return

        model_class, instance = model_instance
        self._storage.update_obj_attribute(
            model_class.__name__, instance.id,
            **attribute_name_value_pair
        )


class UpdateWithDictCommand(AbstractUpdateCommand):
    """
    UpdateCommand is a concrete subclass of AirBnBCommand for
    updating attributes of an object with dictionary.
    """

    def __init__(self, storage):
        super().__init__(storage)

        self.__tokens = {
            "model_name": None,
            "instance_id": None,
            "dictionary": None
        }

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
            tokens (list): A list of token values.
        """
        for key, value in zip(self.__tokens, tokens):
            self.__tokens[key] = value

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        for key in self.__tokens.keys():
            self.__tokens[key] = None

    def execute(self):
        """
        Executes the update command.
        """
        model_instance = self.get_model_instance(self.__tokens)
        if not model_instance:
            return

        dictionary = self.__tokens.get("dictionary", None)
        if not dictionary:
            return

        model_class, instance = model_instance
        self._storage.update_obj_attributes(
            model_class.__name__, instance.id, **dictionary)


class CountCommand(AirBnBCommand):
    """
    CountCommand is a concrete subclass of AirBnBCommand for
    counting the number of class Object in storage.
    """

    def __init__(self, storage):
        super().__init__(storage)

        self.__tokens = {
            "model_name": None,
        }

    def set_tokens(self, tokens):
        """
        Sets the tokens based on the provided values.

        Parameters:
            tokens (list[str]): A list of token values.
        """
        for key, value in zip(self.__tokens, tokens):
            self.__tokens[key] = value

    def reset_tokens(self):
        """
        Resets the tokens dictionary to default values.
        """
        for key in self.__tokens.keys():
            self.__tokens[key] = None

    def execute(self):
        """
        Executes the update command.
        """
        model_class = self.get_model_class(self.__tokens)
        if not model_class:
            return

        print(self._storage.count(model_name=model_class.__name__))
