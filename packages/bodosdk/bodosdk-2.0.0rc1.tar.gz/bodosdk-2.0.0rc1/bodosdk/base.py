import enum
import logging
import re
from typing import Optional, Dict

import pydantic
from pydantic import Field


class APIBaseModel(pydantic.BaseModel):
    """
    TODO: docs string
    """

    _deprecated_fields: Optional[Dict] = Field(
        default_factory=dict, alias="_deprecatedFields"
    )
    _deprecated_methods: Optional[Dict] = Field(
        default_factory=dict, alias="_deprecatedMethods"
    )

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True

    def __init__(self, **data):
        super().__init__(**data)

        self._deprecated_fields = (
            self._deprecated_fields if isinstance(self._deprecated_fields, dict) else {}
        )

        self._deprecated_fields.update(
            data.get("_deprecated_fields", data.get("_deprecatedFields", {}))
        )
        self._deprecated_methods = (
            self._deprecated_methods
            if isinstance(self._deprecated_methods, dict)
            else {}
        )
        self._deprecated_methods.update(
            data.get("_deprecated_methods", data.get("_deprecatedMethods", {}))
        )

    def __getitem__(self, item):
        item = camel_to_snake(item)
        return getattr(self, item)

    def __setitem__(self, key, value):
        key = camel_to_snake(key)
        setattr(self, key, value)

    def __setattr__(self, key, value):
        key = camel_to_snake(key)
        if key.startswith("_"):
            self.__dict__[key] = value
            return
        super().__setattr__(key, value)

    def __getattribute__(self, key):
        key = camel_to_snake(key)
        return super().__getattribute__(key)


class SDKBaseModel(pydantic.BaseModel):
    _deprecated_fields: Optional[Dict] = Field(
        default_factory=dict, alias="_deprecatedFields"
    )
    _deprecated_methods: Optional[Dict] = Field(
        default_factory=dict, alias="_deprecatedMethods"
    )
    _mutable: bool = False

    class Config:
        """
        Configuration for Pydantic models.
        https://docs.pydantic.dev/latest/api/config/
        """

        extra = "ignore"
        allow_population_by_field_name = True

    def __init__(self, **data):
        self._mutable = True
        super().__init__(**data)
        self._modified_fields = set()
        self._deprecated_fields = (
            self._deprecated_fields if isinstance(self._deprecated_fields, dict) else {}
        )
        self._deprecated_fields.update(
            data.get("_deprecated_fields", data.get("_deprecatedFields", {}))
        )
        self._deprecated_methods = (
            self._deprecated_methods
            if isinstance(self._deprecated_methods, dict)
            else {}
        )
        self._deprecated_methods.update(
            data.get("_deprecated_methods", data.get("_deprecatedMethods", {}))
        )
        self._modified = True
        self._mutable = False

    def __getitem__(self, item):
        item = camel_to_snake(item)
        return getattr(self, item)

    def __setitem__(self, key, value):
        key = camel_to_snake(key)
        setattr(self, key, value)

    def __setattr__(self, key, value):
        key = camel_to_snake(key)
        if key.startswith("_"):
            self.__dict__[key] = value
            return
        if self._mutable:
            if getattr(self, key) != value:
                super().__setattr__(key, value)
                self._modified = True
                self._modified_fields.add(key)
            if key in self._deprecated_fields and not {
                "_deprecated_fields",
                "_deprecatedFields",
            }.intersection(self._deprecated_field[key].keys()):
                deprecated_values = self._modified_fields[key].get(
                    "deprecated_values", None
                )
                if is_hashable(value) and value in deprecated_values:
                    msg = (
                        f"Value {value} for field {key} of class {self.__class__.__name__} "
                        f"will be deprecated in version {self._deprecated_fields[key].get('version')}. "
                        f"Value be supported till {self._deprecated_fields[key].get('end_of_support')}. "
                        f"Additional notes: {self._deprecated_fields[key].get('notes')}"
                    )
                else:
                    msg = (
                        f"Field {key} of class {self.__class__.__name__} "
                        f"will be deprecated in version {self._deprecated_fields[key].get('version')}. "
                        f"Field will be supported till {self._deprecated_fields[key].get('end_of_support')}. "
                        f"Additional notes: {self._deprecated_fields[key].get('notes')}"
                    )
                print(msg)
                logging.warning(msg)
        else:
            raise TypeError("Object is immutable")

    def __getattribute__(self, key):
        key = camel_to_snake(key)
        value = super().__getattribute__(key)
        if key.startswith("_"):
            return value
        if key in self._deprecated_fields:
            deprecated_values = self._deprecated_fields[key].get(
                "deprecated_values", set()
            )
            if is_hashable(value) and value in deprecated_values:
                msg = (
                    f"Value {value} for field {key} of class {self.__class__.__name__} "
                    f"will be deprecated in version {self._deprecated_fields[key].get('version')}. "
                    f"Value be supported till {self._deprecated_fields[key].get('end_of_support')}. "
                    f"Additional notes: {self._deprecated_fields[key].get('notes')}"
                )
            else:
                msg = (
                    f"Field {key} of class {self.__class__.__name__} "
                    f"will be deprecated in version {self._deprecated_fields[key].get('version')}. "
                    f"Field will be supported till {self._deprecated_fields[key].get('end_of_support')}. "
                    f"Additional notes: {self._deprecated_fields[key].get('notes')}"
                )
            print(msg)
            logging.warning(msg)
        return value

    def _update(self, data):
        self._mutable = True
        for k, v in data.items():
            if k.startswith("_deprecated") and isinstance(self[k], dict):
                self[k].update(v)
                continue
            try:
                self[k] = v
            except (AttributeError, ValueError):
                continue
        self._saved = False
        self._mutable = False
        return self

    def get(self, key, default=None):
        return self[key] or default

    def items(self):
        for field in self.__fields__:
            yield field, self[field]


def camel_to_snake(name):
    # Insert underscores before uppercase letters and convert to lowercase
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


class APIKeys(pydantic.BaseModel):
    """
    Class representing Bodo Platform API keys used for auth token generation
    """

    client_id: str
    secret_key: str


class PaginationOrder(str, enum.Enum):
    ASC = "ASC"
    DESC = "DESC"

    def __str__(self):
        return str(self.value)


def is_hashable(value):
    try:
        hash(value)
    except TypeError:
        return False
    return True
