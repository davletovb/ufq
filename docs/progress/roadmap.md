<!-- GENERATED FILE - do not edit by hand.
     Source: docs/progress/data/*.json
     Regenerate: python3 tools/progress/progress.py build -->

# Roadmap and gates

As of 2026-08-26. [Back to the tracker](README.md).

## Phase 0 — Calibration pilot  ▶︎ current

**Goal.** Calibrate items, formats and reading levels. Not sales.

**Scope.** Pilot build: M1 subset (~60 cards, ~10 videos), M2 calibration item set, M3-lite, M6 telemetry. Three deliberately different sites: a Tashkent private school, a viloyat-centre school, a rural school. Target n = 150-300 students, grades 7-9.

**Requirements in this phase.** `░░░░░░░░░░░░░░░░░░░░░░` 0% · 0/20 done

| Exit criterion | Target | Current | Status | Source |
|---|---|---|---|---|
| `PG0-1` Session completion across all three sites | >= 70% of started chunks | no data yet | ⬜ Not started | framework §11.4 |
| `PG0-2` Median unique career cards viewed per student | >= 12 | no data yet | ⬜ Not started | framework §11.4 |
| `PG0-3` Parent join rate in at least one site | >= 30% | no data yet | ⬜ Not started | framework §11.4 |
| `PG0-4` Calibration items flagged for comprehension failure in either script | < 10% | no data yet | ⬜ Not started | framework §11.4 |
| `PG0-5` Item pool surviving statistical screening into the v1 scored set | >= 60% | no data yet | ⬜ Not started | framework §11.4 |

## Phase 1 — MVP, B2C via Telegram (free)

**Goal.** Accumulate psychometric data, norms and word of mouth; the family module is the retention engine.

**Scope.** Telegram Mini App plus responsive web/PWA at account parity; three locales at full parity; M1 at content floor; M2 full item set with v1 scoring; M3 full; M4 template planner; M6 pipelines; consent, residency and audit logging.

**Requirements in this phase.** `░░░░░░░░░░░░░░░░░░░░░░` 0% · 0/13 done

| Exit criterion | Target | Current | Status | Source |
|---|---|---|---|---|
| `PG1-1` Norm baselines established | published | no data yet | ⬜ Not started | framework §10 |
| `PG1-2` Phase-1 metrics trending to target for one school term | one full term | no data yet | ⬜ Not started | framework §10, §13 |

## Phase 2 — B2B, private schools first

**Goal.** The advisor's operating system and the reporting wedge. Districts for public scale after.

**Scope.** M5 full, M7 async Q&A, lab mode, onboarding kit, manual invoicing, advisor micro-training.

**Requirements in this phase.** `░░░░░░░░░░░░░░░░░░░░░░` 0% · 0/6 done

| Exit criterion | Target | Current | Status | Source |
|---|---|---|---|---|
| `PG2-1` Paying schools with renewed intent | N - set in the Decisions Log at Phase-2 start | no data yet | ⬜ Not started | framework §10 |

## Phase 3 — Universities

**Goal.** First-year orientation, major-switching triage, employability. Not designed yet, by intent.

**Scope.** Deliberately undesigned.

**Requirements in this phase.** `░░░░░░░░░░░░░░░░░░░░░░` 0% · 0/0 done

| Exit criterion | Target | Current | Status | Source |
|---|---|---|---|---|
| `PG3-1` Local norms published | published | no data yet | ⬜ Not started | framework §10 |
| `PG3-2` Follow-up validity data from M6-F5 | collected | no data yet | ⬜ Not started | framework §10 |
| `PG3-3` Brand evidence universities will demand | documented | no data yet | ⬜ Not started | framework §10 |

## Content floor

| Target | Phase | Progress | Count | Source |
|---|---|---|---|---|
| Career cards | 0 | `░░░░░░░░░░░░░░` 0% | 0/60 cards | framework §10 |
| Day-in-the-life videos | 0 | `░░░░░░░░░░░░░░` 0% | 0/10 videos | framework §10 |
| Career cards | 1 | `░░░░░░░░░░░░░░` 0% | 0/120 cards | framework §10, §12 |
| Videos with low-bandwidth variants | 1 | `░░░░░░░░░░░░░░` 0% | 0/30 videos | framework §10, §12 |
| Pathway templates | 1 | `░░░░░░░░░░░░░░` 0% | 0/40 templates | framework §10, §12 |

## Success metrics

Targets are provisional and confirmed at each phase start via the Decisions Log.

| ID | Phase | Metric | Target | Current |
|---|---|---|---|---|
| `KPI-1` | 1 | Activation: signups completing at least one assessment chunk | >= 50% | no data yet |
| `KPI-2` | 1 | Exposure breadth: median unique cards viewed per 30 days | >= 15 | no data yet |
| `KPI-3` | 1 | Full assessment completion among activated users | >= 60% | no data yet |
| `KPI-4` | 1 | Parent join rate on invited families | >= 25% | no data yet |
| `KPI-5` | 1 | D30 retention on any meaningful event | >= 20% | no data yet |
| `KPI-6` | 1+ | Psychometric: dimension reliability | >= .70 | no data yet |
| `KPI-7` | 2 | Advisor weekly-active among licensed advisors | >= 60% | no data yet |
| `KPI-8` | 2 | Generated advisor reports per class per term | >= 1 | no data yet |
| `KPI-9` | 2 | School renewal intent at term end | >= 70% | no data yet |
| `KPI-10` | 1+ | Follow-up response rate at 6 months, via Telegram | >= 30% | no data yet |

## Launch checklist — phase 1

- [ ] `LC1-1` Telegram Mini App published; web/PWA live at parity; both scripts plus Russian verified in production
- [ ] `LC1-2` Privacy policy and consent flows live in uz and ru; data-residency verification documented; deletion flow tested end to end
- [ ] `LC1-3` Content floor met within freshness rules
- [ ] `LC1-4` Support channel live; crash and analytics dashboards on; rollback plan rehearsed
- [ ] `LC1-5` Brand register check: local, practical, slightly commercial - not an NGO intervention

## Launch checklist — phase 2

- [ ] `LC2-1` School onboarding kit: advisor micro-training, rostering guide, data-processing agreement, MOU template
- [ ] `LC2-2` Lab mode field-tested in at least two real school labs; report templates validated with at least two practising advisors
- [ ] `LC2-3` Pricing sheet approved; manual invoicing acceptable at start
- [ ] `LC2-4` Access matrix and E-3 non-features communicated to school leadership in writing during onboarding

## Risks and standing mitigations

| ID | Risk | Standing mitigation | Status |
|---|---|---|---|
| `RK-1` | Deterministic labeling | P-4, E-1, E-2 - plural provisional outputs are the only outputs that exist. | mitigated-by-design |
| `RK-2` | Test-gaming | E-7 low-stakes framing, no visible scores, behavioral signals that are hard to fake. | mitigated-by-design |
| `RK-3` | Being read as teaching children to defy parents | M3 overlap-first framing, parents' own values vocabulary, E-4 and E-6. | mitigated-by-design |
| `RK-4` | Institutional misuse | E-3 as a product-level refusal plus written expectation-setting at onboarding. | mitigated-by-design |
| `RK-5` | Content staleness | Freshness rules and publishing blocks; wage/cost data older than 6 months cannot publish. | open |
| `RK-6` | Transliteration credibility | Exception table as a tested artifact with a regression suite; human review of both scripts. | open |
| `RK-7` | Telegram platform dependency | Full web/PWA parity from MVP - the Mini App is a distribution choice, not the architecture. | mitigated-by-design |
| `RK-8` | Regulatory drift | M5-F3 report templates are content-configurable; maintain contact with pilot advisors as early warning. | open |
| `RK-9` | Donor-project aesthetics | Brand register check in the launch checklist; pricing exists because paid things are taken seriously. | open |
| `RK-10` | Copying | The moat is the content library, exposure-conditioned data, local norms and the validation loop. Invest there first. | open |
