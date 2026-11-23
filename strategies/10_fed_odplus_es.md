# 10 · Fed early-Globex ES fixed-window long

**Family:** `early_globex_clock` · **Instrument:** `ES` · **Status:** `RESEARCHED_NOT_BACKTESTED` · **Research score:** 56/100

## Original source and evidence

- [The Overnight Drift](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf) — Boyarchenko; Larsen; Whelan, 2022, New York Fed Staff Report 917 (revised 2022).
- Source market: ES futures; selected market: `ES`. Do not transfer this result to a CFD or micro contract unless it is the tested instrument.
- Historical sample: January 2004–December 2020
- Author-reported result: Table IX(b) simple OD+ annualized mean 1.91% and Sharpe 0.26 after bid/ask, 2004–2020. Shorter OD 02:00–03:00 has net Sharpe −0.54; BtD requires order-flow data and is a different conditional variant.
- Independent test: No independent current-market replication identified; positive net result is small and likely vulnerable to extra costs.. No backtest exists in this repository.

## Source rules

- Session/timezone: 01:30–03:30 America/New_York, within one Globex session
- Timeframe and data: M1; Dated ES bid/ask or tick/M1 quotes around 01:30 and 03:30 ET, Globex calendar, holiday/DST and roll metadata.
- Indicator: Fixed Eastern local clock; no price indicator for OD+.
- BUY: Buy one ES futures position at 01:30 Eastern time on eligible trading dates.
- SELL/SHORT: No short signal in simple OD+ rule.
- Exit and mandatory same-session flat: Sell/flatten at 03:30 Eastern time the same Globex session.
- Source stop loss: Not specified by paper.
- Source take profit: No target; fixed two-hour exit.
- Source position sizing: Source compares one-dollar investment; futures contract sizing and margin budget not specified.
- Source cost treatment: Table IX(b) uses best ask/bid quote spread; brokerage fees, impact and full retail fill uncertainty remain.
- Maximum holding: 2 h
- Maximum new entries per day in this selected specification: **1**; observed frequency: NOT REPORTED. The cap does not imply one trade every day.

## Proposed adaptations and gaps

- Proposed, not source-validated: Trade only if the dated contract has an uninterrupted 01:30–03:30 session; one position maximum; fixed contract size and any stop are new, untested rules.
- Key risks: Night-time liquidity and macro/European-open shocks; no stop; daylight-saving sensitivity; margin/roll and spread.
- Additional implementation note: This clock window is early morning but starts and ends within one Globex session; do not carry through maintenance break.
- Exact data and fill model must be acquired and checked before any independent backtest.

## Research score

Evidence 18/25; net after-cost evidence 5/20; rules 18/20; risk 4/15; data 8/10; regime robustness 3/10. This score ranks research priority, not expected profit.

Structured file: [10_fed_odplus_es.json](10_fed_odplus_es.json).
