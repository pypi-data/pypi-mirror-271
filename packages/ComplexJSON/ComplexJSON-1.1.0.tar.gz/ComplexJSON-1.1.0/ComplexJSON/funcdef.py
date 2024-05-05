from typing import Dict, Type, List
from . import ComplexJSONEncoder, ComplexJSONDecoder
from json import dumps as __dumps, loads as __loads, dump as __dump, load as __load


def dumps(obj, *args, skipkeys=False, ensure_ascii=True, check_circular=True,
          allow_nan=True, cls=ComplexJSONEncoder, indent=None, separators=None,
          default=None, sort_keys=False, localClassWord: str = None,
          localModuleWord: str = None, **kwargs):
    if localClassWord or localModuleWord:
        encoder = ComplexJSONEncoder(localModuleWord=localModuleWord, localClassWord=localClassWord)
        default = encoder.default
    return __dumps(obj, *args, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                   allow_nan=allow_nan, cls=cls, indent=indent, separators=separators,
                   default=default, sort_keys=sort_keys, **kwargs)


def loads(s, *args, cls=ComplexJSONDecoder, object_hook=None, parse_float=None,
          parse_int=None, parse_constant=None, object_pairs_hook=None,
          classStorage: Dict[str, Type] | List[Type] | None = None, localClassWord: str = None,
          localModuleWord: str = None, **kwargs):
    if classStorage or localClassWord or localModuleWord:
        decoder = ComplexJSONDecoder(classStorage=classStorage, localClassWord=localClassWord,
                                     localModuleWord=localModuleWord)
        object_hook = decoder.object_hook
    return __loads(s, *args, cls=cls, object_hook=object_hook, parse_float=parse_float,
                   parse_int=parse_int, parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kwargs)


def dump(obj, fp, *args, skipkeys=False, ensure_ascii=True, check_circular=True,
         allow_nan=True, cls=ComplexJSONEncoder, indent=None, separators=None,
         default=None, sort_keys=False, localClassWord: str = None,
         localModuleWord: str = None, **kwargs):
    if localClassWord or localModuleWord:
        encoder = ComplexJSONEncoder(localModuleWord=localModuleWord, localClassWord=localClassWord)
        default = encoder.default
    return __dump(obj, fp, *args, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                  allow_nan=allow_nan, cls=cls, indent=indent, separators=separators,
                  default=default, sort_keys=sort_keys, **kwargs)


def load(fp, *args, cls=ComplexJSONDecoder, object_hook=None, parse_float=None,
         parse_int=None, parse_constant=None, object_pairs_hook=None,
         classStorage: Dict[str, Type] | List[Type] | None = None, localClassWord: str = None,
         localModuleWord: str = None, **kwargs):
    if classStorage or localClassWord or localModuleWord:
        decoder = ComplexJSONDecoder(classStorage=classStorage, localClassWord=localClassWord,
                                     localModuleWord=localModuleWord)
        object_hook = decoder.object_hook
    return __load(fp, *args, cls=cls, object_hook=object_hook, parse_float=parse_float,
                  parse_int=parse_int, parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kwargs)
