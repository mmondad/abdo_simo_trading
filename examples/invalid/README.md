# Invalid fixture recipes

[`cases.json`](cases.json) defines eight invalid strategy examples as deterministic
JSON-pointer mutations of the canonical EMA crossover. The tests apply equivalent
mutations so each case isolates exactly one defect: unknown indicator, unknown
operator, invalid parameter type, missing exit, negative offset, invalid
timeframe, unsupported chart pattern, or unresolved indicator reference. This
avoids copying large documents whose unrelated fields could drift.
