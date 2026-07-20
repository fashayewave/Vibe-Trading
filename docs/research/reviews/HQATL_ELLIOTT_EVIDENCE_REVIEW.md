# HQATL Elliott Cluster — Evidence Review

**RESEARCH DRAFT · NOT HQATL VERIFIED · NOT A SPECIFICATION · NOT AUTHORIZED FOR IMPLEMENTATION**

- **Prepared for:** HQATL evidence-review process (research support only)
- **Division:** Elliott Wave Intelligence
- **Sources reviewed in this pass:**
  - **RQ-001** — Rocket / HewsTradingEdge notes (21 screenshots: Diagonals page, Advanced Corrective page, 13-page combination Cheat Sheet)
  - **RQ-002** — *Elliott Wave Quant System – Pre-Build Review* (PDF, 20 sections)
  - **RQ-004** — EWCore 0.1.5.4 Pine (reference-only; rule logic lives in an external library — see §1)
- **Deferred:** RQ-003 (Quantitative Finance Master Reference) — separate Quant Technical division, reviewed separately.
- **Method:** Claims extracted from each source, then cross-compared for agreement, disagreement, and missing/weak evidence. No source is treated as true because it is confident, published, or implemented in code.

---

## 1. Source-quality assessment (per HQATL Source & Evidence Policy)

| Source | Type | Sourcing | Key caveat for evidence review |
|---|---|---|---|
| **RQ-002** Pre-Build Review | Evidence-review compilation | **Strong.** 29 named "verified" sources + **4 explicitly flagged as hallucinated/misapplied and removed** | Sources named are all **real, canonical texts** (Prechter & Frost, Elliott originals, Neely, Fischer, Pesavento, Carney, Bollinger, Ehlers, Lo et al.). BUT "verified" is the document's **self-attestation** — HQATL should still independently confirm before promoting any claim to `HQATL VERIFIED`. |
| **RQ-001** Rocket notes | Personal educational compilation | **None.** Rules presented as settled fact; no citations, page numbers, or source attributions | Every Rocket claim is currently **unsourced**. It should be treated as a hypothesis to be corroborated against RQ-002's cited sources, exactly as the Research Library already marks it (`REFERENCE ONLY`). |
| **RQ-004** EWCore Pine | Reference implementation | **N/A (code).** Hard-rule logic is **not in the provided file** — it is imported from `Wick-Sniper/EWCoreEvaluators/28` | The mandatory-rule *implementations* (`evaluateImpulseWindow`, etc.) cannot be inspected from what was provided. EWCore also references an unregistered source, **`EW_NEW.pdf`**, in code comments. |

**Positive signal:** RQ-002's self-flagging of hallucinated sources (Bhattacharya & Kumar 2006, Aiken 2005, Hochberg, and the *misapplied* Bergstresser & Pontiff tax paper) is exactly the discipline the HQATL Source & Evidence Policy asks for. This raises confidence in the document's process — but does not by itself discharge HQATL's own verification gate.

---

## 2. Claim-by-claim cross-source comparison

Legend: ✅ agree · ⚠️ partial/needs-resolution · ❌ contradiction · — not addressed by that source.

| # | Topic | RQ-001 Rocket | RQ-002 Pre-Build | RQ-004 EWCore Pine | Verdict |
|---|---|---|---|---|---|
| 1 | **3 mandatory impulse rules** (W2≤100% W1; W3 not shortest; W4 no W1 overlap) | Stated (diagonal page: "W4 overlap = violation in impulse"; "W3 never shortest") | Explicit, as **hard** rules | `tolWave2Pct/3Pct/4Pct` gates (default 0 = hard); diagonals exempt from W4 overlap | ✅ **Strong agreement (3 sources)** |
| 2 | **Measurement basis** (close vs wick/extreme) | Not specified in screenshots | **Close-based only** (Neely) — "removes wick ambiguity" | **Wick/extreme-based** — pivots taken from bar `high`/`low` | ❌ **Contradiction** — RQ-002 mandates close; EWCore uses extremes |
| 3 | **Zigzag** structure | 5-3-5; B retraces 38.2–61.8% of A; "B never > 61.8% in a standard zigzag"; C = 1.0–1.618× A | 5-3-5 (Prechter pp.45–55); Wave B (zigzag) **38.2–78.6%**; invalid >100% | 5-3-5 (evaluator external) | ⚠️ B-retrace ceiling differs (**61.8%** vs **78.6%**) |
| 4 | **Flat** (Regular/Expanded/Running) | All 3-3-5; Expanded "B exceeds prior high" | 3-3-5; Expanded B **>105%** threshold (Neely); Flat B retrace 90–138.2% | 3-3-5 (evaluator external) | ✅ Agreement (Expanded-B threshold ~105% consistent) |
| 5 | **Triangle structure** | ABCDE, 3-3-3-3-3; **3 types** (Contracting/Expanding/Barrier); never W2 or WA; precedes final move | ABCDE, all-3s; **4 types** (adds **Running**); Wave E undershoot <25% apex (Neely) | ABCDE 3-3-3-3-3; contracting/expanding wedge logic | ⚠️ **Type count differs** (3 vs 4); Barrier/Running under-covered by Rocket & EWCore |
| 6 | **Triangle thrust magnitude** | **75–100%** of widest part | Thrust = Wave A width; **Neely 100–138.2%** upper bound | **75–100%** of widest part (`f_projTargetLabels`/Fib box) | ⚠️ Rocket & EWCore agree (75–100%); **both under RQ-002/Neely's 100–138.2%** |
| 7 | **WXY / WXYXZ** complex | X connector retraces 50–78.6% of W/Y, no new extreme; Y=100% or 123.6–161.8% W; triangle only final unit | Double/Triple (Prechter pp.67–75; Neely); **"WXYXZ may exist only in theory"** | `enableCombo3` (WXY) / `enableCombo5` (WXYXZ); comment: **"per EW_NEW.pdf … 'may exist only in theory'"** | ✅ Agreement, incl. the *identical* "only in theory" caveat |
| 8 | **Leading diagonal** sub-structure | **3-3-3-3-3 only** ("all sub-waves corrective, zigzags") | **CONTESTED** — Prechter (some eds.) allows **5-3-5-3-5** OR 3-3-3-3-3; Neely strict 3-3-3-3-3. Build decision: show both, −10 pts, flag `[Contested]` | `enableDiagonal` = **3-3-3-3-3** | ❌ Rocket & EWCore adopt one side of a **contested** rule **without flagging it** |
| 9 | **Ending diagonal** | 3-3-3-3-3; converging or expanding; triple RSI divergence = exhaustion; W5 = 100% of W1 or shorter | Covered (Prechter/Neely) | Leading/Ending distinguished; ending-w5/wC positions in explanation logic | ✅ Agreement |
| 10 | **Fib retracements** | 0.236, 0.382, 0.5, 0.618, 0.786 | Same core set + zone/invalidation logic | `retracementLevels = 0.236,0.382,0.5,0.618,0.786` | ✅ **Exact agreement** |
| 11 | **Fib extensions** | 1.0, 1.272, **1.382**, 1.618, 2.0, 2.618 | 1.0, 1.272, 1.618, 2.0, 2.618, **3.618, 4.236, 5.618** (5.618 = single-source Pesavento, dashed/no-signal) | `extensionLevels = 1.0,1.272,1.618,2.0,2.618` | ⚠️ Rocket & EWCore **cap at 2.618**; RQ-002 documents higher levels (with its own single-source warning) |
| 12 | **Regime filter** (trend gate) | — | **ADX>25 OR Hurst>0.55 → else NEUTRAL** (Lo AMH); called *"the single most important modern correction"* | — (has RSI/MTF/parent-gate, **no ADX/Hurst regime gate**) | ⚠️ **Missing** in both Rocket & EWCore |
| 13 | **Momentum/RSI** | Leading diag = rising RSI/no divergence; ending = triple divergence; cross 50/70 | Elder: volume W3 vs W5 divergence; confidence scoring | `useMomentumScore`, RSI dominance of W3/WC (`rsiMomentumLength`) | ✅ Directionally aligned; specifics differ |
| 14 | **Alternate counts / invalidation** | Implicit (pattern-position logic) | Explicit alternate-count + invalidation cascade | `topInvalidationLevel`, alternates table, degree-first ranking | ✅ Concept aligned |

---

## 3. Notable agreements (candidate high-confidence — corroborated across ≥2 independent sources)

These are the strongest starting points; still require independent source verification before `HQATL VERIFIED`:

- **The three mandatory impulse rules** — agreed by all three sources (rows 1).
- **Corrective structure signatures** — Zigzag 5-3-5, Flat 3-3-5, Triangle 3-3-3-3-3 (ABCDE) (rows 3–5).
- **Fibonacci retracement set** (0.236–0.786) — *exact* match Rocket ↔ EWCore, consistent with RQ-002 (row 10).
- **WXYXZ "may exist only in theory"** — RQ-002 and EWCore state this **verbatim**, suggesting a shared lineage (row 7). *Worth confirming they don't share a common unverified origin (see §5).*
- **Diagonal W4-overlap exception** — universal (rows 1, 8–9).

---

## 4. Disagreements & contradictions to resolve (priority order)

1. **Measurement basis — close vs wick (row 2).** RQ-002 mandates close-based (Neely) to remove ambiguity; EWCore's detector triggers on bar `high`/`low` extremes. This is a **fundamental methodology fork** that changes every pivot, rule test, and Fib measurement. HQATL must decide which basis is authoritative before any spec.
2. **Leading-diagonal sub-structure (row 8).** Rocket and EWCore both hard-code 3-3-3-3-3; RQ-002 correctly flags this as a **contested rule** (Prechter allows 5-3-5-3-5). Rocket/EWCore present a contested point as settled — an oversimplification to correct.
3. **Triangle thrust magnitude (row 6)** and **type count (row 5).** Rocket/EWCore use 75–100% thrust and 3 types; RQ-002/Neely use 100–138.2% and 4 types (adds Running). Needs a single reconciled standard.
4. **Zigzag Wave-B ceiling (row 3):** 61.8% (Rocket) vs 78.6% (RQ-002).
5. **Fib extension range (row 11):** Rocket/EWCore stop at 2.618; RQ-002 extends to 4.236/5.618 (5.618 already self-flagged single-source).

---

## 5. Weak / single-source / missing evidence (route to Research Review Queue)

- **Regime filter absent** in both the teaching material (RQ-001) and the implementation (RQ-004), yet RQ-002 calls it the single most important modern empirical correction (Lo AMH). **Gap** — HQATL should decide whether an ADX/Hurst NEUTRAL gate belongs in the framework.
- **EWCore hard-rule logic is unavailable** — it lives in `EWCoreEvaluators/28`, not provided. The actual rule implementations therefore **cannot be evidence-reviewed** from RQ-004 as supplied. *Request the library, or downgrade RQ-004's usefulness to "input geometry only."*
- **EWCore references `EW_NEW.pdf`** — an unregistered source. Either register and review it, or treat EWCore's "only in theory" comment as **uncorroborated**.
- **RQ-001 is entirely unsourced.** Its rules should each be tagged to a corroborating RQ-002 citation (mostly Prechter & Frost / Neely) before any Rocket claim advances.
- **5.618 extension** — RQ-002 itself flags as Pesavento-only; keep as dashed research level, no signal (already correct in RQ-002).
- **"WXYXZ only in theory"** appears identically in RQ-002 and EWCore — confirm this isn't a single shared unverified origin dressed as two sources (independence check per Source & Evidence Policy).

---

## 6. Note on RQ-002's "29 verified sources" claim

The claim is **credible but not yet HQATL-verified**:

- **What checks out:** every source *named* is a real, well-known work in its field (e.g., Prechter & Frost *Elliott Wave Principle* 1978; Neely *Mastering Elliott Wave* 1990; Fischer *Fibonacci Applications* 1993; Pesavento 1997; Carney *Harmonic Trading* 2010; Bollinger 2002; Ehlers 2004; Lo, Mamaysky & Wang, *J. Finance* 2000; Lo AMH 2004). ISBNs/DOIs are provided.
- **What still needs doing:** independent confirmation of ISBNs, page numbers, and that each cited page actually supports the specific claim attributed to it. The document's own "VERIFIED" mark is an assertion, not third-party verification.
- **Strong process signal:** the document removed 3 hallucinated citations and 1 misapplied one, naming each — this is the behavior HQATL's policy wants and materially raises confidence.

**Recommendation:** register RQ-002's source list as a *candidate* bibliography for the Elliott division; verify the ~6 load-bearing sources first (Prechter & Frost, Elliott originals, Neely, Fischer, Pesavento, Lo 2004) since most rules trace to them.

---

## 7. Recommended Research Review Queue updates & next steps

- Keep **RQ-001, RQ-002, RQ-004** at `PENDING EVIDENCE REVIEW`; attach this draft as the review record.
- Add **`EW_NEW.pdf`** and the **`EWCoreEvaluators` library** as *newly discovered, unregistered* sources needing intake (per §5).
- Consider adding **Frost & Prechter's *Elliott Wave Principle*** as its own registry entry (`HQATL-RQ-005`) — it is the load-bearing source behind most agreements above and is named in the governance docs' Source Evidence Policy but not yet in the queue.
- **Decision items for the human/audit gate:** the five items in §4 (measurement basis, leading-diagonal contested rule, triangle thrust/type, zigzag-B ceiling, Fib range) and the regime-filter gap in §5.
- **RQ-003 (Quant)** reviewed separately as the Quant Technical division.

---

*End of RESEARCH DRAFT. Contents are for review only and confer no approval, specification, or implementation authority. All cross-source claims require independent source verification before any promotion to HQATL VERIFIED.*
