# HQATL Feature Audit

## Purpose

This document classifies the capabilities identified during the completed Vibe repository discovery audit against the approved HQATL Vision. The classifications describe preservation and planning direction only. They do not authorize implementation, removal, live execution, or progression into a later development phase.

Current Status uses the HQATL audit vocabulary. HQATL Decision uses only `KEEP`, `ENHANCE`, `ADD`, `REMOVE`, or `UNKNOWN`.

## KEEP

| Feature Name | Current Status | HQATL Decision | Short Reason |
|---|---|---|---|
| FastAPI service architecture | `EXISTING` | `KEEP` | Provides an established backend boundary for research and application services. |
| React single-page application | `EXISTING` | `KEEP` | Provides the existing user-interface foundation. |
| Application routing and shared layout | `EXISTING` | `KEEP` | Supports established pages, navigation, sessions, themes, and localization. |
| Agent and session workspace | `EXISTING` | `KEEP` | Provides the current natural-language research interaction surface. |
| ECharts visualization foundation | `EXISTING` | `KEEP` | Supports candlesticks, equity curves, drawdowns, overlays, and correlation views. |
| Backend-provided chart series | `EXISTING` | `KEEP` | Allows analytical series to be supplied to charts without binding them to a provider. |
| Historical market-data loader registry | `EXISTING` | `KEEP` | Provides a modular, multi-provider data-access boundary. |
| Market-aware provider fallback routing | `EXISTING` | `KEEP` | Preserves provider flexibility while separating data access from analysis. |
| OHLC data validation | `EXISTING` | `KEEP` | Supports research-data quality and protects downstream analysis. |
| Settled-range market-data cache | `EXISTING` | `KEEP` | Supports repeatable and efficient historical research. |
| Multi-market backtesting engines | `EXISTING` | `KEEP` | Provide an established historical-research and simulation foundation. |
| Shared base backtest engine | `EXISTING` | `KEEP` | Provides a common execution path for historical analysis. |
| Performance metrics | `EXISTING` | `KEEP` | Support the Evidence Library and Backtesting & Validation divisions. |
| Monte Carlo validation | `EXISTING` | `KEEP` | Provides an existing statistical validation capability. |
| Portfolio optimizers | `EXISTING` | `KEEP` | Provide existing research tools that can remain independently governed. |
| Trade and run artifact logging | `EXISTING` | `KEEP` | Supports traceability, reports, audits, and reproducible research. |
| Factor and alpha registry | `EXISTING` | `KEEP` | Provides a strong modular pattern for registered quantitative research. |
| Alpha benchmarking and comparison | `EXISTING` | `KEEP` | Supports comparative research and evidence gathering. |
| ReAct agent loop and tool registry | `EXISTING` | `KEEP` | Provides the existing controlled research-assistant architecture. |
| Goal, claim, criterion, evidence, and audit records | `EXISTING` | `KEEP` | Align with HQATL's evidence and explainability objectives. |
| Hypothesis registry | `EXISTING` | `KEEP` | Supports research-before-implementation governance. |
| Strategy store and decay monitoring | `EXISTING` | `KEEP` | Supports research lifecycle tracking and evidence retention. |
| HTML and PDF reporting | `EXISTING` | `KEEP` | Supports documentation, visualization, and research reporting. |
| CLI and MCP interfaces | `EXISTING` | `KEEP` | Preserve established operator and integration surfaces. |
| Authentication, redaction, and security controls | `EXISTING` | `KEEP` | Security controls are foundational and must be preserved. |
| Multi-language and theme support | `EXISTING` | `KEEP` | Preserves existing application usability and presentation capabilities. |
| Wiki and documentation site | `EXISTING` | `KEEP` | Supports the Education & Documentation and Research Library divisions. |

## ENHANCE

| Feature Name | Current Status | HQATL Decision | Short Reason |
|---|---|---|---|
| Existing dashboard and routed workbench | `PARTIAL` | `ENHANCE` | Existing pages and panels are useful, but the Vision calls for a broader research and decision workspace. |
| Chart system | `PARTIAL` | `ENHANCE` | Existing charts are capable, but the Vision includes layouts, widgets, multi-timeframe work, visualization, and reports. |
| Frontend technical-indicator calculations | `EXISTING` | `ENHANCE` | Existing calculations should ultimately align with shared analytical and backtesting calculations rather than remain duplicated presentation logic. |
| Backend run-indicator overlays | `PARTIAL` | `ENHANCE` | Existing moving-average output is limited and is not a general analytical framework. |
| Pattern-recognition tool | `PARTIAL` | `ENHANCE` | Existing heuristic pattern, trend, swing, and support/resistance functions require clearer semantics and validation. |
| Elliott Wave capability | `PARTIAL` | `ENHANCE` | The repository contains skill material and an example signal engine, while the approved Vision requires Elliott Wave Intelligence as the primary analytical framework. |
| Market-structure capability | `PARTIAL` | `ENHANCE` | Related examples and dependencies exist, but the Vision requires a governed contextual-intelligence capability. |
| Existing walk-forward analysis | `PARTIAL` | `ENHANCE` | Temporal evaluation exists, but the Vision requires a broader governed validation program. |
| Persistent research memory | `EXISTING` | `ENHANCE` | Existing memory is useful but requires research provenance, review, and staleness discipline. |
| Swarm and multi-agent research runtime | `EXISTING` | `ENHANCE` | Existing orchestration can support research, but conclusions must remain evidence-backed and explainable. |
| Report content model | `PARTIAL` | `ENHANCE` | Reporting exists, but the Vision requires integrated research, evidence, decision, and validation reporting. |
| Data-quality reporting | `PARTIAL` | `ENHANCE` | Input validation and warnings exist, but research conclusions need stronger completeness, freshness, provenance, and limitation reporting. |
| Correlation analysis | `EXISTING` | `ENHANCE` | Existing calculation and visualization support part of Contextual Intelligence but not its complete approved scope. |
| Research scheduling | `EXISTING` | `ENHANCE` | Existing scheduling can support future research workflows after governance and evidence requirements are applied. |

## ADD

| Feature Name | Current Status | HQATL Decision | Short Reason |
|---|---|---|---|
| Shared backend analytical framework | `MISSING` | `ADD` | HQATL requires analytical and backtesting calculations to share governed implementations. |
| Explainable evidence-result model | `MISSING` | `ADD` | The Vision requires evidence and confidence while HQATL requires supporting, opposing, and missing evidence to remain explicit. |
| Linked research and Trade Decision Workspace | `MISSING` | `ADD` | The approved Vision defines research, bias, evidence, confidence, entry, invalidation, targets, and trade summary as one division. |
| Modular dashboard layouts and widgets | `MISSING` | `ADD` | The existing UI has fixed page composition, while the Vision explicitly includes layouts and widgets. |
| Multi-timeframe research workspace | `MISSING` | `ADD` | The Vision explicitly includes a multi-timeframe workspace beyond the current chart-range controls. |
| Persistent chart drawing and annotation system | `MISSING` | `ADD` | Charts exist, but the audited application has no persistent research drawing or annotation framework. |
| Evidence Library structure | `MISSING` | `ADD` | The Vision requires an organized home for backtests, validation, case studies, historical research, statistics, and verified findings. |
| Governed Research Library structure | `PARTIAL` | `ADD` | Documentation and skills exist, but the approved Vision requires a curated research library with controlled evidence and references. |
| Unified HQATL terminology and glossary | `PARTIAL` | `ADD` | A glossary document exists as a foundation artifact but has not yet been populated and approved. |
| Integrated contextual-intelligence workspace | `MISSING` | `ADD` | The Vision combines intermarket, correlation, market structure, macro, sector, sentiment, and Dow relationships into a governed research area. |
| Statistical projection research area | `MISSING` | `ADD` | The Vision explicitly identifies statistical projections within Quantitative Technical Evidence. |

## REMOVE

No features are approved for removal. The completed audit required preservation of existing Vibe functionality and did not establish sufficient evidence for deleting any capability.

## UNKNOWN

| Feature Name | Current Status | HQATL Decision | Short Reason |
|---|---|---|---|
| Individual factor and alpha suitability for HQATL | `NOT AUDITED` | `UNKNOWN` | The registry is executable, but each factor's formula, independence, assumptions, and value have not been individually approved for HQATL. |
| Harmonic-pattern capability | `PARTIAL` | `UNKNOWN` | Skill material and an optional dependency exist, but production integration and validation require further investigation. |
| Smart Money Concepts example engine | `PARTIAL` | `UNKNOWN` | Executable example code exists, but its production status and research suitability remain unapproved. |
| Fractal-analysis capability | `NOT AUDITED` | `UNKNOWN` | Related concepts appear in skills and analytical material, but no dedicated audited production framework was established. |
| Broker read connections | `EXISTING` | `UNKNOWN` | Existing Vibe capability is outside the current HQATL foundation decision. |
| Paper-trading connections | `EXISTING` | `UNKNOWN` | Existing capability is outside the current research-only foundation scope. |
| Live-trading and order-routing connections | `EXISTING` | `UNKNOWN` | Existing Vibe functionality must remain isolated and is not authorized by the HQATL roadmap. |
| Automated research conclusions | `PARTIAL` | `UNKNOWN` | Agent and swarm systems can generate conclusions, but HQATL evidence and validation standards have not yet been applied. |
