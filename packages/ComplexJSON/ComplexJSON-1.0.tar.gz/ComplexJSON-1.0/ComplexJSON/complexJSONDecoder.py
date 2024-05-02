import importlib
from . import vardef
from .jsondef import json
from functools import lru_cache


class ComplexJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    @lru_cache
    def getmodule(self, name, package=None):
        return importlib.import_module(name, package)

    def object_hook(self, dct):
        if vardef.moduleword in dct and vardef.classword in dct:
            __class = vars(self.getmodule(dct[vardef.moduleword]))[dct[vardef.classword]]
            del dct[vardef.moduleword]
            del dct[vardef.classword]
            new_obj = object.__new__(__class)
            for k, v in dct.items():
                new_obj.__setattr__(k, v)
            return new_obj
        return dct
