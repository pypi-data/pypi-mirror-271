from typing import Any
from . import vardef
from .jsondef import json

class ComplexJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        encoded_obj = {}
        encoded_obj.update(dict(o.__dict__))
        encoded_obj[vardef.moduleword] = o.__module__
        encoded_obj[vardef.classword] = o.__class__.__name__
        return encoded_obj
