# -*- coding: utf-8 -*-
import slugify
import json
import os

from r3xa.utils import get_schema, random_slug, obj, obj_is_true, obj_iter, slugify_file_name, highlight_json, to_float_or_none
from r3xa.validation import validate

#####################
# Meta data classes #
#####################


class Unit:
    """Independant class that handles units"""

    def __init__(self, **kwargs):
        schema = get_schema()
        unit = schema["$defs"]["types"]["unit"]["properties"]
        # required = schema["$defs"]["types"]["unit"]["required"]

        for k, v in unit.items():
            if "const" in v:
                to_assign = v["const"]
            else:
                to_assign = kwargs.get(k)

            if v["type"] == "number":
                to_assign = to_float_or_none(to_assign)

            setattr(self, k, to_assign)

    def __str__(self):
        return highlight_json(self)

    def __iter__(self):
        for k, v in obj_iter(self):
            yield k, v


class DataSetFile:
    """Independant class that handles data set file (either `timestamps` or `data`) to produces json objects formated as:
    ```json
    {
        "filename": {"type": "string"},
        "delimiter": {"type": "string", "enum": [":", ",", ...]},
        "data_range": {"type": "array", "items": {"type": "string"}}
    }
    ```
    """

    def __init__(self, **kwargs):
        schema = get_schema()
        dsf = schema["$defs"]["types"]["data_set_file"]["properties"]
        # required = schema["$defs"]["types"]["unit"]["required"]

        for k, v in dsf.items():
            if "const" in v:
                to_assign = v["const"]
            else:
                to_assign = kwargs.get(k, v.get("default"))

            if v["type"] == "number":
                to_assign = to_float_or_none(to_assign)

            setattr(self, k, to_assign)

    def __iter__(self):
        for k, v in obj_iter(self):
            yield k, v

    def __str__(self):
        return highlight_json(self)


class Data:
    """Generic parent class for `data_sets`, `data_sources` and `settings`.
    It can take any `key: values` arguments to keep flexible in view of specs changes.
    Therefore it is agnostic to the specifications implemented in the scheme.

    It implements the `__iter__` function to ease the conversion to json objects.
    """

    def __init__(self, data_type, check=False, **kwargs):
        # if payload given load then delete key
        if "payload" in kwargs:
            self.load(kwargs["payload"])
            del kwargs["payload"]

        # get all attributes from the kwargs and set them
        for k, v in kwargs.items():
            if obj_is_true(v):
                setattr(self, k, obj(v))
            # setattr(self, k, v)

        # define an ID of the data as the slugified title appended with and random slug
        if not hasattr(self, "id"):
            self.id = random_slug(n=24)

        # skip the rest if no attributes had been given
        # dummy instantiation
        if not len(set(self.__dict__) - {"id", "kind"}):
            print("WARNING: Skipping full instantiation of empty Data")
            return

        # guess kind if not given
        if not hasattr(self, "kind"):
            setattr(self, "kind", self.guess_kind(data_type))

        # check for keywords (only if more than id and kind)
        if check:
            self.check_keywords(self.kind)

    def __str__(self):
        return highlight_json(self)

    def __iter__(self):
        for k, v in obj_iter(self):
            yield k, v

    def load(self, payload):
        # when you load an key/value it must fall in the 3 following possibilities
        # CASE 1: value is a simple type (string, number, ...)
        #         -> just assign the attribute to the key
        # CASE 2: value is an object (unit, ...)
        #         -> it is detected by the `kind` keyword and instantiate the appropriate class
        # CASE 3: value is a list
        #         -> each element of the must fall into CASE 1, 2 or 3

        def handle_cases_123(k, v):
            v = obj(v)

            # handle lists
            if isinstance(v, list):
                return [handle_cases_123(k, _) for _ in v if obj_is_true(_)]

            elif isinstance(v, dict):
                kind = v.get("kind")

                # handle units
                if kind == "unit":
                    o = Unit(**v)
                    # return value to assign
                    return o

                elif kind == "data_set_file":
                    f = DataSetFile(**v)
                    return f

                raise TypeError(f"Objects of kind {kind} are not handled")

            else:
                # set valid attribute
                return v

        for k, v in payload.items():
            to_be_assigned = handle_cases_123(k, v)

            # case value is empty, delete if already set in the past
            if not obj_is_true(to_be_assigned):
                if hasattr(self, k):
                    delattr(self, k)
                continue

            print(k, to_be_assigned)
            setattr(self, k, to_be_assigned)

    def guess_kind(self, data_type):
        # check for data_sets, data_sources and settings
        schema = get_schema()

        # get all attributes
        keys = set(self.__dict__) - {"id", "kind"}

        # dictionnary of missing keys for each kind
        missing_keys = {}

        # loop over all kinds and compute the candidate score
        for kind, v in schema["$defs"][data_type].items():
            properties = set(v["properties"]) - {"id", "kind"}
            required = set(v["required"]) - {"id", "kind"}

            missing = len(properties - keys)
            missing_required = len(required - keys)
            extra = len(keys - properties)

            # if more keys then propertiesor less than required then discard
            if extra or missing_required:
                continue

            missing_keys[kind] = missing

        if not len(missing_keys):
            raise ValueError(f"No kind guessed from {data_type}")

        # kind is the lowest missing keys
        kind, score = sorted(missing_keys.items(), key=lambda x: x[1])[0]
        return f"{data_type}/{kind}"

    def check_keywords(self, kind):
        """Raise ValueError if the attributes of the instance does not match
        the required keys.

        data_type/kind can be "settings/generic", "data_sources/camera", "data_sets/file", ...

        Warning:
        --------
            Does not check the data type
        """
        # check that all required data from the specs are present
        # check for data_sets, data_sources and settings
        schema = get_schema()

        # get all keys
        keys = set(self.__dict__.keys())
        ki, nd = kind.split("/")
        required = set(schema["$defs"][ki][nd]["required"])
        missing = required - keys
        if len(missing):
            raise ValueError(f"Missing at least the following keys: {missing}")


class Setting(Data):
    def __init__(self, check=False, **kwargs):
        super().__init__("settings", check, **kwargs)


class DataSource(Data):
    def __init__(self, **kwargs):
        super().__init__("data_sources", **kwargs)

    def add_input_data_set(self, data_set: Data):
        if not hasattr(self, "input_data_sets") or not isinstance(getattr(self, "input_data_sets"), list):
            self.input_data_sets = []
        self.input_data_sets.append(data_set.id)
        # self.input_data_set = data_set.id


class DataSet(Data):
    def __init__(self, **kwargs):
        super().__init__("data_sets", **kwargs)

    def add_data_source(self, data_source: Data):
        if not hasattr(self, "data_sources") or not isinstance(getattr(self, "data_sources"), list):
            self.data_sources = []
        self.data_sources.append(data_source.id)
        # self.data_sources = datasource.id


class MetaData:
    def __init__(self, **kwargs):
        schema = get_schema()

        # if payload given load then delete key
        if "payload" in kwargs:
            self.load(kwargs["payload"])
            del kwargs["payload"]

        for k, v in kwargs.items():
            if obj_is_true(v):
                setattr(self, k, v)

        # add by default settings / data_sources and data_sets
        for k in ["settings", "data_sources", "data_sets"]:
            if not hasattr(self, k):
                setattr(self, k, [])

            # sanity check to remove duplicated ID
            data = {d.id: d for d in getattr(self, k)}
            setattr(self, k, list(data.values()))

        # enforce version from schema
        self.version = str(schema["properties"]["version"]["const"])

    def __iter__(self):
        for k, v in obj_iter(self):
            yield k, v

    def __str__(self):
        return highlight_json(self)

    def validate(self):
        validate(dict(self))

    def create_or_modify(self, what, where):
        """Insure that when we had Data we don't duplicate the same ID."""
        # get existing data and use id as a key
        data = {d.id: d for d in getattr(self, where)} if hasattr(self, where) else {}

        # add current data to existing (by the key)
        data[what.id] = what

        # convert dict to list of data
        setattr(self, where, list(data.values()))

    def add_setting(self, setting: Setting):
        self.create_or_modify(setting, "settings")

    def add_data_source(self, data_source: DataSource):
        self.create_or_modify(data_source, "data_sources")

    def add_data_set(self, data_set: DataSet):
        self.create_or_modify(data_set, "data_sets")

    def load(self, payload):
        """Fill class attributes based on a payload"""

        # set global attributes
        for k, v in payload.items():
            # ignore case of list of settings or data_sources or data_sets
            if k in ["settings", "data_sources", "data_sets"]:
                continue

            # case object is empty, delete if already set in the past
            if not obj_is_true(v):
                if hasattr(self, k):
                    delattr(self, k)
                continue

            # match type

            # set valid attribute
            setattr(self, k, obj(v))

        # set settings
        for p in payload.get("settings", []):
            # discard empty objects
            if not len(p):
                continue
            s = Setting(payload=p)
            self.add_setting(s)

        # set data sources
        for p in payload.get("data_sources", []):
            # discard empty objects
            if not len(p):
                continue
            d = DataSource(payload=p)
            self.add_data_source(d)

        # set data sets
        for p in payload.get("data_sets", []):
            # discard empty objects
            if not len(p):
                continue
            d = DataSet(payload=p)
            self.add_data_set(d)

    def save_json(self, name: str = None, folder: str = None, check: bool = True):
        """Appends .json to name"""
        # check validity
        if check:
            validate(dict(self))

        # slugify the json file name
        # if not set use the title
        if name:
            name = slugify_file_name(name)
        else:
            name = slugify.slugify(self.title)

        # write file
        full_path = os.getcwd()
        if folder:
            full_path = os.path.join(full_path, folder)
        full_path = os.path.join(full_path, f"{name}.json")

        print(f"Saving {full_path}")
        json.dump(dict(self), open(full_path, "w"), indent=4)
