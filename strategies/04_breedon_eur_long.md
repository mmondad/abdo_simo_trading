# 04 · Breedon EURUSD US-session long

**Family:** `breedon_fx_clock` · **Instrument:** `EURUSD` · **Status:** `RESEARCHED_NOT_BACKTESTED` · **Research score:** 66/100

## Original source and evidence

- [Intraday Patterns in FX Returns and Order Flow](https://www.snb.ch/public/asset/en/www-snb-ch/publications/research/working-papers/2011/working_paper_2011_04/publications0_en/working_paper_2011_04.n.pdf) — Breedon; Ranaldo, 2013, Journal of Money, Credit and Banking; 2011 SNB working-paper text.
- Source market: EBS EURUSD spot FX; selected market: `EURUSD`. Do not transfer this result to a CFD or micro contract unless it is the tested instrument.
- Historical sample: EBS spot FX 1997–2007; latest decade not tested.
- Author-reported result: Author-reported annualized trading return 0.07 (7%) and Sharpe 0.9 after EBS spread; no independent recent replication verified.
- Independent test: NOT VERIFIED. No backtest exists in this repository.

## Source rules

- Session/timezone: 08:00–16:00 America/New_York
- Timeframe and data: H1 boundary / M1 execution; EURUSD spot tick or M1 bid/ask history and both Europe/London and America/New_York daylight-saving calendars.
- Indicator: Fixed local clock session; no signal indicator beyond calendar time.
- BUY: Buy EURUSD at 08:00 America/New_York.
- SELL/SHORT: NONE; long-only US-session rule.
- Exit and mandatory same-session flat: Sell at 16:00 America/New_York on the same date.
- Source stop loss: NOT SPECIFIED
- Source take profit: NOT SPECIFIED
- Source position sizing: NOT SPECIFIED; fixed notional for replication is a proposal.
- Source cost treatment: Authors use EBS firm bid/ask; retail broker spread and slippage untested.
- Maximum holding: 8 h
- Maximum new entries per day in this selected specification: **1**; observed frequency: NOT REPORTED for this exact selected specification. The cap does not imply one trade every day.

## Proposed adaptations and gaps

- Proposed, not source-validated: Skip bank holidays only if predeclared, use broker quotes for the intended venue, no synthetic 5pm FX day boundary, one entry maximum. Test any protective stop separately.
- Key risks: Old interdealer sample; broker spread and changing FX flows.
- Additional implementation note: Eight-hour holding exceeds preferred four hours but is intraday and directly tested in historical source.
- Exact data and fill model must be acquired and checked before any independent backtest.

## Research score

Evidence 18/25; net after-cost evidence 11/20; rules 17/20; risk 6/15; data 9/10; regime robustness 5/10. This score ranks research priority, not expected profit.

Structured file: [04_breedon_eur_long.json](04_breedon_eur_long.json).
