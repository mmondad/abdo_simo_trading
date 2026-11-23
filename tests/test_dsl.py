import json
from copy import deepcopy
from pathlib import Path

from trading_dsl.assumptions import resolve_assumptions
from trading_dsl.models import Status
from trading_dsl.registries import INDICATORS, OPERATORS
from trading_dsl.validation import validate_backtest_config, validate_strategy

ROOT = Path(__file__).parents[1]


def example(name="ema_crossover.json"):
    return json.loads((ROOT / "examples/valid" / name).read_text())


def test_all_valid_examples_are_structurally_and_semantically_valid():
    for path in (ROOT / "examples/valid").glob("*.json"):
        report = validate_strategy(json.loads(path.read_text()))
        if path.name == "candlestick.json":
            assert report.status == Status.UNSUPPORTED_PATTERN
        else:
            assert report.valid, (path, report.to_dict())
            assert report.status == Status.VALIDATED


def test_unknown_indicator_and_operator_classification():
    spec = example(); spec["indicators"][0]["type"] = "MAGIC"
    assert validate_strategy(spec).status == Status.UNSUPPORTED_FEATURE
    spec = example(); spec["signals"]["long"]["entry"]["operator"] = "approximately"
    report = validate_strategy(spec)
    assert report.status == Status.UNSUPPORTED_FEATURE
    assert report.grouped_capabilities()[0]["missing_feature"] == "approximately"


def test_semantic_parameter_reference_arity_and_types():
    spec = example(); spec["indicators"][0]["parameters"]["period"] = "20"
    assert "INVALID_PARAMETER_TYPE" in {i.code for i in validate_strategy(spec).issues}
    spec = example(); spec["signals"]["long"]["entry"]["operands"] = [{"indicator_ref": "missing"}]
    codes = {i.code for i in validate_strategy(spec).issues}
    assert {"INVALID_ARITY", "UNRESOLVED_REFERENCE"} <= codes
    spec = example(); spec["signals"]["long"]["entry"] = {"operator": "all", "operands": [{"constant": True}, {"constant": 1}]}
    assert "OPERAND_TYPE_MISMATCH" in {i.code for i in validate_strategy(spec).issues}


def test_negative_offset_and_invalid_timeframe_are_rejected():
    spec = example(); spec["signals"]["long"]["entry"]["operands"][0]["offset"] = -1
    assert any(i.layer == "structural" for i in validate_strategy(spec).issues)
    spec = example(); spec["market"]["base_timeframe"] = "hourly"
    assert "INVALID_TIMEFRAME" in {i.code for i in validate_strategy(spec).issues}


def test_exit_is_required_but_sl_or_tp_is_sufficient():
    spec = example("long_only.json"); del spec["signals"]["long"]["exit"]
    assert "MISSING_EXIT" in {i.code for i in validate_strategy(spec).issues}
    spec["signals"]["long"]["stop_loss"] = {"value": 1, "unit": "percentage"}
    assert validate_strategy(spec).valid


def test_chart_pattern_is_never_approximated():
    spec = example("candlestick.json"); spec["signals"]["long"]["entry"]["pattern"] = "head_and_shoulders"
    report = validate_strategy(spec)
    assert report.status == Status.UNSUPPORTED_PATTERN
    assert report.issues[0].code == "UNSUPPORTED_CHART_PATTERN"


def test_assumption_resolution_is_deterministic_idempotent_and_non_mutating():
    spec = example("rsi_threshold.json"); indicator = spec["indicators"][0]
    del indicator["parameters"]["period"]; del indicator["source"]; del indicator["timeframe"]
    original = deepcopy(spec); first = resolve_assumptions(spec); second = resolve_assumptions(first)
    assert spec == original
    assert first == second
    assert first["indicators"][0] == {"id": "rsi", "type": "RSI", "parameters": {"period": 14}, "source": "close", "timeframe": "15m"}
    assert len(first["assumptions"]) == 3
    assert validate_strategy(first).valid


def test_registry_lookup_and_identity_versioning():
    assert {"EMA", "RSI", "MACD"} <= INDICATORS.keys()
    assert {"all", "crosses_above", "within_last_n"} <= OPERATORS.keys()
    spec = example(); spec["schema_version"] = "0.2.0"
    assert any(i.code == "SCHEMA_VIOLATION" for i in validate_strategy(spec).issues)
    spec = example(); spec["strategy_id"] = "bad id"
    assert not validate_strategy(spec).valid


def test_backtest_contract_and_date_semantics():
    config = {"config_version": "0.1.0", "instrument": "EURUSD", "date_range": {"start": "2024-01-02T00:00:00+00:00", "end": "2024-01-01T00:00:00+00:00"}, "data": {"source": "dukascopy", "timezone": "UTC"}, "account": {"initial_capital": 10000, "currency": "USD", "position_sizing": {}}, "costs": {"spread": 0, "commission": 0, "slippage": 0}, "execution": {}, "instrument_spec": {}, "position_limits": {}, "data_quality": {}}
    assert "INVALID_DATE_RANGE" in {i.code for i in validate_backtest_config(config).issues}
