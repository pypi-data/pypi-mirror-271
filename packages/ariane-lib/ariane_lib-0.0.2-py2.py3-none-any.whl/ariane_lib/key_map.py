#!/usr/bin/env python

import datetime

from collections import UserDict
from collections import UserList

from ariane_lib.types import ProfileType
from ariane_lib.types import ShotType
from ariane_lib.types import UnitType
from ariane_lib.type_utils import maybe_convert_str_type


class OptionalArgList(UserList):
    pass


class KeyMapCls(UserDict):
    def fetch(self, data, key):
        if key in self.keys():
            possible_keys = self[key]
            try:
                for tentative_key in self[key]:
                    try:
                        return data[tentative_key]
                    except KeyError:
                        continue
                else:
                    raise KeyError(f"Unable to find any of {self[key]}")
            except KeyError:
                if isinstance(possible_keys, OptionalArgList):
                    return None
                raise
        else:
            raise ValueError(f"The key `{key}` does not exists inside `data`")


class KeyMapMeta(type):
    def __new__(cls, name, bases, attrs):

        try:
            _KEY_MAP = attrs["_KEY_MAP"]
        except KeyError as e:
            raise AttributeError(
                f"The class {name} does not define a `_KEY_MAP` "
                "class attribute"
            ) from e
    
        def fetcher(self, name):
            value = self._KEY_MAP.fetch(self.data, name)

            match name:
                
                case "color":
                    return value

                case "date":
                    year, month, day = [int(v) for v in value.split("-")]
                    return datetime.datetime(year=year, month=month, day=day)
            
                case "profiletype":
                    return ProfileType.from_str(value)

                case "type":
                    return ShotType.from_str(value)
                
                case "unit":
                    return UnitType.from_str(value)
                
                case _:
                    return maybe_convert_str_type(value)
        
        attrs["_fetch_property_value"] = fetcher

        # Definining all the properties
        for key in _KEY_MAP.keys():
            
            # nested function necessary to avoid 
            # reference leak on the closure variable: "name"
            def wrapper(name):
                @property
                def inner(self):
                    return self._fetch_property_value(name)
                return inner
            
            attrs[key] = wrapper(name=key)

        obj = super().__new__(cls, name, bases, attrs)

        return obj
