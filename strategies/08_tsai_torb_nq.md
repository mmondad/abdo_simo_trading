# 08 · Tsai NQ timely opening-range breakout

**Family:** `opening_range_breakout` · **Instrument:** `NQ` · **Status:** `RESEARCHED_NOT_BACKTESTED` · **Research score:** 61/100

## Original source and evidence

- [Assessing the Profitability of Timely Opening Range Breakout on Index Futures Markets](https://doi.org/10.1109/ACCESS.2019.2899177) — Tsai et al., 2019, IEEE Access journal article.
- Source market: NQ and YM futures directly tested; selected market: `NQ`. Do not transfer this result to a CFD or micro contract unless it is the tested instrument.
- Historical sample: NQ 2001–2013 in paper; probe minute optimized on full sample.
- Author-reported result: Author-reported NQ 1-minute probe: 17.51% annual return after assumed cost, 3,099 transactions, p=0.3%; no independent untouched OOS.
- Independent test: NOT VERIFIED. No backtest exists in this repository.

## Source rules

- Session/timezone: Underlying US cash-market open to close; historical paper aligns to 09:30–16:00 America/New_York
- Timeframe and data: M1; Dated one-minute US index futures OHLC and preferably bid/ask, accurate cash-session calendar and contract roll metadata.
- Indicator: Probe high/low from first 1 or 4 minutes; first later cross gives direction; exit at active-hours end.
- BUY: After the one-minute opening probe, first price above the fixed probe high: buy once.
- SELL/SHORT: After the one-minute opening probe, first price below the fixed probe low: sell short once.
- Exit and mandatory same-session flat: Close any open position at underlying cash-market close on that date.
- Source stop loss: NOT SPECIFIED
- Source take profit: NOT SPECIFIED
- Source position sizing: NOT SPECIFIED; one fixed contract for backtest is a proposal, not paper rule.
- Source cost treatment: Author assumes 0.01% transaction cost per trade; not an exchange quote/fill model.
- Maximum holding: up to 6.5 h
- Maximum new entries per day in this selected specification: **1**; observed frequency: NOT REPORTED for this exact selected specification. The cap does not imply one trade every day.

## Proposed adaptations and gaps

- Proposed, not source-validated: First signal wins and no reversal/re-entry; choose next available executable price to avoid same-bar lookahead; use contract-specific tick/fee/slippage model. These are implementation choices.
- Key risks: Full-sample parameter selection, 1-minute fill sensitivity, no stop specified.
- Additional implementation note: First signal wins and no re-entry is a selected specification cap; source profit does not validate this implementation choice separately.
- Exact data and fill model must be acquired and checked before any independent backtest.

## Research score

Evidence 15/25; net after-cost evidence 11/20; rules 17/20; risk 5/15; data 8/10; regime robustness 5/10. This score ranks research priority, not expected profit.

Structured file: [08_tsai_torb_nq.json](08_tsai_torb_nq.json).
