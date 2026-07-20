# HQATL Documentation Reconciliation Map

**RESEARCH DRAFT · NOT HQATL VERIFIED · NOT A SPECIFICATION · NOT AUTHORIZED FOR IMPLEMENTATION**

- **Prepared for:** HQATL evidence-review process (research support only)
- **Repository:** `github.com/fashayewave/Vibe-Trading`
- **Branch:** `feature/project-foundation`
- **Scope compared:**
  - **Set 1** — 12 files under `docs/` (`HQATL_*.md`) + root `HQATL_MANIFEST.md`
  - **Set 2** — 7 numbered files under `docs/architecture/` (`00`–`06`) + `docs/research/rocket_reference_notes/ROCKET_REFERENCE_INDEX.md`
- **Governing set (per project brief):** `docs/architecture/` = **Set 2** governs. Set 1 treated as policy/detail annexes subordinate to it.

---

## Bottom line

The two sets are **~80% complementary**. The governance philosophy is **identical** across both (Elliott Wave primary; evidence over indicator-count; research before implementation; explainability with supporting/opposing/missing evidence; human decision authority; no live trading). There are **3 real contradictions** and several gaps to resolve before the evidence review relies on these documents. Nothing is broken — this is the expected seam between two doc layers authored at different times.

---

## Topic-by-topic map

| Topic | Set 1 (`docs/`) | Set 2 (`docs/architecture/`) | Relationship |
|---|---|---|---|
| Core philosophy | `HQATL_MANIFEST` | `00_VISION`, `02_DECISION_LOG` | Agree |
| Spec gatekeeping workflow | Charter refers to it | `01`, `02` (D006), `06` — identical 11-step chain | Agree |
| Capability taxonomy | `ARCHITECTURE_OVERVIEW` — 9 layers | `00_VISION` — 10 Divisions | Overlap (two structures for one system) |
| Roadmap / phases | `IMPLEMENTATION_ROADMAP` — Phases 0–12 | `01_PROJECT_ROADMAP` — 9 phases / 5 eras | **Contradict** (different numbering) |
| Vibe code audit | `MASTER_REQUIREMENTS`: "nothing audited," all `PLANNED` + `VIBE_AUDIT_CHECKLIST` (future) | `03_FEATURE_AUDIT`: "completed audit," KEEP/ENHANCE/ADD | **Contradict** ("not done" vs "done") |
| Research registry | `RESEARCH_REGISTRY` (empty template) + `RESEARCH_BACKLOG` (questions) | `04_RESEARCH_LIBRARY` + `06_REVIEW_QUEUE` (4 real sources) | Overlap (two registries) |
| Source policy | `SOURCE_EVIDENCE_POLICY` (source tiers, claim record) | `06` status lifecycle | Complement |
| Dashboard / decision UI | `DASHBOARD_VISION` + `TRADE_DECISION_WORKSPACE` (detailed) | `00_VISION` Div 6 & 7 (high-level) | Complement |
| Security | `SECURITY_POLICY` | — | Set 1 only — keep |
| Data providers | `DATA_PROVIDER_PLAN` | — | Set 1 only — keep |
| Glossary | — | `05_GLOSSARY` (empty skeleton) | Set 2 only — needs populating |
| Status vocabulary | `MASTER_REQUIREMENTS` vocab | `06` lifecycle + `03` audit vocab | Overlap (several vocabularies, no master key) |

---

## Contradictions to resolve (priority order)

### 1. The audit paradox (highest priority)
`MASTER_REQUIREMENTS` states *"No existing capability has been audited"* and marks everything `PLANNED`. `03_FEATURE_AUDIT` presents a *"completed Vibe repository discovery audit"* classifying ~50 features as `EXISTING` / KEEP / ENHANCE / ADD. Both cannot be true.

**Risk for evidence review:** if the Feature Audit was produced by an AI reading the repo, each `EXISTING` tag is itself an *unverified claim* — the exact thing HQATL governance requires to be evidence-reviewed before trust.

**Recommended resolution:** treat `03_FEATURE_AUDIT` as `PENDING EVIDENCE REVIEW`, not settled fact, until each `EXISTING` classification is traced to actual code. Then update `MASTER_REQUIREMENTS` statuses with evidence links.

### 2. Two roadmaps
Phases 0–12 (Set 1) vs 9 phases / 5 eras (Set 2). "Phase 1" means different things in each.

**Recommended resolution:** adopt Set 2's roadmap as canonical (it governs); fold Set 1's finer-grained items (EMA specs, iFVG, adaptive-indicator research, etc.) in as sub-tasks under the matching era.

### 3. Two capability structures
9 architectural layers (Set 1) vs 10 Vision Divisions (Set 2).

**Recommended resolution:** make the 10 Divisions the primary index (governing Vision); keep the 9 layers as the technical view, cross-referenced to it.

---

## Gaps

- **`05_GLOSSARY` is empty** — natural home for a single canonical status-vocabulary key mapping all status words (`PLANNED`, `EXISTING`, `PENDING EVIDENCE REVIEW`, `HQATL VERIFIED`, `LOCKED`, `KEEP/ENHANCE/ADD`, etc.).
- **Frost & Prechter's *Elliott Wave Principle*** is named as a foundational source in `SOURCE_EVIDENCE_POLICY` but is **not registered** in the Research Review Queue (`06`). If a real source, add it (e.g. `HQATL-RQ-005`).
- **Two research registries** (`RESEARCH_REGISTRY` empty template vs populated `04`/`06`) should be merged — retire the empty one, or make its per-claim template the format used inside the queue.
- **Set 1's relationship to the governing set is undeclared** — the 12 `docs/` files carry no numbering and sit outside `docs/architecture/`. A decision is needed: governing peers, subordinate annexes, or superseded drafts. (This draft assumes: subordinate annexes.)

---

## Registered research sources (from `04` / `06`)

| Source ID | Title | Division | Priority | Status | In Git? |
|---|---|---|---|---|---|
| `HQATL-RQ-001` | Rocket Reference Notes | Elliott Wave | High | PENDING EVIDENCE REVIEW | Index only |
| `HQATL-RQ-002` | Elliott Wave Quant System – Pre-Build Review | Elliott Wave | High | PENDING EVIDENCE REVIEW | No (PDF outside Git) |
| `HQATL-RQ-003` | Quantitative Finance Master Reference | Quant Technical | Medium | PENDING EVIDENCE REVIEW | No (PDF outside Git) |
| `HQATL-RQ-004` | EWCore 0.1.5.4 Pine Script | Elliott Wave | High | PENDING EVIDENCE REVIEW | No (Pine outside Git) |

**To perform evidence review (step b), these source files must be provided directly** — they are intentionally kept outside Git and are not readable from the repository.

---

*End of RESEARCH DRAFT. Contents are for review only and confer no approval, specification, or implementation authority.*
