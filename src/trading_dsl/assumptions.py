"""Deterministic controlled assumption application."""

from copy import deepcopy
from .defaults import load_defaults

ASSUMPTION_REGISTRY_VERSION = "0.1.0"


def _record(spec: dict, path: str, value, rule: str, reason: str, missing: str) -> None:
    spec.setdefault("assumptions", []).append({"target_path": path, "value": value, "rule_id": rule, "registry_version": ASSUMPTION_REGISTRY_VERSION, "reason": reason, "missing_information": missing})


def resolve_assumptions(strategy: dict) -> dict:
    """Return a normalized deep copy. Repeated application is idempotent."""
    result = deepcopy(strategy)
    defaults = load_defaults()
    base = result.get("market", {}).get("base_timeframe")
    existing = {a.get("target_path") for a in result.setdefault("assumptions", [])}
    for index, indicator in enumerate(result.get("indicators", [])):
        prefix = f"/indicators/{index}"
        if indicator.get("type") == "RSI" and "period" not in indicator.get("parameters", {}):
            path = prefix + "/parameters/period"
            indicator.setdefault("parameters", {})["period"] = defaults["assumptions"]["rsi_period"]
            if path not in existing: _record(result, path, indicator["parameters"]["period"], "INDICATOR.RSI.PERIOD", "Apply the conventional provisional RSI period.", "RSI period")
        if "source" not in indicator:
            path = prefix + "/source"; indicator["source"] = defaults["assumptions"]["indicator_source"]
            if path not in existing: _record(result, path, indicator["source"], "INDICATOR.DEFAULT_SOURCE", "Use completed candle close as the default input.", "indicator source")
        if "timeframe" not in indicator and base and defaults["assumptions"]["inherit_indicator_timeframe"]:
            path = prefix + "/timeframe"; indicator["timeframe"] = base
            if path not in existing: _record(result, path, base, "INDICATOR.INHERIT_TIMEFRAME", "Inherit the strategy base timeframe.", "indicator timeframe")
    risk = result.setdefault("risk", {})
    for key in ("max_simultaneous_positions", "pyramiding", "hedging"):
        if key not in risk: risk[key] = defaults["execution"][key]
    risk.setdefault("execution", {k: v for k, v in defaults["execution"].items() if k not in {"max_simultaneous_positions", "pyramiding", "hedging"}})
    return result
