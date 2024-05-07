from __future__ import annotations

import orjson
import dataclasses
from datetime import datetime, date, time
from typing import get_type_hints, get_origin, get_args, Union
from types import NoneType
from enum import Enum
import json

from .serializable import Serializable
# -------------------------------------------


class JsonDataclass(Serializable):
    def __init__(self):
        if not dataclasses.is_dataclass(self):
            raise TypeError(f'{self.__class__} must be a dataclass to be Jsonifyable')

    @classmethod
    def from_str(cls, json_str: str):
        json_str_dict = orjson.loads(json_str)
        return from_json(cls=cls, json_dict=json_str_dict)

    def to_str(self) -> str:
        json_dict = self.to_json()
        return orjson.dumps(json_dict).decode("utf-8")

    def to_json(self) -> dict:
        return {attr: get_json_entry(obj=value) for attr, value in self.__dict__.items()}

    @classmethod
    def from_json(cls, json_dict : dict) -> JsonDataclass:
        return from_json(cls=cls, json_dict=json_dict)


def get_json_entry(obj):
    if isinstance(obj, JsonDataclass):
        entry = obj.to_json()
    elif isinstance(obj, Enum):
        entry = obj.value
    elif hasattr(obj, '__dict__'):
        entry = {attr: value for attr, value in obj.__dict__.items() if not callable(value)}
    elif isinstance(obj, dict):
        entry = json.dumps(obj)
    else:
        entry = obj
    return entry


def from_json(cls : type, json_dict: dict):
    if not dataclasses.is_dataclass(cls):
        raise TypeError(f'{cls} is not a dataclass. from_json can only be used with dataclasses')
    type_hints = get_type_hints(cls)
    init_dict = {}
    for key, value in json_dict.items():
        if value is None:
            init_dict[key] = value
            continue

        dtype = type_hints.get(key)
        core_dtype = get_core_type(dtype=dtype)
        if core_dtype.__name__ in elementary_type_names:
            init_dict[key] = make_elementary(cls=core_dtype,value=value)
        elif issubclass(core_dtype, Enum):
            init_dict[key] = core_dtype(value)
        elif core_dtype == dict:
            init_dict[key] = make_dict(dtype=dtype, value=value)
        elif dataclasses.is_dataclass(obj=core_dtype):
            init_dict[key] = from_json(cls=core_dtype, json_dict=value)
        else:
            raise TypeError(f'Unsupported type {core_dtype}')

    return cls(**init_dict)


def make_dict(dtype : type, value : str):
    key_type, value_type = get_dict_item_types(dtype=dtype)
    item_types = {key_type.__name__, value_type.__name__}
    supported_types = set(elementary_type_names)
    if any(item_type not in supported_types for item_type in item_types):
        raise TypeError(f'Unsupported type in dict {item_types}')

    str_dict = json.loads(value)
    dict_value = {make_elementary(cls=key_type, value=k): make_elementary(cls=value_type, value=v) for k, v in
                  str_dict.items()}
    return dict_value


def make_elementary(cls, value : str):
    if cls in conversion_map:
        return conversion_map[cls](value)
    elif cls.__name__ in typecast_classes:
        return cls(value)
    else:
        raise TypeError(f'Unsupported type {cls}')


def get_dict_item_types(dtype : type) -> (type, type):
    if not get_core_type(dtype) == dict:
        raise TypeError(f'{dtype} is not a dict')
    args = get_args(dtype)
    if not len(args) == 2:
        raise ValueError(f'{dtype} does not have key and value annotations')
    key_type, value_type = args
    return key_type, value_type


# noinspection DuplicatedCode
def get_core_type(dtype : type) -> type:
    origin = get_origin(dtype)
    if origin is Union:
        types = get_args(dtype)
        not_none_types = [t for t in types if not t is NoneType]
        if len(not_none_types) == 1:
            core_type = not_none_types[0]
        else:
            raise ValueError(f'Union dtype {dtype} has more than one core dtype')
    elif origin:
        core_type = origin
    else:
        core_type = dtype
    return core_type


typecast_classes = ['Decimal', 'UUID', 'Path', 'str', 'int', 'float', 'bool']
conversion_map = {
    datetime: datetime.fromisoformat,
    date: date.fromisoformat,
    time: time.fromisoformat,
}
elementary_type_names : list[str] = typecast_classes + [cls.__name__ for cls in conversion_map.keys()]
