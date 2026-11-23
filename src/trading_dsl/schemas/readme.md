# Trading DSL JSON Schemas

This directory contains the versioned JSON Schemas used to validate a trading
strategy and the environment in which that strategy is backtested. Both files
use [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12).

The schemas serve different purposes:

| File | Purpose | Version field |
| :-- | :-- | :-- |
| [`strategy-0.1.0.json`](./strategy-0.1.0.json) | Describes a strategy's indicators, entry/exit expressions, risk rules, provenance, and assumptions. | `schema_version: "0.1.0"` |
| [`backtest-config-0.1.0.json`](./backtest-config-0.1.0.json) | Describes one backtest environment: instrument, period, data source, capital, costs, execution, and limits. | `config_version: "0.1.0"` |

Keeping these documents separate allows one strategy to be tested against many
instruments, periods, cost scenarios, and execution assumptions without changing
the strategy itself.

## `strategy-0.1.0.json`

Use this schema for the normalized, executable representation of a trading
strategy extracted from a paper or created as an explicit variant.

### Top-level fields

All top-level fields are required, and unknown top-level properties are rejected.

| Field | Type | Meaning and constraints |
| :-- | :-- | :-- |
| `schema_version` | string constant | Must be exactly `0.1.0`. |
| `strategy_id` | string | Stable strategy identifier. Length is 1–128 characters; the first character must be alphanumeric, and the rest may also contain `_`, `.`, or `-`. |
| `variant_id` | string | Identifies the exact interpretation or assumption set. It follows the same format as `strategy_id`. |
| `metadata` | object | Human-readable identity and traceability information. Extra metadata fields are allowed. |
| `market` | object | Defines the base timeframe and optional market hints. |
| `indicators` | array | Indicator declarations referenced by signal expressions or risk levels. An empty array is valid. |
| `signals` | object | Contains at least one of `long` or `short`. |
| `risk` | object | Portfolio and execution-related risk settings. The object may be empty. |
| `assumptions` | array | Records values introduced because the source material was incomplete. An empty array means no assumptions were recorded. |

### Metadata and provenance

`metadata` requires:

| Field | Type | Description |
| :-- | :-- | :-- |
| `name` | non-empty string | Display name for the strategy. |
| `paper_id` | non-empty string | Identifier of the source paper or research document. |
| `provenance` | array | Per-field traceability records. The array may be empty. |
| `paper_reference` | object | Optional bibliographic or source-location data. Its internal shape is currently open. |

Each provenance item requires a JSON-like `path` and a `category`:

| Category | Meaning |
| :-- | :-- |
| `EXPLICIT` | Directly stated by the source. |
| `DERIVED` | Logically or mathematically derived from the source. |
| `ASSUMED` | Filled using a documented default or interpretation. |
| `MODIFIED` | Intentionally differs from the source. |
| `UNRESOLVED` | The source does not provide enough information to settle the value. |

Optional `source_reference` may hold page, section, quotation, or document
coordinates, while `note` can explain the classification. Unknown fields inside
a provenance item are rejected.

### Market

`market.base_timeframe` is required. `asset_class` and `instrument_hint` are
optional strings. The schema does not currently restrict timeframe notation, so
the producing and consuming applications must agree on a convention such as
`1m`, `15m`, `1h`, or `1d`.

### Indicators

Every indicator declaration requires:

| Field | Type | Description |
| :-- | :-- | :-- |
| `id` | non-empty string | Unique reference used by expressions. Uniqueness is a semantic rule and is not enforced by this schema. |
| `type` | non-empty string | Registered indicator name, for example `ema`, `rsi`, or `atr`. |
| `parameters` | object | Indicator-specific parameters, such as `{ "period": 14 }`. |
| `source` | enum, optional | One of `open`, `high`, `low`, `close`, or `volume`. |
| `timeframe` | string, optional | Overrides the market's base timeframe. |
| `output` | string, optional | Selects an output when an indicator exposes more than one series. |

Unknown fields in an indicator are rejected. Whether an indicator type,
parameter, output, or timeframe is supported must be checked by the DSL's
semantic validator or feature registry.

### Signals and directions

`signals` must contain `long`, `short`, or both. Each direction requires `entry`
and may also define `exit`, `stop_loss`, and `take_profit`.

An entry or exit is a recursive expression made from exactly one of these node
shapes:

| Expression node | Required field(s) | Optional field(s) | Purpose |
| :-- | :-- | :-- | :-- |
| Operation | `operator`, `operands` | `periods` (integer ≥ 1) | Combines nested expressions using a registered comparison, Boolean, or temporal operator. |
| Indicator reference | `indicator_ref` | `output`, `offset` (integer ≥ 0) | Reads an indicator declared in `indicators`. |
| Price reference | `price_ref` | `offset` (integer ≥ 0), `timeframe` | Reads `open`, `high`, `low`, `close`, or `volume`. |
| Constant | `constant` | — | Supplies a number or Boolean literal. |
| Pattern | `pattern` | `offset` (integer ≥ 0), `timeframe` | Invokes a registered candle or market pattern. |

The schema intentionally permits any string for `operator` and `pattern`.
Applications must reject names that are not present in their feature registry.
They must also verify that every `indicator_ref` resolves, operand types are
compatible, and no expression introduces look-ahead.

Stops and targets use a risk-level object:

| Field | Type | Description |
| :-- | :-- | :-- |
| `value` | number > 0 | Distance or multiplier. |
| `unit` | enum | `pips`, `points`, `percentage`, `absolute_price`, or `atr_multiple`. |
| `indicator_id` | string, optional | Indicator used to calculate a dynamic level, normally required semantically for `atr_multiple`. |

### Risk

The optional members of the required `risk` object are:

| Field | Type | Constraint / purpose |
| :-- | :-- | :-- |
| `position_sizing` | object | Strategy-level sizing rule; its internal shape is not yet constrained. |
| `max_simultaneous_positions` | integer | Must be at least 1. |
| `pyramiding` | boolean | Whether positions may be added in the same direction. |
| `hedging` | boolean | Whether opposing positions may coexist. |
| `execution` | object | Strategy-specific execution instructions; its internal shape is not yet constrained. |

### Assumptions

Each assumption documents a value inserted into the strategy and requires all of
the following fields:

| Field | Description |
| :-- | :-- |
| `target_path` | Location in the strategy affected by the assumption. |
| `value` | Assumed value; any valid JSON value is accepted. |
| `rule_id` | Identifier of the defaulting or inference rule used. |
| `registry_version` | Version of the assumption-rule registry. |
| `reason` | Why this value was selected. |
| `missing_information` | What the original source failed to specify. |

### Minimal strategy example

```json
{
  "schema_version": "0.1.0",
  "strategy_id": "ema-crossover",
  "variant_id": "baseline",
  "metadata": {
    "name": "EMA crossover",
    "paper_id": "synthetic-example",
    "provenance": [
      {
        "path": "/signals/long/entry",
        "category": "EXPLICIT",
        "note": "Example rule, not an investment recommendation."
      }
    ]
  },
  "market": {
    "base_timeframe": "1h",
    "asset_class": "fx"
  },
  "indicators": [
    {"id": "ema_fast", "type": "ema", "parameters": {"period": 20}, "source": "close"},
    {"id": "ema_slow", "type": "ema", "parameters": {"period": 50}, "source": "close"}
  ],
  "signals": {
    "long": {
      "entry": {
        "operator": "crosses_above",
        "operands": [
          {"indicator_ref": "ema_fast"},
          {"indicator_ref": "ema_slow"}
        ]
      },
      "exit": {
        "operator": "crosses_below",
        "operands": [
          {"indicator_ref": "ema_fast"},
          {"indicator_ref": "ema_slow"}
        ]
      }
    }
  },
  "risk": {
    "max_simultaneous_positions": 1,
    "pyramiding": false,
    "hedging": false
  },
  "assumptions": []
}
```

## `backtest-config-0.1.0.json`

Use this schema to describe the external conditions for a reproducible backtest.
All top-level fields are required, and unknown top-level fields are rejected.

| Field | Type | Meaning and constraints |
| :-- | :-- | :-- |
| `config_version` | string constant | Must be exactly `0.1.0`. |
| `instrument` | non-empty string | Instrument or contract identifier understood by the data and execution adapters. |
| `date_range` | object | Requires `start` and `end`, both JSON Schema `date-time` strings. Chronological ordering is a semantic check. |
| `data` | object | Requires string fields `source` and `timezone`. |
| `account` | object | Requires positive `initial_capital`, a string `currency`, and a `position_sizing` object. |
| `costs` | object | Optional non-negative numeric `spread`, `commission`, and `slippage`; `other` is an array of unconstrained cost objects. The object may be empty. |
| `execution` | object | Fill timing, order behavior, and intrabar policy. Its shape is currently open. |
| `instrument_spec` | object | Tick size, pip value, contract size, margin, rounding, and related properties. Its shape is currently open. |
| `position_limits` | object | Exposure and position-count constraints. Its shape is currently open. |
| `data_quality` | object | Gap, duplicate, timezone, and anomaly policies. Its shape is currently open. |

`date_range`, `data`, `account`, and `costs` reject unknown properties. The last
four open objects currently accept any properties because their detailed
contracts have not yet been formalized.

### Minimal backtest configuration example

```json
{
  "config_version": "0.1.0",
  "instrument": "EURUSD",
  "date_range": {
    "start": "2020-01-01T00:00:00Z",
    "end": "2024-12-31T23:59:59Z"
  },
  "data": {
    "source": "dukascopy",
    "timezone": "UTC"
  },
  "account": {
    "initial_capital": 100000,
    "currency": "USD",
    "position_sizing": {"type": "fixed_fraction", "fraction": 0.01}
  },
  "costs": {
    "spread": 0.8,
    "commission": 0,
    "slippage": 0.1,
    "other": []
  },
  "execution": {"signal_fill": "next_bar_open"},
  "instrument_spec": {"price_precision": 5, "pip_size": 0.0001},
  "position_limits": {"max_open_positions": 1},
  "data_quality": {"on_gap": "reject"}
}
```

The nested keys in `position_sizing`, `execution`, `instrument_spec`,
`position_limits`, and `data_quality` are illustrative: version 0.1.0 does not
validate their internal vocabulary yet.

## Validation

With Python and the optional `jsonschema` package installed, validate a document
against a schema as follows:

```bash
python -m jsonschema \
  --instance path/to/strategy.json \
  src/trading_dsl/schemas/strategy-0.1.0.json

python -m jsonschema \
  --instance path/to/backtest-config.json \
  src/trading_dsl/schemas/backtest-config-0.1.0.json
```

A schema-valid document is not necessarily executable. A second semantic
validation stage should check at least:

- indicator ID uniqueness and reference resolution;
- supported indicators, operators, patterns, units, timeframes, and parameters;
- expression operand types and operator arity;
- chronological date ranges and available market data;
- timezone names, instrument specifications, and unit consistency;
- assumptions and unresolved essential logic;
- look-ahead, fill timing, cost, and position-limit rules.

Format validation should enable a JSON Schema validator's format checker so that
`date-time` is enforced rather than treated only as annotation.

## Versioning and compatibility

The version is present in both the filename and the document body. When changing
a schema:

1. Create a new versioned file; do not silently alter the meaning of an existing
   published version.
2. Update its `$id`, title where applicable, and version constant together.
3. Keep producers and consumers explicit about which schema version they use.
4. Add migration logic when a new version is not backward compatible.
5. Add valid and invalid fixture tests for every new constraint.

The current `$id` values use `example.org` as a placeholder namespace. Replace
them with a stable project-controlled URI before treating the schemas as
published artifacts.
