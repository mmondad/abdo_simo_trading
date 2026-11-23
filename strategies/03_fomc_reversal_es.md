# 03 · FOMC pre-announcement reversal ES

**Family:** `fomc_event_reversal` · **Instrument:** `ES` · **Status:** `RESEARCHED_NOT_BACKTESTED` · **Research score:** 67/100

## Original source and evidence

- [The FOMC Announcement Reversal](https://repositorio-api.insper.edu.br/server/api/core/bitstreams/fb55a5bb-06c8-4ed4-aa81-054742c3b42d/content) — Baglioni; Ribeiro, 2022, SSRN working paper; accessible chapter in 2023 Insper thesis.
- Source market: ES futures; selected market: `ES`. Do not transfer this result to a CFD or micro contract unless it is the tested instrument.
- Historical sample: September 1997–January 2020, 180 scheduled FOMC events
- Author-reported result: Table 1.2: 180 events, mean 17.86 basis points per event after bid/ask, annualized event Sharpe 1.02; Table 1.8 109 early events mean 14.30 bp, Table 1.9 71 later events mean 23.34 bp. These are author subsamples, not untouched OOS.
- Independent test: No independent or post-2020 test; source-period splits do not count as independent OOS.. No backtest exists in this repository.

## Source rules

- Session/timezone: Scheduled FOMC day, usual 13:50–15:50 paper clock; eight historical 12:30 releases use 12:15 entry and 14:15 exit
- Timeframe and data: M1; Exact-dated ES M1 bid/ask or tick quotes, scheduled FOMC timestamps, historical release-time exceptions, exchange/DST calendar and contract roll.
- Indicator: Prior 24-hour ES return at the paper pre-release entry minute: mid_t / mid_at_same_clock_previous_day − 1.
- BUY: On scheduled FOMC day, buy ES at ask if prior 24-hour return is negative.
- SELL/SHORT: On scheduled FOMC day, sell ES at bid if prior 24-hour return is positive.
- Exit and mandatory same-session flat: Close two hours later using opposing bid/ask, before the cash close; zero-return treatment not stated.
- Source stop loss: Not specified by paper.
- Source take profit: No target; fixed two-hour exit.
- Source position sizing: Notional/contract sizing and max loss are not specified.
- Source cost treatment: Original uses ask for buys and bid for sells at minute-close observations; explicitly ignores broker fees and market impact.
- Maximum holding: 2 h
- Maximum new entries per day in this selected specification: **1**; observed frequency: FOMC event count, not daily average. The cap does not imply one trade every day.

## Proposed adaptations and gaps

- Proposed, not source-validated: Resolve source EST/ET wording against each historic FOMC timestamp; skip zero-return events by a predeclared rule; cap one event position; fixed contract sizing and news slippage stress are new assumptions.
- Key risks: Announcement jumps, rapid quote changes, order rejection/impact, no protective stop; high event concentration.
- Additional implementation note: Eight historical 12:30 releases use 12:15 entry and 14:15 exit; verify timestamps and source EST/ET convention before implementation. Zero-return rule is unresolved.
- Exact data and fill model must be acquired and checked before any independent backtest.

## Research score

Evidence 18/25; net after-cost evidence 11/20; rules 18/20; risk 5/15; data 9/10; regime robustness 6/10. This score ranks research priority, not expected profit.

Structured file: [03_fomc_reversal_es.json](03_fomc_reversal_es.json).
