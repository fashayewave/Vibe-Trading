# HQATL — Elliott Trade-Policy Experiment Matrix (v2)

**RESEARCH DRAFT · NOT HQATL VERIFIED · NOT A SPECIFICATION · NOT AUTHORIZED FOR IMPLEMENTATION**

- **Prepared for:** the HQATL build track, after the causal-swing fix (F1) + tests (B1) + first corrected baseline.
- **v2 note:** incorporates Codex's engineering corrections (2026‑07‑21). Changes are marked **[Codex]**.
- **Premise (from the baseline run):** the current policy converts every completion *alert* into a **1-bar position** (avg holding = exactly 1 bar; Sharpe 0.14; 3/5 windows). This tests the **trade interpretation**, not Elliott itself. This matrix defines explicit, falsifiable trade policies to run against the **same detected structures** once detection / events / trade-lifecycle are separated.
- **Rule:** change **one thing at a time** vs a frozen baseline; keep a policy only if evidence supports it.

---

## 1. Prerequisite: the three-layer contract  **[Codex — refined]**

1. **Detection** — causal pivots + *candidate* structures (no look-ahead).
2. **Events** — *confirmed* analytical interpretations and **invalidations** (e.g. "impulse completed," "count invalidated").
3. **Trade policy** — converts *selected* events into positions.

Each event carries enough for any policy to act:

```
ElliottEvent {
  timestamp            # bar the event is CONFIRMED on (post causal-lag, no look-ahead)
  type                 # IMPULSE_COMPLETE | ABC_COMPLETE | INVALIDATION | (later: WAVE1_2_SET, WAVE3_* ...)
  direction            # UP | DOWN  (direction of the completed structure)
  p0..p5 / pa..pc      # the pivot prices/times the structure is built from
  invalidation_level   # structural stop (later layer)
  fib_targets[]        # projected targets (later layer)
}
```

A **trade policy** is a pure function `events + price -> positions`. Detection never changes across the matrix — only the policy does. This lets the desk *show* counts without auto-trading them (governance: "decision support, not autonomous authority").

---

## 2. Baselines / controls

| ID | Baseline | Purpose |
|---|---|---|
| **C0** | **Current 1-bar flip** (frozen, preserved) | the thing we're trying to beat; reproduces the 3.05% run |
| **C1** | **Buy-and-hold** — **per instrument AND as an equal-weight portfolio [Codex]** | absolute yardstick (bull-market ceiling, not the real bar) |
| **C2** | **Matched-random** control | isolates whether Elliott *timing* adds anything |

**C2 must match each policy's full profile [Codex]:** symbol, **direction mix**, trade count, **holding-period distribution**, and **exposure** — not merely the number of trades. **C2 runs *after* P1a [Codex]**, because P1a determines the holding-period distribution the random trades must match. N ≥ 1000 resamples.

**Decision rule:** keep a policy only if it beats **C2 on Sharpe** (outside the random band, e.g. >95th pct) **and** holds up **out-of-sample** (see §5). Beating C1 is a bonus, not required.

---

## 3. Trade policies (the experiment menu)

Ordered by dependency and expected value.

| ID | Policy | Entry | Hold / Exit | Depends on |
|---|---|---|---|---|
| **P1a** | **Hold-until-opposite** *(run first)* | on a confirmed completion event, take the implied direction | hold until the next **opposing confirmed event** — **no stop yet [Codex]** | events layer only |
| **P1b** | **P1a + structural invalidation** | same as P1a | also exit on `invalidation_level` breach | **run only after P1a is kept [Codex]** (adds one variable) |
| **P4** | **Correction-complete → long** | **completed *downward* ABC event → open a *long* [Codex, disambiguated]** | hold to next opposing event | events layer |
| **P3** | **Trade-with-wave-3 (momentum)** | enter with trend at start of wave 3 | exit at wave-3 completion / trailing stop | **needs partial Wave 1–2 + Wave-3 events to exist first [Codex]** |
| **P2** | **Target-or-stop** | on completion event | exit at `fib_targets` or `invalidation_level` | **needs structural targets + invalidations to exist first [Codex]** |
| **P5** | **Confirmation-filtered** (wrapper) | require a confirming close past the pivot before entering | as wrapped policy | run on the winning policy |
| **P6** | **Regime-gated** (wrapper) | act only when a trend filter is on; else flat | as wrapped policy | run on the winning policy |

**Variable-isolation:** P5/P6 are wrappers — run only on top of whichever base policy wins.

---

## 4. Optional detection variants (only after a trade policy shows value)

Each a one-line change, tested against the frozen baseline — the earlier "five disagreements" as **experiments**:

- **D1 — close vs wick pivots** · **D2 — min price-move filter** · **D3 — Fib tolerance sweep** · **D4 — wave-5 ratio check**

Run these **after** a policy works; changing detection and policy at once confounds results.

---

## 5. Evaluation protocol

- **In-sample:** SPY/QQQ/AAPL 2018–2025 for comparability.
- **Genuine out-of-sample [Codex]:** Vibe's current sequential-window report is **not** real train/test walk-forward. Keep/reject decisions require a **separate untouched period or instrument set** the policy has never seen.
- **Execution:** next-bar fill, slippage, costs — identical to the baseline harness.
- **No look-ahead:** every event confirmed post causal-lag (F1); tests assert no future dependence.
- **Metrics:** total & annual return, max drawdown, Sharpe, trades, win rate, **avg holding period** (the tell), profitable windows.
- **Robustness:** Monte Carlo + bootstrap + **C2 matched-random** for that policy's full profile.

---

## 6. Corrected order of execution  **[Codex]**

1. **Preserve C0** — the completed one-bar baseline.
2. **C1 buy-and-hold** — per instrument *and* equal-weight portfolio.
3. **Implement** the detection / events / trade-policy separation.
4. **Implement P1a** — hold until an opposing confirmed event.
5. **Run P1a.**
6. **Run C2 matched-random** against P1a (matched to P1a's full profile).
7. **Test P1a out-of-sample** — untouched instruments or dates.
8. **Keep or reject P1a** on out-of-sample Sharpe vs C2.
9. **Only then P1b** — add structural invalidation.
10. **Delay D1–D4** until a trade policy has demonstrated value.

Stop early on any branch the moment C2 isn't beaten out-of-sample — "test before trust / stand aside," applied to our own work.

---

*End of RESEARCH DRAFT. A menu of falsifiable experiments, not a specification. No implementation authorized; Codex owns the engineering and picks what to run. The next coding task is the three-layer split, preserving C0 for comparison.*
