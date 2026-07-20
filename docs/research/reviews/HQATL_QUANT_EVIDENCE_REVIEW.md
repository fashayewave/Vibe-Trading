# HQATL Quant Cluster — Evidence Review

**RESEARCH DRAFT · NOT HQATL VERIFIED · NOT A SPECIFICATION · NOT AUTHORIZED FOR IMPLEMENTATION**

- **Prepared for:** HQATL evidence-review process (research support only)
- **Division:** Quantitative Technical Evidence
- **Source reviewed:** **RQ-003** — *Quantitative Finance Master Reference / The Master Reference Compendium* (PDF, 6 sections, 16 pages)
- **Method:** Claims extracted and checked for internal accuracy, source integrity, and relevance to HQATL's Quant Technical division. No claim is treated as true because the document asserts it is "verified."

---

## 1. Source-quality assessment (per HQATL Source & Evidence Policy)

**Verdict: strong sourcing, one transparency gap.**

- **Strengths:** RQ-003 carries a full annotated reference directory (Section 6) with **52 citations**, real page numbers, ISBNs/DOIs, and **FREE archive links** (Archive.org, JSTOR, Gallica BnF, SSRN, AEA). Every source *named* is a genuine, load-bearing quant-finance work — de Moivre, Gauss, Laplace, Quetelet, Galton, Pearson, Mandelbrot (1963), Taleb, Markowitz (1952), Sharpe (1964), Engle (ARCH, 1982, Nobel), Bollerslev (GARCH, 1986), Bollinger (2002), McNeil/Frey/Embrechts (2005), Fama-French, Gatev et al., DeBondt & Thaler, Whaley, Asness et al. (2013), Patterson (*The Quants*). Self-reported tally: **52 verified / 4 hallucinated removed / 28 free**.
- **Transparency gap vs RQ-002:** RQ-003 states *"Hallucinated Sources Removed: 4"* and *"where a source could not be fully verified, it was omitted"* — but **does not name the 4 removed sources.** RQ-002 named each removed hallucination explicitly. For an audit trail, the un-named removals in RQ-003 are **less verifiable**; request the list of what was removed and why.
- **Caveat (same as RQ-002):** "All citations verified" is the document's **self-attestation**. HQATL should independently confirm the load-bearing sources before promotion to `HQATL VERIFIED`.

---

## 2. Claim inventory (by section)

| Section | Core claims | Sources cited | Notes |
|---|---|---|---|
| **1. Bell curve & normal dist.** | Curve pre-dates Gauss (de Moivre 1718); CLT (Laplace); 68-95-99.7 empirical rule; **fails in finance — fat tails** | de Moivre, Gauss, Laplace, Quetelet, Galton, Pearson, Mandelbrot 1963 | Fat-tail conclusion is the key HQATL-relevant claim; see accuracy flags §3 |
| **2. International mathematicians** | Who built quant finance (pre-1950 → modern) | Biographical/historical | Context; low direct HQATL relevance |
| **3. Trader competitions** | Global competition results → strategy hierarchy "from live performance, not backtests" | Competition data (WorldQuant, Numerai, Kaggle, QuantConnect) | Interesting but **not independently verifiable** as presented |
| **4. Trillion-dollar quants** | Industry ~$1.5–2T AUM; fund profiles (Medallion 66%/yr gross, D.E. Shaw, AQR, Bridgewater) | Patterson *The Quants*; Asness et al. 2013; Lux 2000; BarclayHedge 2024 | Real sources; return figures are famous but hard to independently audit |
| **5. Strategy comparisons / mean reversion** | Academic vs quant vs discretionary; **mean-reversion strategy table** with returns | Fama-French, Gatev (pairs), O'Shaughnessy (VC2), Connors & Alvarez (RSI2), DeBondt & Thaler, Bollinger, Whaley (VIX) | **Most HQATL-relevant section** — see §4 |
| **6. Reference directory** | Annotated bibliography + free-resource index | 52 sources | Strong; the backbone deliverable of the doc |

---

## 3. Accuracy flags (caught during review)

1. **Chebyshev conflation (Section 1.2).** The doc attributes the exact 68-95-99.7 percentages to *"Chebyshev (1867) proved these bounds."* **This is incorrect.** Chebyshev's inequality gives much *weaker* distribution-free bounds (≥75% at 2σ, ≥88.9% at 3σ). The exact 68.27/95.45/99.73% figures come from **integrating the normal PDF**, not from Chebyshev. Minor but real — flag before any glossary/spec reuse.
2. **"25-sigma event" attribution (Section 1.2).** The 25-standard-deviation framing is genuinely famous, but it traces to **Goldman's CFO describing the August 2007 "quant quake,"** not the 2008 crash as the doc states. Attribution/date nuance to correct.
3. **Strategy return figures (Section 5).** Numbers like RSI(2) *"15.95% vs 10.46%, 78% of years"* and pairs-trading returns are presented as documented fact. They trace to real published/backtested studies, but **must be independently verified and checked for the standard biases** (survivorship, look-ahead, post-publication decay). The doc itself commendably notes several strategies *"degraded post-2010"* — consistent with HQATL's "test before trust" principle.

None of these sink the document; they are the kind of precision issues the evidence review exists to catch.

---

## 4. Relevance to HQATL — this is the Quant Technical Evidence bibliography

RQ-003 is the natural **source backbone for several PLANNED HQATL modules** in `MASTER_REQUIREMENTS`:

- **EMA standard-deviation analytics / statistical projections** → Markowitz (1952), Sharpe (1964) establish std-dev-as-risk.
- **Modern adaptive Bollinger** → Bollinger (2002) directly; Engle ARCH (1982) + Bollerslev GARCH (1986) support *volatility-is-not-constant* → the empirical basis for **adaptive** (vs fixed) bands.
- **Mean reversion / regression channels** → Galton (regression to the mean), DeBondt & Thaler, Gatev (cointegration/OU-process pairs), Connors & Alvarez (RSI2).
- **Data-quality / stand-aside discipline** → Mandelbrot fat tails + McNeil/Frey/Embrechts (VaR, EVT) justify *why* naive normal-distribution assumptions must carry warnings.

**Recommendation:** treat RQ-003's Section 6 directory as the **candidate bibliography for the Quant Technical Evidence division**, mirroring how RQ-002 anchors the Elliott division.

---

## 5. Cross-cluster connection (Quant ↔ Elliott) — worth surfacing to the audit

RQ-003 **independently reinforces RQ-002's single biggest modern correction:**

- RQ-002 argues Elliott signals are **regime-conditional** (Lo AMH; ADX/Hurst NEUTRAL gate).
- RQ-003 independently documents **fat tails** (Mandelbrot), the **2007 Quant Quake / crowding risk**, and that mean-reversion edges **degrade post-2010** — all pointing to the same conclusion: *strategies are regime-dependent and decay; test before trust.*
- **Mandelbrot appears in BOTH documents** (fractal geometry → multi-degree waves in RQ-002; Lévy-stable fat tails in RQ-003) — a consistent, real, load-bearing source across both divisions.

This strengthens the case for building **regime-awareness and explicit uncertainty** into HQATL from the foundation — consistent with the Manifest's "stand aside with discipline" and "no guaranteed outcomes" principles.

---

## 6. Weak / missing evidence (route to Research Review Queue)

- **The 4 removed hallucinated sources are un-named** (§1) — request the list for the audit trail.
- **Competition-derived "strategy hierarchy" (Section 3)** is presented as fact but is **not independently verifiable** from the doc — treat as anecdotal until sourced.
- **Fund return figures (Section 4)** (e.g., Medallion 66%/yr) are real-world-famous but **not auditable**; keep as context, not evidence.
- **Strategy return/percentage claims (Section 5)** need independent verification + bias review before any use in an HQATL specification.
- **Two accuracy corrections** required (Chebyshev, 25-sigma) before any content is lifted into the Glossary or a spec.

---

## 7. Recommended Research Review Queue updates & next steps

- Keep **RQ-003** at `PENDING EVIDENCE REVIEW`; attach this draft as the review record.
- Register RQ-003's **Section 6 directory** as the *candidate* Quant Technical Evidence bibliography; verify the load-bearing sources first (Markowitz, Sharpe, Engle, Bollerslev, Bollinger, Mandelbrot, McNeil et al.).
- Log the **two accuracy corrections** (Chebyshev, 25-sigma) against the source.
- Request the **4 un-named removed sources** to complete the integrity check.
- **Decision item for the human/audit gate:** whether the fat-tail / regime-dependence evidence (shared with RQ-002) should be elevated into a foundational HQATL principle for the Quant and Elliott divisions alike.

---

*End of RESEARCH DRAFT. Contents are for review only and confer no approval, specification, or implementation authority. All claims require independent source verification before any promotion to HQATL VERIFIED.*
