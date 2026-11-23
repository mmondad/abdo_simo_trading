"""Structural, semantic, and DSL-capability validation."""

from datetime import datetime
from importlib.resources import files
import json
import re
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from .assumptions import ASSUMPTION_REGISTRY_VERSION
from .defaults import DEFAULTS_VERSION
from .models import Issue, Status, ValidationReport
from .registries import CHART_PATTERNS, INDICATORS, OPERATORS, PATTERNS, registry_versions

TIMEFRAME = re.compile(r"^[1-9][0-9]*(s|m|h|d|w)$")


def _schema(name: str) -> dict:
    return json.loads(files("trading_dsl").joinpath("schemas", name).read_text())


def _pointer(parts) -> str:
    return "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def _structural(instance: dict, schema_name: str) -> list[Issue]:
    validator = Draft202012Validator(_schema(schema_name), format_checker=FormatChecker())
    return [Issue("structural", "SCHEMA_VIOLATION", _pointer(e.absolute_path), e.message) for e in sorted(validator.iter_errors(instance), key=lambda x: list(x.absolute_path))]


def _source_ref(spec: dict, path: str) -> dict | None:
    for item in spec.get("metadata", {}).get("provenance", []):
        if path.startswith(item.get("path", "#never")):
            return item.get("source_reference")
    return None


def _expression(expr: Any, path: str, indicators: dict[str, dict], issues: list[Issue]) -> str:
    if not isinstance(expr, dict): return "unknown"
    if "constant" in expr: return "boolean" if isinstance(expr["constant"], bool) else "numeric"
    if "price_ref" in expr: return "numeric"
    if "indicator_ref" in expr:
        ref = expr["indicator_ref"]
        if ref not in indicators:
            issues.append(Issue("semantic", "UNRESOLVED_REFERENCE", path + "/indicator_ref", f"Indicator {ref!r} is not defined."))
        elif expr.get("output") and expr["output"] not in INDICATORS.get(indicators[ref].get("type"), {}).get("outputs", []):
            issues.append(Issue("semantic", "INVALID_OUTPUT", path + "/output", f"Output {expr['output']!r} is invalid for this indicator."))
        return "numeric"
    if "pattern" in expr: return "boolean"
    if "operator" not in expr: return "unknown"
    op_name = expr["operator"]
    operands = expr.get("operands", [])
    op = OPERATORS.get(op_name)
    if not op: return "unknown"
    count = len(operands)
    if count < op.min_args or (op.max_args is not None and count > op.max_args):
        expected = str(op.min_args) if op.min_args == op.max_args else f"{op.min_args}..{op.max_args or 'many'}"
        issues.append(Issue("semantic", "INVALID_ARITY", path + "/operands", f"Operator {op_name!r} expects {expected} operand(s), got {count}."))
    kinds = [_expression(value, f"{path}/operands/{i}", indicators, issues) for i, value in enumerate(operands)]
    if op.input_kind in {"numeric", "boolean"} and any(k not in {op.input_kind, "unknown"} for k in kinds):
        issues.append(Issue("semantic", "OPERAND_TYPE_MISMATCH", path, f"Operator {op_name!r} requires {op.input_kind} operands; got {kinds}."))
    if op.input_kind == "same" and len(set(k for k in kinds if k != "unknown")) > 1:
        issues.append(Issue("semantic", "OPERAND_TYPE_MISMATCH", path, f"Operator {op_name!r} requires operands of the same type."))
    if op_name in {"consecutive", "within_last_n"} and not isinstance(expr.get("periods"), int):
        issues.append(Issue("semantic", "MISSING_PERIODS", path + "/periods", f"Operator {op_name!r} requires a positive integer periods value."))
    if op_name == "div" and len(operands) == 2 and operands[1].get("constant") == 0:
        issues.append(Issue("semantic", "DIVISION_BY_ZERO", path + "/operands/1", "A constant zero divisor is impossible."))
    return op.result_kind


def _walk_expressions(value: Any, path: str = ""):
    if isinstance(value, dict):
        if any(k in value for k in ("operator", "indicator_ref", "price_ref", "constant", "pattern")):
            yield value, path
        for key, child in value.items():
            yield from _walk_expressions(child, f"{path}/{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value): yield from _walk_expressions(child, f"{path}/{i}")


def _semantic(spec: dict) -> list[Issue]:
    issues: list[Issue] = []
    base = spec.get("market", {}).get("base_timeframe")
    if base and not TIMEFRAME.fullmatch(base): issues.append(Issue("semantic", "INVALID_TIMEFRAME", "/market/base_timeframe", "Use a positive integer plus s, m, h, d, or w (for example 5m or 4h)."))
    by_id: dict[str, dict] = {}
    for i, ind in enumerate(spec.get("indicators", [])):
        path = f"/indicators/{i}"; ident = ind.get("id")
        if ident in by_id: issues.append(Issue("semantic", "DUPLICATE_INDICATOR_ID", path + "/id", f"Duplicate indicator id {ident!r}."))
        if ident: by_id[ident] = ind
        tf = ind.get("timeframe")
        if tf and not TIMEFRAME.fullmatch(tf): issues.append(Issue("semantic", "INVALID_TIMEFRAME", path + "/timeframe", f"Invalid timeframe {tf!r}."))
        meta = INDICATORS.get(ind.get("type"))
        if meta:
            params = ind.get("parameters", {})
            for name, (types, minimum, maximum) in meta["params"].items():
                if name not in params: issues.append(Issue("semantic", "MISSING_INDICATOR_PARAMETER", path + "/parameters/" + name, f"Required parameter {name!r} is missing.")); continue
                val = params[name]
                if isinstance(val, bool) or not isinstance(val, types): issues.append(Issue("semantic", "INVALID_PARAMETER_TYPE", path + "/parameters/" + name, f"Parameter {name!r} has an invalid type.")); continue
                if minimum is not None and val < minimum: issues.append(Issue("semantic", "INVALID_PARAMETER_VALUE", path + "/parameters/" + name, f"Parameter {name!r} must be at least {minimum}."))
            unknown = set(params) - set(meta["params"])
            for name in sorted(unknown): issues.append(Issue("semantic", "UNKNOWN_PARAMETER", path + "/parameters/" + name, f"Parameter {name!r} is not registered."))
            if ind.get("type") == "MACD" and all(k in params and isinstance(params[k], int) for k in ("fast_period", "slow_period")) and params["fast_period"] >= params["slow_period"]:
                issues.append(Issue("semantic", "INVALID_PARAMETER_COMBINATION", path + "/parameters", "MACD fast_period must be less than slow_period."))
            output = ind.get("output")
            if len(meta["outputs"]) > 1 and not output: issues.append(Issue("semantic", "MISSING_OUTPUT", path + "/output", "A multi-output indicator requires output selection."))
            elif output and output not in meta["outputs"]: issues.append(Issue("semantic", "INVALID_OUTPUT", path + "/output", f"Unknown output {output!r}."))
    for direction, rules in spec.get("signals", {}).items():
        if not any(k in rules for k in ("exit", "stop_loss", "take_profit")):
            issues.append(Issue("semantic", "MISSING_EXIT", f"/signals/{direction}", "Define a signal exit, stop-loss, or take-profit."))
        for key in ("entry", "exit"):
            if key in rules:
                kind = _expression(rules[key], f"/signals/{direction}/{key}", by_id, issues)
                if kind not in {"boolean", "unknown"}: issues.append(Issue("semantic", "SIGNAL_NOT_BOOLEAN", f"/signals/{direction}/{key}", "Entry and exit expressions must return boolean."))
        for key in ("stop_loss", "take_profit"):
            level = rules.get(key, {})
            if level.get("unit") == "atr_multiple" and level.get("indicator_id") not in by_id:
                issues.append(Issue("semantic", "UNRESOLVED_REFERENCE", f"/signals/{direction}/{key}/indicator_id", "ATR-multiple risk requires a defined indicator_id."))
    return issues


def _capability(spec: dict) -> list[Issue]:
    issues: list[Issue] = []
    for i, ind in enumerate(spec.get("indicators", [])):
        name = ind.get("type")
        if name not in INDICATORS: issues.append(Issue("capability", "UNKNOWN_INDICATOR", f"/indicators/{i}/type", f"Indicator {name!r} is not registered.", "UNSUPPORTED_FEATURE", name, _source_ref(spec, f"/indicators/{i}"), "Register its parameter and output contract."))
    for expr, path in _walk_expressions(spec.get("signals", {}), "/signals"):
        if "operator" in expr and expr["operator"] not in OPERATORS:
            name = expr["operator"]; issues.append(Issue("capability", "UNKNOWN_OPERATOR", path + "/operator", f"Operator {name!r} is not registered.", "UNSUPPORTED_FEATURE", name, _source_ref(spec, path), "Register the operator type, arity, and semantics."))
        if "pattern" in expr:
            name = expr["pattern"]
            if name.lower() in CHART_PATTERNS: code, cat, action = "UNSUPPORTED_CHART_PATTERN", "UNSUPPORTED_PATTERN", "Reserve for the V2 chart-pattern contract; do not approximate it."
            elif name not in PATTERNS: code, cat, action = "UNKNOWN_PATTERN", "UNSUPPORTED_PATTERN", "Define and register the candlestick pattern contract."
            elif not PATTERNS[name]["engine_supported"]: code, cat, action = "PATTERN_IMPLEMENTATION_MISSING", "UNSUPPORTED_PATTERN", "Implement this registered pattern in a future execution engine."
            else: continue
            issues.append(Issue("capability", code, path + "/pattern", f"Pattern {name!r} is not executable.", cat, name, _source_ref(spec, path), action))
    return issues


def validate_strategy(strategy: dict) -> ValidationReport:
    paper = strategy.get("metadata", {}).get("paper_id") if isinstance(strategy, dict) else None
    sid = strategy.get("strategy_id") if isinstance(strategy, dict) else None
    versions = registry_versions() | {"assumptions": ASSUMPTION_REGISTRY_VERSION, "defaults": DEFAULTS_VERSION, "schema": "0.1.0"}
    structural = _structural(strategy, "strategy-0.1.0.json")
    issues = structural or (_semantic(strategy) + _capability(strategy))
    if any(i.category == "UNSUPPORTED_PATTERN" for i in issues): status = Status.UNSUPPORTED_PATTERN
    elif any(i.layer == "capability" for i in issues): status = Status.UNSUPPORTED_FEATURE
    elif issues: status = Status.UNRESOLVED
    else: status = Status.VALIDATED  # EXECUTABLE is intentionally reserved for a future engine capability profile.
    return ValidationReport(paper, sid, status, issues, versions)


def validate_backtest_config(config: dict) -> ValidationReport:
    issues = _structural(config, "backtest-config-0.1.0.json")
    try:
        start = datetime.fromisoformat(config.get("date_range", {}).get("start", "")); end = datetime.fromisoformat(config.get("date_range", {}).get("end", ""))
        if start >= end: issues.append(Issue("semantic", "INVALID_DATE_RANGE", "/date_range", "start must be earlier than end."))
    except ValueError: pass
    return ValidationReport(None, None, Status.VALIDATED if not issues else Status.UNRESOLVED, issues, {"config": "0.1.0"})
