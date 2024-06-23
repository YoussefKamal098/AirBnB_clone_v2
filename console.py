#!/usr/bin/python3
"""
This module defines the HBNBCommand class, which implements
a command-line interface for an AirBnB-like application.
"""

import cmd
import readline
import subprocess

from models.dict_wrapper import FrozenDict
from utils import extract_method_call, parse_line

from console_commands import (
    CreateCommand,
    ShowCommand,
    AllCommand,
    DestroyCommand,
    UpdateCommand,
    CountCommand
)
import models


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class represents the command-line interface for
    the AirBnB-like application.
   """

    prompt = "(hbnb) "
    __history_file = ".airbnb_cmd_history.txt"
    __MAX_HIST = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__airbnb_commands = FrozenDict({
            "create": CreateCommand(models.storage),
            "show": ShowCommand(models.storage),
            "destroy": DestroyCommand(models.storage),
            "all": AllCommand(models.storage),
            "update": UpdateCommand(models.storage),
            "count": CountCommand(models.storage)
        })

        self.__history = []
        self.__current_cmd = ""

    def preloop(self):
        self.load_history()

    def postloop(self):
        self.save_history()

    def do_create(self, line):
        """
        Create a new class instance and print its id.
        Usage: create <Class name> <param 1> <param 2> <param 3>...
            Param syntax: <key name>=<value>
            Value syntax:
                String: "<value>" => starts with a double quote
                    all underscores _ will be replaced by spaces .
                    Example: You want to set the string `My little house`
                    to the attribute `name`, the command line must be
                    `name="My_little_house`"
                Float: <unit>.<decimal> => contains a dot .
                Integer: <number> => default case
            If any parameter doesn’t fit with these requirements or can’t be
            recognized correctly by the program, it will be skipped

        """
        self.__airbnb_commands["create"].execute()

    def do_show(self, line):
        """
        Display the string representation of a class instance of a given id.
        Usage: show <class> <id> or <class>.show(<id>)
        """
        self.__airbnb_commands["show"].execute()

    def do_destroy(self, line):
        """
        Delete a class instance of a given id.
        Usage: destroy <class> <id> or <class>.destroy(<id>)
        """
        self.__airbnb_commands["destroy"].execute()

    def do_all(self, line):
        """
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.

        Usage: all or all <class> or <class>.all()
        """
        self.__airbnb_commands["all"].execute()

    def do_count(self, line):
        """
        counting the number of class Object in storage.

        Usage: count <class> or <class>.count()
        """
        self.__airbnb_commands["count"].execute()

    def do_update(self, line):
        """
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.

        Usage: update <class> <id> <attribute_name> <attribute_value> or
              <class>.update(<id>, <attribute_name>, <attribute_value>) or
              <class>.update(<id>, <dictionary>)
        """
        self.__airbnb_commands["update"].execute()

    def do_quit(self, line):
        """
        Quits the command-line interface.
        """
        models.storage.close()

        return True

    def do_EOF(self, line):
        """
        Quits the command-line interface.
        """
        models.storage.close()

        return True

    def do_clear(self, line):
        """
        Clears the Screen
        """
        try:
            result = subprocess.run(["clear"], capture_output=True)
        except OSError as err:
            print(err)
            return

        print(result.stderr.decode(), end="")
        print(result.stdout.decode(), end="")

    def default(self, line):
        """
        Handles unmatched commands by delegating execution to
        the parent class's default method. If parsing fails,
        an error message is printed.

        Parameters:
            line (str): The command line input.
        """
        extracted_data = extract_method_call(line)
        if not extracted_data:
            super().default(line)
            return

        class_name, function_name, function_args = extracted_data
        if function_name not in self.__airbnb_commands:
            return

        tokens = [class_name]

        if isinstance(function_args, tuple):
            tokens.extend(function_args)
        else:
            tokens.append(function_args)

        self.__current_cmd = function_name
        self.__airbnb_commands[function_name].set_tokens(tokens)
        self.__airbnb_commands[function_name].execute()

    def emptyline(self):
        """
        Handles empty input.
        """
        pass

    def _precmd(self, line):
        """
        Processes the command before execution.
        Parameters:
            line (str): The command line input.
        Returns:
            str: The processed command line input.
        """
        self.add_history(line)

        tokens = parse_line(line)
        if not tokens:
            return ""

        command = tokens[0]

        self.__current_cmd = command
        if command in self.__airbnb_commands:
            self.__airbnb_commands[command].set_tokens(tokens[1:])

        return line.strip()

    def _postcmd(self, stop, line):
        """
        Processes the command after execution.

        Parameters:
            stop (bool): Flag indicating whether to stop further processing.
            line (str): The command line input.

        Returns:
            bool: Flag indicating whether to stop further processing.
        """
        if self.__current_cmd in self.__airbnb_commands:
            self.__airbnb_commands[self.__current_cmd].reset_tokens()

        self.__current_cmd = ""
        return stop

    def onecmd(self, line):
        """Processes a single command line and returns a boolean
        indicating termination.

        This method serves as the entry point for processing a user-provided
        command line. It performs the following steps:

        1. Preprocessing: Calls the `precmd` method (if defined)
            to potentially modify the input line before further processing.
        2. Command Execution: Delegates the actual command execution
            to the parent class (likely `cmd.Cmd`) by calling
            `super().onecmd(line)`.
           This invokes the appropriate command handling logic based
           on the user input.
        3. Postprocessing: Calls the `postcmd` method (if defined)
           to perform any necessary actions after the command has
           been processed. This allows for custom post-execution tasks.

        Parameter:
            line (str): The user-provided command line string.

        Returns:
            bool: True if the command indicates termination
            (e.g., "quit"), False otherwise.
        """
        line = self._precmd(line)
        stop = super().onecmd(line)
        self._postcmd(stop, line)

        return stop

    def do_history(self, line):
        """Displays the command history maintained by the command
        interpreter.

        This method iterates through the internal command
        history (`self.__history`) and prints each command
        entry along with its corresponding index number.
        The index number can be used to recall a previous
        command using its position in the history.

        Parameter
            line (str): The user input line (typically unused in
            this implementation).
        """
        for i, line in enumerate(self.__history):
            print(f"{i:02}. {line}")

    def add_history(self, line):
        """
        Adds a command line input to the command history,
        maintaining a maximum size.
        Parameters:
            line (str): The command line input to be added.
        """
        self.__history.append(line)
        history_length = len(self.__history)

        if history_length > self.__MAX_HIST:
            self.__history.pop(0)

    def load_history(self):
        """Loads the command history from the file (if it exists)."""
        try:
            with open(self.__history_file, "r") as file:
                for line in file:
                    line = line.strip("\n")
                    self.__history.append(line)
                    readline.add_history(line)

                history_length = len(self.__history)
                if history_length > self.__MAX_HIST:
                    extra = history_length - self.__MAX_HIST
                    self.__history = self.__history[extra:]

        except FileNotFoundError:
            pass

    def save_history(self):
        """Saves the current command history to the file."""
        with open(self.__history_file, "w") as file:
            for line in self.__history:
                file.write(f"{line}\n")

    def completedefault(self, *args):
        """
        Provides basic completion for commands without
        specific complete_* methods.
        """

        classes = models.storage.get_classes_names()
        return [module for module in classes if module.startswith(args[0])]


if __name__ == '__main__':
    HBNBCommand().cmdloop()
