import json
import importlib
from typing import Dict, Type, List

from . import vardef
from functools import lru_cache


class ComplexJSONDecoder(json.JSONDecoder):
    def __init__(self,
                 *args,
                 classStorage: Dict[str, Type] | List[Type] | None = None,
                 localClassWord: str = None,
                 localModuleWord: str = None,
                 **kwargs):
        kwargs.setdefault("object_hook", self.object_hook)
        json.JSONDecoder.__init__(self, *args, **kwargs)
        self.classStorage = {}
        if isinstance(classStorage, dict):
            self.classStorage = classStorage
        elif isinstance(classStorage, list):
            self.classStorage = {classType.__name__: classType for classType in classStorage}
        self.localModuleWord = localModuleWord if isinstance(localModuleWord,
                                                             str) and localModuleWord else vardef.moduleword
        self.localClassWord = localClassWord if isinstance(localClassWord, str) and localClassWord else vardef.classword

    @lru_cache
    def getmodule(self, name, package=None):
        return importlib.import_module(name, package)

    def object_hook(self, dct):
        if self.localClassWord in dct:
            if self.localModuleWord in dct:
                __class = vars(self.getmodule(dct[self.localModuleWord])).get(dct[self.localClassWord], None)
                del dct[self.localModuleWord]
                if __class is None:
                    raise RuntimeError(
                        f'Can\'t find class "{dct[self.localClassWord]}" in module "{dct[self.localModuleWord]}"')
            else:
                __class = self.classStorage.get(dct[self.localClassWord], None)
                if __class is None:
                    raise RuntimeError(f'Can\'t find class "{dct[self.localClassWord]}" in classStorage')
            del dct[self.localClassWord]
            new_obj = object.__new__(__class)
            for k, v in dct.items():
                new_obj.__setattr__(k, v)
            return new_obj
        return dct
