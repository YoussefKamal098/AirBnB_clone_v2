#!/usr/bin/python3

"""
This module provides functions for parsing and manipulating
command line inputs.
"""

from typing import Union
import re
import ast


def extract_method_call(line):
    """
    Extracts method call information (class name, function name, arguments)
    from a line using regular expressions. Handles potential errors during
    argument parsing.

    Parameters:
        line (str): The command line input.

    Returns:
        tuple or None: A tuple containing
        (class_name, function_name, function_args) if successful,
        None otherwise.
    """
    pattern = r'^([A-Z]\w*)?\s*\.\s*([A-Za-z]\w*)\s*\((.*)\)$'
    math = re.match(pattern, line)
    if not math:
        return None

    class_name, function_name, function_args_literal = math.groups()
    function_args = None

    try:
        if function_args_literal:
            function_args = ast.literal_eval(function_args_literal)
    except (SyntaxError, ValueError) as err:
        print(err)
        return None

    return class_name, function_name, function_args


def split(line):
    """
    Splits a line into tokens, considering both double and single quotes.

    Parameters:
        line (str): The line to split into tokens.

    Returns:
        list: A list of tokens extracted from the line.
    """
    tokens = []
    current_token = ''
    inside_quotes = False
    inside_single_quotes = False

    for char in line:
        if char == '"' and not inside_single_quotes:
            if inside_quotes:
                # End of quoted string
                current_token += char
                tokens.append(current_token)
                current_token = ''
            else:
                # Start of quoted string
                current_token += char
            inside_quotes = not inside_quotes
        elif char == "'" and not inside_quotes:
            if inside_single_quotes:
                # End of single quoted string
                current_token += char
                tokens.append(current_token)
                current_token = ''
            else:
                # Start of single quoted string
                current_token += char
            inside_single_quotes = not inside_single_quotes
        elif char.isspace() and not inside_quotes and not inside_single_quotes:
            # End of token
            if current_token:
                tokens.append(current_token)
                current_token = ''
        elif char in ['"', "'"] and (inside_quotes or inside_single_quotes):
            # Invalid quote inside a quoted string
            current_token += char
        else:
            current_token += char

    if current_token:
        tokens.append(current_token)

    return tokens


def parse_line(line):
    """
    Splits a command line input string into a list of tokens using shlex.
    Parameters:
        line (str): The command line input string.
    Returns:
        list: A list of tokens parsed from the input string,
        or an empty list if parsing fails.
    """
    try:
        return split(line)
    except ValueError as err:
        print(err)
        return []


def parse_value(value):
    """
    Parses and evaluates the provided value based on its syntax.

    Parameters:
        value (str): The value to parse and evaluate.

    Returns:
        Union[str, float, int]: The parsed and evaluated value.
    """
    try:
        if ((value.startswith('"') and value.endswith('"')) or
                (value.startswith("'") and value.endswith("'"))):
            # String value
            return value[1:-1]
        elif '.' in value:
            # Float value
            return float(value)
        else:
            # Integer value
            return int(value)
    except ValueError:
        return value


def parse_params(params):
    """
    Parses the parameters stored in the tokens dictionary to
    extract key-value pairs for object creation.

    The parameters are expected to be stored in the tokens
    dictionary under the key "params" as a list.

    Parameter syntax:
    <key name>=<value>

    Value syntax:
    - String: "<value>" => starts with a double quote
        - any double quote inside the value must be escaped with a backslash \
        - all underscores _ must be replaced by spaces. Example:
        name="My_little_house"
    - Float: <unit>.<decimal> => contains a dot.
    - Integer: <number> => default case

    If any parameter doesn’t fit with these requirements or can’t be recognized
    correctly by the program, it will be skipped.

    Parameters:
        params(tuple[str]): params

    Returns:
        dict: A dictionary containing the parsed key-value pairs.

    """
    # Parse and validate parameters
    kwargs = {}
    for param in params:
        key = param[:param.index("=")]
        value = param[param.index("=") + 1:]

        try:
            if ((value.startswith('"') and value.endswith('"')) or
                    (value.startswith("'") and value.endswith("'"))):
                # String value
                value = value[1:-1].replace("_", " ")
            elif '.' in value:
                # Float value
                value = float(value)
            else:
                # Integer value
                value = int(value)
        except ValueError:
            # Invalid integer format, skip it
            continue

        kwargs[key] = value

    return kwargs
