# HQATL — Vibe Elliott Engine: Read-Only Executable Audit & KEEP / FIX / BUILD Gap List

**READ-ONLY AUDIT — FINDINGS ONLY · NO IMPLEMENTATION AUTHORIZED · DO NOT IMPLEMENT YET**

- **Prepared for:** HQATL build track (per the agreed reset: audit Vibe's real Elliott capability, then build + backtest one gap at a time)
- **Scope:** static read of `fashayewave/Vibe-Trading` @ `main`. No code executed, no changes made.
- **Question answered (Codex's):** where does the real Elliott engine end, and where does construction begin?

---

## 0. Headline

Vibe's "Elliott Wave capability" is **one skill**: a scenario guide (`SKILL.md`) + a single **example engine** (`example_signal_engine.py`, ~458 lines) + two Chinese reference notes. It is:

- ✅ **real, executable, and backtest-shaped** (its `generate(data_map)` contract matches the runner exactly), **but**
- ⚠️ **an untested template with a critical look-ahead flaw**, and
- ❌ **not integrated into any dashboard / decision workspace** (zero frontend wiring).

Honest baseline label: *a conservative, single-interpretation impulse/ABC detector — currently look-ahead-biased and untested.*

---

## 1. What the capability actually IS (architecture truth)

- Skills are loaded by `agent/src/agent/skills.py` (`SkillsLoader`) as **scenario guides** — it reads each `SKILL.md`; it does **not** execute the example engines.
- `example_signal_engine.py` is a **template the LLM agent adapts** when writing a strategy. The **backtest runner** then executes an agent-produced engine via `import module; SignalEngine().generate(data_map)` (`agent/backtest/runner.py:259`).
- It is **1 of 15** shipped `example_signal_engine.py` files across **87 skills** — Elliott is not privileged or wired into a product pipeline.
- **Classification:** `EXISTING` (executable example), **not** a productionized/integrated Elliott detector. This aligns with `03_FEATURE_AUDIT`'s "PARTIAL / skill material + example signal engine."

## 2. What the engine does (precisely)

`agent/src/skills/elliott-wave/example_signal_engine.py`:

- **Swing detection** (`_find_swings`, L73–74): centered rolling window (radius `swing_window=10` → 21-bar window) local extrema, then strict H/L alternation keeping the more extreme point on same-type runs.
- **Impulse** (`_find_impulse`, L193+): scans 6-swing windows (`L,H,L,H,L,H` bull / `H,L,H,L,H,L` bear); enforces the 3 iron rules; min-bar gap; loose Fibonacci filter; emits **−1 at a completed 5-wave up** / **+1 at a completed 5-wave down**.
- **ABC** (`_find_abc`, L270+): 4-swing windows; `B` must not break the start; `B` retraces 0.382–0.618 of `A` (±tol); `C` is 0.618–1.618 of `A` (±tol); emits **+1/−1 at C**.
- **`generate`** (L355+): provider-neutral; takes `data_map`, returns `1/-1/0` Series. **Contract matches the runner** (`runner.py:469` expects exactly `def generate(self, data_map: Dict[str, pd.DataFrame]) -> Dict[str, pd.Series]`, all-default `__init__`).

---

## 3. KEEP — works, preserve unchanged

| # | Item | Evidence |
|---|---|---|
| K1 | **The 3 iron rules are implemented correctly** — W2 doesn't break W0 (`L210/L246`); W3 not shortest (`L214/L250`); W4 no overlap into W1 (`L218/L254`). | matches classic EWT |
| K2 | **Backtest-compatible today** — engine signature + all-default `__init__` fit the runner contract (`runner.py:464,469`). | no adapter needed |
| K3 | **Provider-neutral engine** — OKX fetch is only in the `__main__` demo (`_fetch_okx`, L393); `generate()` has no provider coupling. Security scrubber (VT-001) already governs reachable engine code. | clean boundary |
| K4 | **"Rather miss than misclassify" single-interpretation design** — conservative bias; consistent with HQATL's "stand aside with discipline." | SKILL.md + code |

## 4. FIX — simplified / incorrect / risky (correct before trusting any backtest)

| # | Severity | Item | Location |
|---|---|---|---|
| **F1** | **CRITICAL** | **Look-ahead / repaint.** `rolling(full_w, center=True)` confirms a swing using **10 future bars**; signals are stamped at the swing's own timestamp (`p5["index"]`/`pc["index"]`), which can't be known until +10 bars. Any backtest stamping signals at those indices **leaks future information**. → emit with a confirmation lag (shift right by `swing_window`) or only confirm a swing once its right-side window closes. | `L73–74`; also `pattern_tool.py:41` |
| F2 | High | **Doc/impl mismatch:** `SKILL.md` claims "Wave 5 ≈ Wave 1," but `_check_fib_ratios` never checks a wave-5 ratio. Implement it or fix the doc. | `L108–148` |
| F3 | Med | **min-bars bug:** `_check_min_bars` uses `(idx_b − idx_a).days` — for intraday indices `.days≈0` (always fails); for daily it counts calendar days incl. weekend gaps, not bars. Should count index positions. Breaks on non-daily timeframes. | `L164–168` |
| F4 | Med | **Very loose Fibonacci bands** (`tol=0.15` on already-wide ranges → W2 ≈ 0.35–0.77, W3/W1 ≈ 0.85–2.77, W4 ≈ 0.09–0.65). Decide intended tightness — a prime candidate to tune **empirically**, not by decree. | `L128–148` |
| F5 | Med | **No minimum price-move filter** in swing detection (pure extrema + alternation, no %/ATR threshold) → noise-sensitive; not a true Zigzag. Testable variant vs ATR-adaptive pivots. | `L53–106` |
| F6 | Low | **Overwrite ordering:** in `generate`, the ABC loop runs after impulse and `signal[idx]=direction` overwrites a coincident impulse signal. Define precedence deliberately. | `L378–386` |
| F7 | Low | **No completed-bar / provisional flag** — OKX `confirm` column is dropped; engine can't distinguish forming vs closed bars. | `L415`, engine-wide |

## 5. BUILD — missing vs the stated goal (construct only where backtest evidence supports)

| # | Item | Notes |
|---|---|---|
| **B1** | **No-look-ahead, completed-bar tests for the Elliott engine** — **none exist today** (confirmed: no Elliott test in `agent/tests/`). Synthetic wave fixtures; assert signal timing has no future dependence. **Prerequisite for everything else.** |
| B2 | **Frozen baseline backtest harness** — wrap the unchanged engine as the baseline so every future change diffs against it. |
| B3 | **Testable variants (one at a time):** close-vs-wick pivots (F1-related), tighter Fib (F4), min-move filter (F5), wave-5 ratio (F2). Each is a hypothesis measured against B2 — the five "disagreements" from the earlier reviews live here as experiments, not roadblocks. |
| B4 | **Later-phase (out of scope now):** alternate-count/invalidation, degree/multi-timeframe, volume/RSI momentum, regime filter, and dashboard/decision-workspace integration (zero frontend wiring today). |

---

## 6. Where the real engine ends / construction begins

- **Real executable Elliott logic =** the ~458-line `SignalEngine` (swings + impulse + ABC + Fib + iron rules). It runs and is backtest-shaped. **Keep it as the baseline.**
- **Construction begins at:**
  1. **F1** — remove the look-ahead (confirmation lag), so backtests stop lying.
  2. **B1** — add no-look-ahead / completed-bar tests.
  3. **B2** — freeze the corrected engine as the baseline.
  4. Then **B3** — test one variant at a time against the baseline; keep only what the evidence supports.

Everything above is a **finding**, not a change. No code was modified. Recommend Codex own steps 1–4 as approved engineering, starting with F1 + B1.

---

*End of read-only audit. No implementation authorized by this document.*
