<!-- GENERATED FILE - do not edit by hand.
     Source: docs/progress/data/*.json
     Regenerate: python3 tools/progress/progress.py build -->

# Decision ledger

Product decisions mirror the framework's Decisions Log, which stays authoritative. ADRs record implementation choices. Open questions are the things still costing us optionality.

As of 2026-08-26. [Back to the tracker](README.md).

## Product decisions

| ID | Date | Decision | Rationale | Owner | Affects |
|---|---|---|---|---|---|
| `D-1` | 2026-08-25 | RIASEC retained as internal scaffold only; re-derivation from local data planned. | GT-2, GT-3, P-5. | Research lead | `P-5`, `M2-F4`, `M6-F4` |
| `D-2` | 2026-08-25 | Primary audience grades 7-9. | Subject-block lock-in at 9-10 (GT-4). | Product | `R-1`, `GT-4` |
| `D-3` | 2026-08-25 | Telegram Mini App primary consumer surface with full web parity. | GT-6; platform-dependency risk. | Product/Eng | `NFR-1`, `NFR-2`, `RK-7` |
| `D-4` | 2026-08-25 | No ranked lists or individual score exports, permanently. | E-3; institutional-misuse risk. | Product | `E-3`, `M5-F6` |
| `D-5` | 2026-08-25 | B2B beachhead: private schools; public scale via tuman-level deals. | GT-7; sales-cycle reality. | Product | `M5`, `R-5` |
| `D-6` | 2026-08-25 | Migration pathway content on consumer surface only. | E-9; institutional sensitivity. | Content | `E-9`, `M4-F4` |

## Architecture decision records

| ID | Title | Status | Date | Product refs | Blocks | Tracking |
|---|---|---|---|---|---|---|
| `ADR-0001` | Choose the initial application stack | proposed | — | `NFR-1`, `NFR-2`, `GT-6` | `M1-F1`, `M1-F3`, `M6-F1` | [#1](https://github.com/davletovb/ufq/issues/1) |

## Open questions

| ID | Area | Question | Blocks | Source |
|---|---|---|---|---|
| `OQ-1` | engineering | Hosting provider inside Uzbekistan that satisfies the data-residency requirement. | `E-8` | framework §7.6 |
| `OQ-2` | content | Transliteration implementation: build-time or render-time, and who owns the exception table. | `NFR-5`, `RK-6` | framework §7.3 |
| `OQ-3` | research | The two remaining values cards, to be determined in Phase 0. | `M2-F1` | framework §6 M2-F1 |
| `OQ-4` | mentorship | Monetization of T-5 family consultations, and what paid mentorship does to the volunteer framing. | `T-5` | mentorship §11.1 |
| `OQ-5` | mentorship | Stipend levels and funding source for MS-2 near-peers, and whether university partners co-fund. | `MS-2` | mentorship §11.2 |
| `OQ-6` | mentorship | Moderation staffing for T-2 at launch scale: in-house or trained senior mentors. | `T-2` | mentorship §11.3 |
| `OQ-7` | mentorship | Who moderates T-3 content, and what advisor training adds for hosting duties. | `T-3` | mentorship §11.4 |
| `OQ-8` | content | Karakalpak and regional-language mentor supply timing relative to locale expansion. | `NFR-5` | mentorship §11.5 |
| `OQ-9` | legal | Legal review of obligations around organized minor-adult contact under Uzbek law. Required before any T-4+ format. | `T-4`, `T-5`, `T-6` | mentorship §11.6 |
| `OQ-10` | mentorship | Whether T-2 answers are attributable by full name or first name plus role. | `T-2` | mentorship §11.7 |

Open-question IDs are assigned by this tracker for reference; they are not IDs from the source documents.
