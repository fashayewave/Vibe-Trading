# HQATL — Elliott Trade-Policy Experiment Matrix

**RESEARCH DRAFT · NOT HQATL VERIFIED · NOT A SPECIFICATION · NOT AUTHORIZED FOR IMPLEMENTATION**

- **Prepared for:** the HQATL build track, after the causal-swing fix (F1) + tests (B1) + first corrected baseline.
- **Premise (from the baseline run):** the current policy converts every completion *alert* into a **1-bar position** (avg holding = exactly 1 bar; Sharpe 0.14; 3/5 windows). This tests the **trade interpretation**, not Elliott itself. This matrix defines explicit, falsifiable trade policies to run against the **same detected structures** once detection / events / trade-lifecycle are separated (Codex's next target).
- **Rule:** change **one thing at a time** vs a frozen baseline; keep a policy only if evidence supports it.

---

## 1. Prerequisite: the three-layer contract

The policies below assume Codex's split. Concretely, the detector should emit an **event stream** (not signals), each event carrying enough for any policy to act:

```
ElliottEvent {
  timestamp            # bar the event is CONFIRMED on (post causal-lag, no look-ahead)
  type                 # IMPULSE_COMPLETE | ABC_COMPLETE | (later: WAVE3_IN_PROGRESS, ...)
  direction            # UP (5-up done / ABC-up done) | DOWN (5-down done / ABC-down done)
  p0..p5 / pa..pc      # the pivot prices/times the structure is built from
  invalidation_level   # structural stop (e.g. beyond wave-5 end, or beyond C)
  fib_targets[]        # projected corrective/continuation targets
}
```

A **trade policy** is a pure function `events + price -> positions`. Detection never changes across the matrix — only the policy does. This is what lets the desk *show* counts without auto-trading them (governance: "decision support, not autonomous authority").

---

## 2. Baselines / controls (run these first, they anchor everything)

| ID | Baseline | Purpose |
|---|---|---|
| **C0** | **Current 1-bar flip** (frozen) | the thing we're trying to beat; reproduces the 3.05% run |
| **C1** | **Buy-and-hold** each instrument | absolute yardstick (was ~310% — a bull-market ceiling, not the real bar) |
| **C2** | **Matched-random** — same trade count (~49) & holding-period distribution as the policy under test, entries at random timestamps, N≥1000 resamples | **the key control:** isolates whether Elliott *timing* adds anything beyond trade frequency |

**Decision rule (applies to every policy P):** keep P only if it beats **C2 on Sharpe** (outside the random band, e.g. >95th percentile) **and** holds up across a majority of sequential windows **out-of-sample**. Beating C1 is a bonus, not required (an occasional-signal strategy needn't beat leveraged-long-a-bull-market).

---

## 3. Trade policies (the experiment menu)

Each consumes the same event stream. Ordered by expected value / ease.

| ID | Policy | Entry | Hold / Exit | Hypothesis being tested |
|---|---|---|---|---|
| **P1** | **Hold-until-opposite** | on completion event, take the implied direction (5-up done → short/flat; ABC-down done → long) | hold until the next *opposing* completion event **or** `invalidation_level` breached | Does making it a *persistent* position (vs 1-bar) recover the edge the alert throws away? **(most direct fix — run first)** |
| **P2** | **Target-or-stop** | on completion event | exit at `fib_targets` (projected move) **or** `invalidation_level`, whichever first; time-stop at N bars | Do the structure's own projected targets/stops define a tradable envelope? |
| **P3** | **Trade-with-wave-3 (momentum)** | after a confirmed 1–2 sets up, enter *with* trend at start of wave 3 | exit at wave-3 completion (or trailing stop) | Flips from counter-trend tops/bottoms to riding the strongest wave — often the more tradable Elliott edge. Tests momentum vs mean-reversion framing. |
| **P4** | **Correction-complete, long-only** | only `ABC_COMPLETE → UP` events; ignore top-shorting | hold to next opposing event / invalidation | Does the long side alone carry the edge? Dodges the structural penalty of shorting an up-drifting index. |
| **P5** | **Confirmation-filtered** (wrapper on P1) | require a confirming close beyond a threshold (e.g. k×ATR past the pivot) *after* the event before entering | same as P1 | Do false/late completions explain the weak win rate? Trades quality for quantity. |
| **P6** | **Regime-gated** (wrapper on best of P1–P4) | only act when a trend filter is on (e.g. ADX>25 / above long MA); else flat | same as wrapped policy | Tests the RQ-002/RQ-003 "regime-dependence" idea empirically — *now a hypothesis, not a mandate*. |

**Variable-isolation note:** P5 and P6 are *wrappers* — run them only on top of whichever of P1–P4 wins, so each experiment changes one lever.

---

## 4. Optional detection variants (only if P1–P4 plateau)

These re-open the earlier "five disagreements" **as experiments**, each a one-line change tested against the frozen baseline:

- **D1 — close vs wick pivots** (the biggest RQ-002↔EWCore disagreement): swing extremes from `close` vs `high/low`.
- **D2 — min price-move filter** (audit F5): add %/ATR threshold to swing detection.
- **D3 — Fib tolerance tightness** (audit F4): sweep `fib_tolerance`.
- **D4 — wave-5 ratio check** (audit F2): add the W5≈W1 constraint the SKILL.md claims.

Run these **after** a trade policy works — changing detection and policy at once confounds results.

---

## 5. Evaluation protocol (hold constant across all runs)

- **Instruments/period:** same SPY/QQQ/AAPL 2018–2025 for comparability, **plus** at least one out-of-sample set (different tickers and/or an earlier period) before keeping anything.
- **Execution:** next-bar fill, slippage, costs — identical to the baseline harness already used.
- **No look-ahead:** every event confirmed post causal-lag (the F1 fix); tests assert signal timing has no future dependence.
- **Metrics (per run):** total & annual return, max drawdown, Sharpe, trades, win rate, **avg holding period** (watch this — it's the tell), profitable windows k/5.
- **Robustness:** Monte Carlo + bootstrap + sequential-window validation (as already run) **and C2 matched-random** for that policy's trade count/holding.
- **Report:** one row per (policy × instrument-set), baseline C0/C1/C2 alongside, so keep/reject is a glance.

---

## 6. Suggested order of execution

1. **C0, C1, C2** (anchors).
2. **P1** (hold-until-opposite) — most likely to recover edge; directly fixes the 1-bar problem.
3. **P4** (long-only) and **P3** (wave-3 momentum) — cheap, high-information.
4. **P2** (target-or-stop).
5. Wrappers **P5 / P6** on the winner.
6. Detection variants **D1–D4** only if P-policies plateau.

Stop early on any branch the moment C2 isn't beaten out-of-sample — that's the "test before trust / stand aside" discipline, applied to our own work.

---

*End of RESEARCH DRAFT. A menu of falsifiable experiments, not a specification. No implementation authorized; Codex owns the engineering and picks what to run.*
