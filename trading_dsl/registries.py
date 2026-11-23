"""Versioned metadata registries; no calculations are implemented here."""

from dataclasses import dataclass
from typing import Any

INDICATOR_REGISTRY_VERSION = "0.1.0"
OPERATOR_REGISTRY_VERSION = "0.1.0"
PATTERN_REGISTRY_VERSION = "0.1.0"


@dataclass(frozen=True)
class Operator:
    min_args: int
    max_args: int | None
    input_kind: str
    result_kind: str
    engine_supported: bool = False


OPERATORS = {
    "gt": Operator(2, 2, "numeric", "boolean"), "gte": Operator(2, 2, "numeric", "boolean"),
    "lt": Operator(2, 2, "numeric", "boolean"), "lte": Operator(2, 2, "numeric", "boolean"),
    "eq": Operator(2, 2, "same", "boolean"),
    "all": Operator(2, None, "boolean", "boolean"), "any": Operator(2, None, "boolean", "boolean"),
    "not": Operator(1, 1, "boolean", "boolean"),
    "add": Operator(2, None, "numeric", "numeric"), "sub": Operator(2, 2, "numeric", "numeric"),
    "mul": Operator(2, None, "numeric", "numeric"), "div": Operator(2, 2, "numeric", "numeric"),
    "abs": Operator(1, 1, "numeric", "numeric"),
    "crosses_above": Operator(2, 2, "numeric", "boolean"),
    "crosses_below": Operator(2, 2, "numeric", "boolean"),
    "consecutive": Operator(1, 1, "boolean", "boolean"),
    "within_last_n": Operator(1, 1, "boolean", "boolean"),
}

INDICATORS: dict[str, dict[str, Any]] = {
    "SMA": {"params": {"period": (int, 1, None)}, "outputs": ["value"]},
    "EMA": {"params": {"period": (int, 1, None)}, "outputs": ["value"]},
    "RSI": {"params": {"period": (int, 1, None)}, "outputs": ["value"]},
    "ATR": {"params": {"period": (int, 1, None)}, "outputs": ["value"]},
    "MACD": {"params": {"fast_period": (int, 1, None), "slow_period": (int, 2, None), "signal_period": (int, 1, None)}, "outputs": ["macd", "signal", "histogram"]},
    "BOLLINGER_BANDS": {"params": {"period": (int, 1, None), "stddev": ((int, float), 0, None)}, "outputs": ["upper", "middle", "lower"]},
}

# A pattern can be valid DSL vocabulary while unavailable to a future engine.
PATTERNS = {
    "bullish_engulfing": {"direction": "bullish", "engine_supported": False},
    "bearish_engulfing": {"direction": "bearish", "engine_supported": False},
    "doji": {"direction": "neutral", "engine_supported": False},
}

CHART_PATTERNS = {"head_and_shoulders", "fair_value_gap", "fvg"}


def registry_versions() -> dict[str, str]:
    return {"indicators": INDICATOR_REGISTRY_VERSION, "operators": OPERATOR_REGISTRY_VERSION, "patterns": PATTERN_REGISTRY_VERSION}
