# 07 · Baltussen ROD YM

**Family:** `baltussen_last_half_hour` · **Instrument:** `YM` · **Status:** `RESEARCHED_NOT_BACKTESTED` · **Research score:** 63/100

## Original source and evidence

- [Hedging demand and market intraday momentum](https://academicweb.nd.edu/~zda/intramom.pdf) — Baltussen; Da; Lammers; Martens, 2021, Journal of Financial Economics.
- Source market: ES, NQ, YM directly represented; portfolio of 60+ futures; selected market: `YM`. Do not transfer this result to a CFD or micro contract unless it is the tested instrument.
- Historical sample: YM history in paper 1997-10-08–2020-05-01, with early standard contract extension.
- Author-reported result: Equity-futures 1/N portfolio: gross annual return 6.86%, Sharpe 1.73; YM individual ROD predictive OOS R² 2.18%, not a YM trading P&L.
- Independent test: NOT VERIFIED. No backtest exists in this repository.

## Source rules

- Session/timezone: 09:30–16:00 America/New_York research window
- Timeframe and data: M30; Minute or quote data for the exact dated CME/CBOT contract, prior 16:00 research-window close, current 15:30 quote, and exit quote.
- Indicator: Return r_ROD = price 30 minutes before the defined research close / prior research-window close − 1. Trade sign for the final half hour.
- BUY: At 15:30 of the paper session, enter long if r_ROD > 0.
- SELL/SHORT: At 15:30 of the paper session, enter short if r_ROD <= 0.
- Exit and mandatory same-session flat: Exit at 16:00 research-window close; operational order must finish before the close.
- Source stop loss: NOT SPECIFIED
- Source take profit: NOT SPECIFIED
- Source position sizing: Source uses equal-weighted 1/N portfolio; single-contract sizing is an untested implementation assumption.
- Source cost treatment: Gross portfolio results only; YM-specific net result NOT REPORTED.
- Maximum holding: 30 min
- Maximum new entries per day in this selected specification: **1**; observed frequency: NOT REPORTED for this exact selected specification. The cap does not imply one trade every day.

## Proposed adaptations and gaps

- Proposed, not source-validated: Use exact dated contract, a volume-based roll chosen using the prior day, one position maximum, finish execution before the defined close, and test a stop separately. No CFD or micro-futures transfer is established.
- Key risks: YM-specific execution costs unverified; source portfolio performance cannot be assigned to YM.
- Additional implementation note: No further source rule is asserted.
- Exact data and fill model must be acquired and checked before any independent backtest.

## Research score

Evidence 19/25; net after-cost evidence 4/20; rules 19/20; risk 6/15; data 8/10; regime robustness 7/10. This score ranks research priority, not expected profit.

Structured file: [07_baltussen_rod_ym.json](07_baltussen_rod_ym.json).
