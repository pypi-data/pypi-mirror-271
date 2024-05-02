import importlib, os

json = importlib.import_module(os.environ.get("COMPLEX_JSON_MODULE_NAME", "json"))
original_json = importlib.import_module("json")

json_vars = vars(json)
if "JSONDecoder" not in json_vars or "JSONEncoder" not in json_vars:
    json = original_json
