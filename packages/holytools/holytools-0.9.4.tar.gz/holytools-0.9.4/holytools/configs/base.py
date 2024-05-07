from __future__ import annotations

import ast
from abc import abstractmethod, ABC
from typing import TypeVar, Union, Optional
from holytools.logging import Loggable, LogLevel

DictType = TypeVar(name='DictType', bound=dict)
ConfigValue = Union[str, int, bool, float]

# ---------------------------------------------------------

class BaseConfigs(Loggable, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._map : DictType = self._retrieve_map()

    @abstractmethod
    def _retrieve_map(self) -> DictType:
        pass

    # ---------------------------------------------------------

    def get(self, key : str) -> ConfigValue:
        if len(key.split()) > 1:
            raise ValueError(f'Key must not contain whitespaces, got : \"{key}\"')

        try:
            flatten_dict = flatten(self._map)
            value = flatten_dict.get(key)
            if value is None:
                raise KeyError
        except:
            self.log(f'Could not find key {key} in settings: Please set it manually', level=LogLevel.WARNING)
            value = input()
            self.set(key=key, value=value)

        value = self.convert_string(value)
        return value


    def set(self, key : str, value : ConfigValue, section : Optional[str] = None):
        if key in self._map:
            raise ValueError(f'Key \"{key}\" already exists in settings')
        if not isinstance(value, ConfigValue):
            raise ValueError(f'Value must be of type {ConfigValue} got : \"{value}\"')
        if not section is None:
            self._map[section] = {}
        inner_dict = self._map if section is None else self._map[section]
        inner_dict[key] = value
        self.update_config_resouce(key=key, value=str(value), section=section)


    @abstractmethod
    def update_config_resouce(self, key : str, value : str, section : Optional[str] = None):
        pass


    @staticmethod
    def convert_string(value) -> ConfigValue:
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value


def flatten(obj : dict) -> dict:
    flat_dict = {}

    def add(key : str, value : object):
        if key in flat_dict:
            raise ValueError(f'Key {key} already exists in flattened dictionary')
        flat_dict[key] = value

    for k1, v1 in obj.items():
        if isinstance(v1, dict):
            flattened_subdict = flatten(v1)
            for k2, v2 in flattened_subdict.items():
                add(key=k2, value=v2)
        else:
            add(key=k1, value=v1)
    return flat_dict


if __name__ == '__main__':
    nested_dict = {
        'key1': 'value1',
        'key2': {
            'key3': 'value2',
            'key4': {
                'key5': 'value3'
            }
        }
    }

    flattend = flatten(nested_dict)
    print(flattend)