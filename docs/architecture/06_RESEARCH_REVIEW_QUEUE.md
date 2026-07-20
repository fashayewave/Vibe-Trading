# HQATL Research Review Queue

## 1. Queue Purpose

This document tracks every HQATL research source from initial inventory through evidence verification. A research source must progress through the governed review lifecycle before any information from that source can influence an HQATL specification or implementation.

## 2. Research Status Lifecycle

- `INVENTORIED`
- `PENDING EVIDENCE REVIEW`
- `EVIDENCE REVIEW IN PROGRESS`
- `HQATL VERIFIED`
- `SPECIFICATION CANDIDATE`
- `IMPLEMENTED`
- `VALIDATED`
- `REJECTED`
- `SUPERSEDED`

## 3. Research Review Queue

| Source ID | Source Title | Research Division | Priority | Current Status | Review Owner | Evidence Review Date | Decision | Next Action | Repository Location |
|---|---|---|---|---|---|---|---|---|---|
| `HQATL-RQ-001` | Rocket Reference Notes | Elliott Wave Intelligence | High | `PENDING EVIDENCE REVIEW` | `[Unassigned]` | `[Pending]` | `[Pending]` | Conduct evidence review | `docs/research/rocket_reference_notes/ROCKET_REFERENCE_INDEX.md` |
| `HQATL-RQ-002` | Elliott Wave Quant System – Pre-Build Review | Elliott Wave Intelligence | High | `PENDING EVIDENCE REVIEW` | `[Unassigned]` | `[Pending]` | `[Pending]` | Conduct evidence review | `docs/research/source_documents/ELLIOTT_WAVE_QUANT_SYSTEM_PREBUILD_REVIEW.pdf` |
| `HQATL-RQ-003` | Quantitative Finance Master Reference | Quantitative Technical Evidence | Medium | `PENDING EVIDENCE REVIEW` | `[Unassigned]` | `[Pending]` | `[Pending]` | Conduct evidence review | `docs/research/source_documents/QUANTITATIVE_FINANCE_MASTER_REFERENCE.pdf` |
| `HQATL-RQ-004` | EWCore 0.1.5.4 Pine Script | Elliott Wave Intelligence | High | `PENDING EVIDENCE REVIEW` | `[Unassigned]` | `[Pending]` | `[Pending]` | Conduct evidence review | `docs/research/source_documents/EWCore_0.1.5.4.pine` |

## 4. Review Governance

- Registration does not imply approval.
- Every claim must be evidence reviewed before entering HQATL specifications.
- Every approved concept must remain traceable to its original source.
- Rejected and superseded research remains archived for historical traceability.
- Only `HQATL VERIFIED` research may be considered for promotion into a Research Specification.
- Research Specification, Architecture Design, and Engineering Specification approvals must precede implementation.
- Testing and empirical validation are separate gates.

## 5. Specification Gatekeeping Workflow

Research Library
↓

Research Review Queue
↓

Evidence Review
↓

Verified Evidence Library
↓

Research Specification
↓

Architecture Design
↓

Engineering Specification
↓

Implementation
↓

Testing
↓

Validation
↓

Production Candidate
