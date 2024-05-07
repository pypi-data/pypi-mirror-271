import json
from types import NoneType
from typing import Any, Type, List, Iterable, Dict
from . import vardef


class ComplexJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, localClassWord: str = None, localModuleWord: str = None, localClassIdWord: str = None,
                 useTypeAssociation: bool = False,
                 classStorage: Dict[str, Type] | List[Type] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.localClassIdWord = localClassIdWord if isinstance(localClassIdWord,
                                                               str) and localClassIdWord else vardef.classidword
        self.localModuleWord = localModuleWord if isinstance(localModuleWord,
                                                             str) and localModuleWord else vardef.moduleword
        self.localClassWord = localClassWord if isinstance(localClassWord, str) and localClassWord else vardef.classword
        self.useTypeAssociation = bool(useTypeAssociation or classStorage)
        if isinstance(classStorage, dict):
            self.classStorage = classStorage
        elif isinstance(classStorage, list):
            self.classStorage = {classType.__name__: classType for classType in classStorage}
        else:
            self.classStorage = {}
        if self.useTypeAssociation:
            self.classTypeToClassTypeIdDict = {}

    def default(self, o: Any) -> Any:
        encoded_obj = {}
        encoded_obj.update(dict(o.__dict__))
        if not self.useTypeAssociation:
            if self.localModuleWord is not None:
                encoded_obj[self.localModuleWord] = o.__module__
            if self.localClassWord is not None:
                encoded_obj[self.localClassWord] = o.__class__.__name__
        else:
            if not self.localClassIdWord:
                raise RuntimeError("ClassIdWord can't be None when using type annotation mode")
            encoded_obj[self.localClassIdWord] = self.classTypeToClassTypeIdDict[o.__class__]
        return encoded_obj

    def encode(self, o: Any) -> str:
        if self.useTypeAssociation:
            json_obj = {"types": {".": {"useTA": True}, }, "obj": o}
            if not self.classStorage:
                self.classStorage = self.createClassStorageFromObj(o)
            for index, classType in enumerate(self.classStorage.values()):
                classTypeId = dec_to_chars(index)
                self.classTypeToClassTypeIdDict[classType] = classTypeId
                classTypeDict = {}
                if self.localModuleWord is not None:
                    classTypeDict[self.localModuleWord] = classType.__module__
                if self.localClassWord is None:
                    raise RuntimeError("Classword can't be None when using type annotation mode")
                classTypeDict[self.localClassWord] = classType.__name__
                json_obj["types"][classTypeId] = classTypeDict
            return super(ComplexJSONEncoder, self).encode(json_obj)
        else:
            return super(ComplexJSONEncoder, self).encode(o)

    def createClassStorageFromObj(self, obj: Any) -> Dict[str, Type]:
        type_set = set()

        def recursionTypeExtractor(obj: Any):
            if isinstance(obj, (str, int, float, bool, NoneType)):
                return
            if isinstance(obj, (tuple, list)):
                for sub_obj in obj.__iter__():
                    recursionTypeExtractor(sub_obj)
                return
            if isinstance(obj, dict):
                for sub_obj in obj.values():
                    recursionTypeExtractor(sub_obj)
                return
            type_set.add(obj.__class__)
            if hasattr(obj, "__dict__"):
                for sub_obj in obj.__dict__.values():
                    recursionTypeExtractor(sub_obj)

        recursionTypeExtractor(obj)
        return {classType.__name__: classType for classType in list(type_set)}


allowed_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+-/:;<=>?@[]^_`{|}~"


def dec_to_chars(i: int, base=len(allowed_chars)) -> str:
    if i < base:
        return allowed_chars[i]
    return dec_to_chars(i // base, base) + allowed_chars[i % base]
