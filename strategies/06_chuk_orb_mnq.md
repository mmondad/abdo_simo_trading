# 06 · Chuk MNQ opening-range breakout

**Family:** `opening_range_breakout` · **Instrument:** `MNQ` · **Status:** `RESEARCHED_NOT_BACKTESTED` · **Research score:** 65/100

## Original source and evidence

- [Regime-Dependent Opening Range Breakout Returns in Nasdaq-100 Futures](https://justinchuktrading.com/papers/orb_paper.pdf) — Chuk, 2026, Author working paper.
- Source market: NQ original series; MNQ author rebuild; selected market: `MNQ`. Do not transfer this result to a CFD or micro contract unless it is the tested instrument.
- Historical sample: NQ study 2010–July 2026; executable MNQ rebuild 2020–July 2026. All intervals used in selection are in-sample.
- Author-reported result: Author-reported MNQ rebuild: 754 trades, $17.83 net per trade, 57% win; original NQ 2010–2019 interval was −$2.29/trade, 2020–2026 +$129.20/trade; no untouched OOS.
- Independent test: NOT VERIFIED. No backtest exists in this repository.

## Source rules

- Session/timezone: 09:30–14:00 America/New_York; flat at the 14:00 open
- Timeframe and data: M5 signal / M1 fill; Dated MNQ one-minute OHLCV, 5-minute aggregation, exchange calendar, FOMC calendar, contract roll metadata, and fill-cost schedule.
- Indicator: Frozen 30-minute range, 0.85% filter, first 5-minute close above high, next-bar entry, 1:1 bracket, 14:00 flat.
- BUY: After 10:00, first five-minute bar closing above the 09:30–10:00 high; enter long at next bar open. Skip if range/10:00 price >0.85%, FOMC decision days and exchange holidays.
- SELL/SHORT: NONE; long-only opening-range rule.
- Exit and mandatory same-session flat: Exit at stop, target, or at 13:55 bar close / 14:00 open, whichever comes first.
- Source stop loss: Opening-range low.
- Source take profit: Entry plus (entry minus opening-range low), 1:1 reward/risk.
- Source position sizing: One MNQ contract in 2020–July 2026 rebuild.
- Source cost treatment: Rebuild assumes $2 round trip, with entry/stop slippage treatment documented separately; independent live fill validation is incomplete.
- Maximum holding: up to ~4 h
- Maximum new entries per day in this selected specification: **1**; observed frequency: NOT REPORTED for this exact selected specification. The cap does not imply one trade every day.

## Proposed adaptations and gaps

- Proposed, not source-validated: Freeze exclusion list before test and use prior-day volume to select active contract; audit same-bar stop/target ordering; forward-test untouched dates.
- Key risks: Regime break around 2020, multiple testing, no independent OOS, stop fill slippage.
- Additional implementation note: No further source rule is asserted.
- Exact data and fill model must be acquired and checked before any independent backtest.

## Research score

Evidence 13/25; net after-cost evidence 13/20; rules 19/20; risk 7/15; data 9/10; regime robustness 4/10. This score ranks research priority, not expected profit.

Structured file: [06_chuk_orb_mnq.json](06_chuk_orb_mnq.json).
