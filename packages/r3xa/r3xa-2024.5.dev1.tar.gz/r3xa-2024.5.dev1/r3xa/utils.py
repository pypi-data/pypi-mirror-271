# -*- coding: utf-8 -*-
import random
import string
import importlib.resources
import json
import os
import slugify
from pygments import highlight, lexers, formatters


#######################
# Utilitary functions #
#######################


def random_slug(n: int = 6):
    """Generates a random string  of n ascii lowercase chars.
    This function is used to generates unique identifiers.
    """
    chars = string.ascii_lowercase  # + string.digits
    return "".join([random.choice(chars) for i in range(n)])


def obj(value):
    """Convert a value as a dictionary if possible.
    This function is used in the meta data classes to convert them to json parsable objects.
    It implies that the object have their `self.__iter__` functions implemented.
    """
    if isinstance(value, int):
        return value

    if isinstance(value, str) and value.strip() == "":
        return None

    # check if only kind is set and return None
    # this can happen with hidden field in the gui
    if isinstance(value, dict) and "kind" in value and len(value) == 1:
        return None

    if isinstance(value, list):
        return [obj(v) for v in value if obj_is_true(v)]

    if isinstance(value, dict):
        return {k: obj(v) for k, v in value.items() if obj_is_true(v)}

    try:
        return obj(dict(value))
    except (TypeError, ValueError):
        return value


def obj_is_true(value):
    """Determine if a value is true or not basically used to have int 0 == True"""
    if isinstance(value, int):
        return value >= 0

    if isinstance(value, float):
        return True

    if isinstance(value, dict):
        if "kind" in value and len(value) == 1:
            return False

    return value

    # if isinstance(value, list):
    #     return any([obj(v) for v in value])
    #
    # if isinstance(value, dict):
    #     return any([obj(v) for v in value.values()])
    #
    # r = True if value else False
    # return r


def obj_iter(instance):
    """Defines the conversion between instance and dictionnary
    It does not ouput unset values and convert list of Iterable to dict if possible.
    """
    for k, v in instance.__dict__.items():
        # return empty lists
        # convert list of Iterable to list of dict if possible
        # used for our own classes where __iter__ is defined
        if isinstance(v, list):
            v = [obj(_) for _ in v if obj_is_true(v)]
            yield k, obj(v)

        # ignore unset values
        if not obj_is_true(v):
            continue

        # yield the key: value pair
        yield k, obj(v)


def get_schema():
    """Reads the current json schema of meta data located in `resources/schema.json`.
    and returns it as a dictionary.
    """
    f = importlib.resources.files("resources").joinpath("schema.json").open("r")
    payload = json.load(f)

    return payload


def to_float_or_none(f):
    try:
        return float(f)
    except (ValueError, TypeError):
        return None


def slugify_file_name(path):
    """Slugify a file name.
    - doesn't slugify the path
    - conserve the .
    - gives random name if only path
    """

    # get basename if the file and slugify
    basename = os.path.basename(path)
    basename = ".".join([slugify.slugify(_) for _ in basename.split(".")])
    # get path
    directory_path = os.path.dirname(path)
    if not len(basename):
        basename = "r3xa"
    return os.path.join(directory_path, f"{basename}")


def highlight_json(obj):
    formatted_json = json.dumps(dict(obj), sort_keys=False, indent=4)
    return highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())


def pprint(obj):
    print(highlight_json(obj))
