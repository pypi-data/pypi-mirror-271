from .jsondef import json, original_json
from . import ComplexJSONEncoder, ComplexJSONDecoder

__dumps = vars(json).get("dumps", original_json.dumps)
__loads = vars(json).get("loads", original_json.loads)
__dump = vars(json).get("dump", original_json.dump)
__load = vars(json).get("load", original_json.load)


def dumps(obj, *args, skipkeys=False, ensure_ascii=True, check_circular=True,
          allow_nan=True, cls=ComplexJSONEncoder, indent=None, separators=None,
          default=None, sort_keys=False, **kwargs):
    return __dumps(obj, *args, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                   allow_nan=allow_nan, cls=cls, indent=indent, separators=separators,
                   default=default, sort_keys=sort_keys, **kwargs)


def loads(s, *args, cls=ComplexJSONDecoder, object_hook=None, parse_float=None,
          parse_int=None, parse_constant=None, object_pairs_hook=None, **kwargs):
    return __loads(s, *args, cls=cls, object_hook=object_hook, parse_float=parse_float,
                   parse_int=parse_int, parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kwargs)


def dump(obj, fp, *args, skipkeys=False, ensure_ascii=True, check_circular=True,
         allow_nan=True, cls=ComplexJSONEncoder, indent=None, separators=None,
         default=None, sort_keys=False, **kwargs):
    return __dump(obj, fp, *args, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                  allow_nan=allow_nan, cls=cls, indent=indent, separators=separators,
                  default=default, sort_keys=sort_keys, **kwargs)


def load(fp, *args, cls=ComplexJSONDecoder, object_hook=None, parse_float=None,
         parse_int=None, parse_constant=None, object_pairs_hook=None, **kwargs):
    return __load(fp, *args, cls=cls, object_hook=object_hook, parse_float=parse_float,
                  parse_int=parse_int, parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kwargs)
