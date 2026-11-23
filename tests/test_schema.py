import json
from importlib.resources import files
from jsonschema import Draft202012Validator

def test_schemas_are_valid_draft_2020_12():
    for name in ("strategy-0.1.0.json", "backtest-config-0.1.0.json"):
        Draft202012Validator.check_schema(json.loads(files("trading_dsl").joinpath("schemas", name).read_text()))
