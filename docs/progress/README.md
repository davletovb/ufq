<!-- GENERATED FILE - do not edit by hand.
     Source: docs/progress/data/*.json
     Regenerate: python3 tools/progress/progress.py build -->

# UFQ progress tracker

**Phase 0 — Calibration pilot** · as of 2026-08-26 · [Roadmap](roadmap.md) · [Requirements](requirements.md) · [Guardrails](guardrails.md) · [Decisions](decisions.md) · [Visual dashboard](dashboard.html)

> Repository bootstrapped and the product framework is committed. No application code yet: the stack decision (ADR-0001) is open and blocks the first vertical slice.

## At a glance

| | Progress | |
|---|---|---|
| Delivery, all phases | `░░░░░░░░░░░░░░░░░░░░░░` | 0% · 0/39 done |
| MVP scope (Phase 1) | `░░░░░░░░░░░░░░░░░░░░░░` | 0% · 0/26 done |
| Binding guardrails upheld | `░░░░░░░░░░░░░░░░░░░░░░` | 0/16 · 0 at risk or violated |
| Open decisions | — | 1 ADR, 10 open questions |

## Phases

| Phase | | Requirements | Exit criteria met |
|---|---|---|---|
| ▶︎ **0 — Calibration pilot** | `░░░░░░░░░░░░░░` | 0% · 0/20 | 0/5 |
|   **1 — MVP, B2C via Telegram (free)** | `░░░░░░░░░░░░░░` | 0% · 0/13 | 0/2 |
|   **2 — B2B, private schools first** | `░░░░░░░░░░░░░░` | 0% · 0/6 | 0/1 |
|   **3 — Universities** | `░░░░░░░░░░░░░░` | 0% · 0/0 | 0/3 |

## Now and next

| ID | Requirement | Status | Owner | Tracking |
|---|---|---|---|---|
| `M1-F1` | Career card model | ⬜ Not started | Engineering | — |
| `M1-F3` | Exposure logging | ⬜ Not started | Engineering | [#2](https://github.com/davletovb/ufq/issues/2) |
| `M2-F3` | Session engine | ⬜ Not started | Engineering | — |
| `M6-F1` | Telemetry schema | ⬜ Not started | Engineering | [#2](https://github.com/davletovb/ufq/issues/2) |
| `NFR-6` | Resumability | ⬜ Not started | Engineering | — |

## Module board

| Module | Phase | | Features |
|---|---|---|---|
| ⬜ Not started **[`M1` Occupation Explorer](requirements.md#modules)** | 0 | `░░░░░░░░░░░░` 0% | ⬜ ⬜ ⬜ ⬜ ⬜ |
| ⬜ Not started **[`M2` Assessment Suite](requirements.md#modules)** | 0 | `░░░░░░░░░░░░` 0% | ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ |
| ⬜ Not started **[`M3` Family Module](requirements.md#modules)** | 0 | `░░░░░░░░░░░░` 0% | ⬜ ⬜ ⬜ ⬜ ⬜ |
| ⬜ Not started **[`M4` Pathway Planner](requirements.md#modules)** | 1 | `░░░░░░░░░░░░` 0% | ⬜ ⬜ ⬜ ⬜ |
| ⬜ Not started **[`M5` School Layer](requirements.md#modules)** | 2 | `░░░░░░░░░░░░` 0% | ⬜ ⬜ ⬜ ⬜ ⬜ |
| ⬜ Not started **[`M6` Research Layer](requirements.md#modules)** | 0 | `░░░░░░░░░░░░` 0% | ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ |
| 💤 Deferred **[`M7` Mentorship (deferred by design)](requirements.md#modules)** | 2 | `░░░░░░░░░░░░` 0% | — |

Feature icons in reading order: ⬜ not started, 🟡 in progress, 🟢 shipped, ✅ verified, ⛔ blocked, 💤 deferred, 📐 concept.

## Content floor

| Target | Phase | | Count |
|---|---|---|---|
| Career cards | 0 | `░░░░░░░░░░░░░░` | 0/60 cards |
| Day-in-the-life videos | 0 | `░░░░░░░░░░░░░░` | 0/10 videos |
| Career cards | 1 | `░░░░░░░░░░░░░░` | 0/120 cards |
| Videos with low-bandwidth variants | 1 | `░░░░░░░░░░░░░░` | 0/30 videos |
| Pathway templates | 1 | `░░░░░░░░░░░░░░` | 0/40 templates |

## How this stays true

This tracker is generated from `docs/progress/data/*.json`. Update the data in the same pull request as the work, run `python3 tools/progress/progress.py build`, and commit the regenerated views. CI fails a pull request whose views are stale or whose cited requirement IDs do not exist. See [HOWTO.md](HOWTO.md).
