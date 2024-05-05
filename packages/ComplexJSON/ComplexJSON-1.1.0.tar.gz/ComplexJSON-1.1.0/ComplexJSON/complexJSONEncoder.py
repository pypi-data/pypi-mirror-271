import json
from typing import Any
from . import vardef


class ComplexJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, localClassWord: str = None, localModuleWord: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.localModuleWord = localModuleWord if isinstance(localModuleWord,
                                                             str) and localModuleWord else vardef.moduleword
        self.localClassWord = localClassWord if isinstance(localClassWord, str) and localClassWord else vardef.classword

    def default(self, o: Any) -> Any:
        encoded_obj = {}
        encoded_obj.update(dict(o.__dict__))
        if self.localModuleWord is not None:
            encoded_obj[self.localModuleWord] = o.__module__
        if self.localClassWord is not None:
            encoded_obj[self.localClassWord] = o.__class__.__name__
        return encoded_obj
