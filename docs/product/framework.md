# Career Discovery Platform — Uzbekistan
## Product Framework & Source of Truth

| Field | Value |
|---|---|
| Version | 0.1 (draft for team review) |
| Date | 25 August 2026 |
| Status | Governing document for the MVP development, testing, and publishing phases |
| Audience | Project management, developers, content team, research lead |
| Change process | Amendments go through the Decisions Log (§16). No silent edits. |

---

## 1. Purpose and scope of this document

This document is the single source of truth for the platform across three phases: MVP development, pilot testing, and publishing/rollout. It defines what we are building and why (§2–§6), how (§7–§9), in what order (§10), how we verify that it works (§11), how we ship (§12–§13), and what could go wrong (§14).

Where a ticket, a design file, or a verbal agreement conflicts with this document, this document wins until the Decisions Log records a change.

**Referencing convention.** Everything that tickets and PRs may need to point at has a stable ID: ground truths `GT-n`, principles `P-n`, roles `R-n`, modules `M-n`, functional requirements `Mn-Fn`, non-functional requirements `NFR-n`, ethics guardrails `E-n`. Use these IDs in issue trackers and commit messages so decisions stay traceable to their rationale.

---

## 2. Product vision

The standard Western career-discovery stack — interest inventory → type label → matching occupation list — assumes three things Uzbekistan does not reliably supply: an individual who chooses alone, a child who already knows the occupational landscape well enough to have differentiated interests in it, and a labor market where interest-fit predicts returns. None of the three holds cleanly here. The product therefore inverts the standard sequence:

1. **Exposure before assessment.** You cannot measure interest in occupations a child has never seen.
2. **Family before individual.** The household is the deciding unit; the product's flagship output is a structured family conversation, not a verdict for the child.
3. **Pathways before types.** The output is always concrete, plural, financed next steps — never a personality label.

**Product in one sentence.** A Telegram-first and web platform where schoolchildren (grades 7–9 core) discover the occupational landscape, are assessed through behavior rather than self-description, and receive — together with their parents — concrete, financed, plural pathways; schools get an advisor operating system that fulfills the state-mandated career-orientation function.

**Relationship to the existing RIASEC work.** The existing 28-item Holland-framework instrument (React, EN/UZ/RU) is retained as the internal v0 scaffold and item source. It is explicitly provisional: the interest structure will be re-derived from our own Uzbek response data (§6 M6, §11.2). RIASEC codes never appear in child-facing or parent-facing UI (E-2).

---

## 3. Ground truths (context the design must absorb)

Each ground truth ends with its binding design implication. These are constraints, not opinions; changing one requires a Decisions Log entry.

**GT-1 — The deciding unit is the household, not the child.** Career choice functions as a family portfolio decision: diversifying income sources, securing stability, and maintaining legibility to relatives and the mahalla. Social evaluation ("odamlar nima deydi") is a real utility term, not noise. A tool that only talks to the teenager optimizes the wrong actor and gets overridden at the dinner table.
*Implication:* the core deliverable is a negotiation artifact for the family (M3), and the parent is a first-class user (R2), not an afterthought.

**GT-2 — Occupational awareness is narrow, and Soviet-inflected at the parent level.** A fifteen-year-old can name perhaps two dozen professions; many parents' occupational map effectively froze around 1995, minus IT-as-magic. An interest inventory administered over unfamiliar occupations measures familiarity and prestige, not interest.
*Implication:* exposure (M1) precedes and feeds assessment (M2); interest is scored only over activities and occupations the platform has surfaced to that child (M2-F2). Exposure history is a logged, first-class data stream.

**GT-3 — Self-report psychometrics degrade in predictable ways.** Acquiescence bias, social desirability, unfamiliar Likert conventions, the DTM-conditioned instinct that every test has a correct answer to find, and a parent physically beside the child on a shared phone.
*Implication:* format-level countermeasures, not translation-level ones — forced-choice triads, situational judgments, performance mini-tasks, and behavioral telemetry as revealed preference. Child-facing language never says "test" (o'yin, not imtihon), and there is no visible score (E-7).

**GT-4 — The prestige economy and the wage economy have diverged, and lock-in comes early.** Medicine and law are oversubscribed relative to returns; real money moves through trades, logistics, agro-processing, IT services, and labor migration. Grant/kontrakt economics make feasibility a first-class variable, and subject-block choice around grades 9–10 forecloses paths before "discovery" normally happens.
*Implication:* the primary audience is grades 7–9 (R1); every recommendation carries a financing path and a subject-block plan (M4); vocational routes get production parity with university routes (E-10 in content policy, §11.3).

**GT-5 — Constraints are structured by gender and geography.** Some families cap a daughter's options by marriage timing; some professions are socially coded; mobility to Tashkent is a live constraint for regional children.
*Implication:* constraints enter the system only as explicit family-stated inputs to navigate (M2-F6), never as platform-encoded rules (E-5). The possibility space is expanded through content — regional women in IT, finance, engineering, shown matter-of-factly (M1 content policy) — not through exhortation.

**GT-6 — Infrastructure realities.** Telegram is the distribution layer; cheap, shared Android devices are the norm; regional bandwidth is thin; school computer labs require a batch, low-bandwidth "lab mode." Uzbek exists in two scripts plus a Russian parallel. Personal-data law requires in-country hosting, and users are minors.
*Implication:* Telegram Mini App as the primary consumer surface with full web parity (§7.1); single-source content with render-time Latin⇄Cyrillic transliteration and a curated exception table (§7.3); low-bandwidth media variants by default (§7.4); data residency, parental consent, and shared-device safety are architectural requirements, not features (§7.6, E-6, E-8).

**GT-7 — The state has already created our category.** Career orientation (kasbga yo'naltirish) is a mandated school function, and the September 2025 presidential decree on mandatory school advisors turned a vague obligation into a named, staffed, under-tooled role.
*Implication:* the B2B pitch is not "extra work" but the advisor's operating system — assessment, parent meetings, and the mandated reporting they already owe (M5). Private schools are the beachhead; districts (tuman-level) are the public-scale channel later (§10).

---

## 4. Design principles (non-negotiables)

Each principle includes a violation test — the concrete symptom that tells us we are drifting.

**P-1 — Exposure before assessment.** The explorer feeds the instrument.
*Violation test:* any interest item referencing an occupation the child has not been shown, or any child-facing item using bare occupation names.

**P-2 — Behavior over self-description.** Choices, task performance, and usage traces outrank agree/disagree statements.
*Violation test:* Likert agree-scales appearing in the child flow; a release where telemetry-derived signals are not part of the profile.

**P-3 — The family is the user.** Three-sided product — child, parent, advisor — and the flagship output is a structured family conversation.
*Violation test:* a launch plan or report design in which the parent has no role, or in which the child's result is framed as a verdict to be delivered to the parent.

**P-4 — Pathways, not labels.** Output is always plural, provisional, and concrete: next subject block, next course, next cost, plan B.
*Violation test:* any UI surface showing a type label, a single recommendation, or a score; fewer than three pathways in any generated report.

**P-5 — Local validity is built, not imported.** RIASEC is the starting hypothesis; every item is instrumented; the interest structure is re-derived from Uzbek data, with norms by cohort, region, and language of administration.
*Violation test:* shipping item changes without telemetry; treating the Holland hexagon as settled truth in scoring code; hard-coding weights no one can trace to data.

---

## 5. Users and roles

| ID | Role | Description | Phase |
|---|---|---|---|
| R-1 | Student | Grades 7–9 primary; 10–11 secondary. Uses explorer, assessment, pathway planner. | 0+ |
| R-2 | Parent / guardian | Runs the parallel parent instrument; receives the family congruence report; consent holder. | 0+ |
| R-3 | Family broker (optional) | The relative whose opinion actually carries — often an older sibling or uncle in IT. Invited as a viewer of the family report. | 1+ |
| R-4 | School advisor | The decree-mandated role; primary B2B user. Aggregate dashboards, one-at-a-time student summaries, report generation, parent-meeting log. | 2 |
| R-5 | School administrator / director | Buyer. Sees aggregate analytics only. | 2 |
| R-6 | Content editor (internal) | Maintains career cards, pathway templates, media, translations, verification dates. | 0+ |
| R-7 | Research lead (internal) | Owns item bank, telemetry analysis, norms, validation studies. | 0+ |
| — | University roles | Deferred to Phase 3. Not designed yet by intent. | 3 |

**Access matrix (binding; see also E-3, E-4):**

| Data | R-1 Student | R-2 Parent | R-3 Broker | R-4 Advisor | R-5 Admin | R-7 Research |
|---|---|---|---|---|---|---|
| Own item-level responses | Playful feedback only, no scores | Never | Never | Never | Never | De-identified |
| Individual profile summary | Own (pathway-framed) | Via family report only | Via family report only | One-at-a-time, access logged | Never | De-identified |
| Family congruence report | Yes | Yes | If invited | On family's request | Never | De-identified |
| Class/school aggregates | No | No | No | Yes | Yes | Yes |
| Ranked individual lists / score exports | **Does not exist as a product capability** (E-3) | | | | | |

---

## 6. Modules

Each module lists purpose, functional requirements, and phase. "Phase" marks when the module first ships; MVP scope is consolidated in §10.

### M1 — Occupation Explorer (content engine; the moat)

**Purpose.** Build occupational awareness before and during assessment; serve as the assessment's item pool; log exposure as a first-class data stream.

**Functional requirements.**
- **M1-F1 Career card model.** Every card carries: `id`; titles and body in uz-Latn (canonical), uz-Cyrl (transliterated + exceptions), ru (authored); cluster/tags; daily-reality description; entry routes; education requirement and subject-block mapping; cost-of-entry band; wage ranges by region at years 1/5/10; geography of demand (Tashkent / viloyat / abroad); related cards; media refs; `sources[]` and `last_verified` date; surface flags (see M4-F4).
- **M1-F2 Video content.** 60–90-second "bir kun" (day-in-the-life) videos with real people; every video has a low-bandwidth variant (audio + stills) generated by the media pipeline (§7.4).
- **M1-F3 Exposure logging.** Every card view logs dwell time, replays, returns, and completion; this stream feeds M2 scoring eligibility (P-1) and M6.
- **M1-F4 Browse and search** by cluster, tag, and free text, in all three locales, both scripts.
- **M1-F5 Content policy (editorial, enforced at review).** Deliberate over-indexing on regional role models, women in nontraditional fields shown matter-of-factly, and dignified skilled-trade arcs (apprentice → usta → own shop → employer). No gender-coded card copy.

**Phase:** 0 (subset) → 1 (full).

### M2 — Assessment Suite (multi-method, chunked)

**Purpose.** Produce a student profile from behavior and structured choice, not self-description.

**Functional requirements.**
- **M2-F1 Item formats.** (a) Forced-choice triads over *illustrated activities* — pick most-like-me and least-like-me; (b) situational-judgment items set in recognizably local scenes; (c) performance mini-tasks (MVP: one pattern/spatial task, one numeric task) with timing captured; (d) values card-sort — drag-rank of 8 value cards in parent-legible vocabulary (barqarorlik, daromad, obro', oilaga yaqinlik, halollik, mustaqillik, plus two determined in Phase 0); (e) constraints intake (M2-F6).
- **M2-F2 Exposure rule.** Interest items reference illustrated activities or occupations already surfaced via M1. Bare occupation names are forbidden in the child flow (P-1).
- **M2-F3 Session engine.** Sessions are 10–15-minute resumable chunks; state is server-side; a full profile accumulates across sessions. Designed for shared devices and 45-minute lessons.
- **M2-F4 Scoring v1.** Internal vectors only: interest (RIASEC-6, provisional per P-5), values (ranked 8), aptitude (per task), constraints (structured). Scoring code must be traceable to item data; weights are configuration, not constants buried in code.
- **M2-F5 Child-facing output.** Playful, non-evaluative feedback plus unlocked pathway suggestions. No scores, no types, no pass/fail (E-2, E-7).
- **M2-F6 Constraints intake.** Explicit family-context questions: budget band, mobility (can you study in Tashkent? abroad?), non-negotiables. Stored as stated constraints, used by M4; never inferred (E-5).

**Phase:** 0 (calibration set) → 1 (v1 scoring).

### M3 — Family Module

**Purpose.** Convert the child's profile and the parents' aspirations into a structured negotiation, not a confrontation.

**Functional requirements.**
- **M3-F1 Parent instrument.** ~10 minutes: aspiration picks, non-negotiables, an occupational-map exercise (surfacing outdated assumptions gently), and flexibility items — forced-choice formats, mirroring M2 conventions.
- **M3-F2 Invitation flow.** Child (or advisor, in Phase 2) invites the parent via Telegram deep link ("share with ota-ona"); parent onboarding must complete in one sitting on a low-end phone.
- **M3-F3 Family congruence report.** Where the child's profile and the parents' aspirations overlap; where they diverge (framed neutrally); three concrete pathways that live inside the overlap; a conversation guide. Rendered in the values vocabulary parents already optimize for.
- **M3-F4 Third seat.** Optional invited viewer (R-3) for the actual broker in many families.
- **M3-F5 Hard privacy rules.** Parents see fit and options, never the child's item-level answers (E-4). All child-visible outputs must be safe if seen by a parent on a shared device (E-6).

**Phase:** 0 (lite) → 1 (full).

### M4 — Pathway Planner

**Purpose.** Turn profiles and constraints into named, financed, plural routes.

**Functional requirements.**
- **M4-F1 Pathway template model.** Fields: target occupation(s); education step; subject block (fan bloki) and exam requirements; cost band; financing options (grant probability context, kontrakt band); timeline; plausible first job; plan-B link; region variants; surface flags.
- **M4-F2 Matching engine v1.** Rules/template matching over profile × constraints. No ML in MVP; every match must be explainable in one sentence.
- **M4-F3 Plurality rule.** Every generated plan contains ≥3 routes, always including at least one non-university route where constraints allow (P-4, GT-4).
- **M4-F4 Surface flags.** Migration-related pathway content renders on the consumer (B2C) surface only; the school-facing surface receives the softened variant (E-9, GT-4).

**Phase:** 1.

### M5 — School Layer (the advisor's operating system)

**Purpose.** Make the platform the tool with which the decree-mandated advisor does their job, including the reporting they owe.

**Functional requirements.**
- **M5-F1 Rostering** via class codes; no school-side IT integration required in Phase 2.
- **M5-F2 Advisor dashboard.** Class-level aggregate heatmaps; "no-signal" flags for profiles needing a human conversation; one-at-a-time student summaries with access logging (E-3).
- **M5-F3 Report generator.** One-click generation of the career-orientation documentation the advisor role requires, from aggregates.
- **M5-F4 Parent-meeting log** tied to family reports (with the family's consent).
- **M5-F5 Lab mode.** Batch student sessions on shared lab machines: low bandwidth, resumable, queue-and-sync tolerant of connectivity drops.
- **M5-F6 Explicit non-features.** No ranked lists, no individual score exports, no "class results" spreadsheet. These are refused at the product level, permanently (E-3).

**Phase:** 2.

### M6 — Research Layer

**Purpose.** Turn usage into validity: item statistics, local norms, and the evidence base Phase 3 will require.

**Functional requirements.**
- **M6-F1 Telemetry schema.** Exposure events, item responses with latency, session events — versioned, and present from the first pilot build (P-5).
- **M6-F2 Item bank** with per-item statistics pipeline (usage balance for forced-choice, discrimination, latency flags, comprehension flags).
- **M6-F3 Norms jobs** by cohort, region, and language/script of administration.
- **M6-F4 Structure analysis readiness.** Export shapes suitable for testing whether the six-factor interest structure holds locally, with re-clustering as the expected outcome, not a failure.
- **M6-F5 Follow-up scheduler.** 6- and 18-month follow-ups via Telegram (choice made, satisfaction, persistence) — the criterion-validation loop.
- **M6-F6 De-identified research exports** only (E-8).

**Phase:** 0 (telemetry) → 1 (pipelines) → ongoing.

### M7 — Mentorship (deferred by design)

Supply-side bootstrapping is hard, so mentorship starts asynchronous and cheap: "ask the person in the video" Q&A threads under career cards, then structured group sessions for schools, and only later 1:1 matching. Out of MVP; the only MVP-era dependency is that career cards can host threaded content later.

**Phase:** 2 (async Q&A) → 3.

---

## 7. Platform architecture

### 7.1 Surfaces
One backend, three surfaces:
1. **Telegram Mini App** — students and parents. Telegram auth, notifications, parent-invitation deep links; Payme/Click payment rails available natively when payments arrive (post-MVP).
2. **Web / PWA** — full account parity with the Mini App (phone-OTP auth); hosts lab mode in Phase 2. This is the mobile-friendly website requirement: one responsive web app, not a separate mobile site.
3. **School dashboard** — web, RBAC-gated, for R-4/R-5.

### 7.2 Backend
Single API serving all surfaces. Server-side session state (M2-F3). Role-based access control implementing the §5 access matrix. Feature flags per surface (e.g., migration content, E-9). Audit logging on any advisor access to individual student data.

### 7.3 Content and localization pipeline
- Canonical content is authored once in **uz-Latn**; **uz-Cyrl** is produced by render-time (or build-time) transliteration through a curated exception table covering the known breakage points (apostrophe forms oʻ/gʻ, ц/е-class loanword mappings, proper nouns). The exception table is a versioned, tested artifact with its own regression suite (§11.1).
- **Russian** is an authored parallel, not machine translation.
- **Karakalpak** is staged later; the pipeline must not assume exactly three locales.
- All content records carry `sources[]` and `last_verified`; the CMS blocks publishing wage/pathway data older than the freshness rule (§11.3).

### 7.4 Media pipeline
Every video is transcoded to a standard variant and a low-bandwidth variant (audio + stills). Client selects by measured connection quality; low-bandwidth is the default on unknown connections.

### 7.5 Core data model (entity sketch)
`User(role)`, `StudentProfile`, `FamilyLink` (parent/broker relations + consent state), `School`, `ClassGroup`, `AdvisorAssignment`, `CareerCard`, `MediaAsset`, `ExposureEvent`, `AssessmentItem`, `ItemResponse` (with latency), `SessionState`, `ProfileVector` (interest/values/aptitude/constraints, versioned), `PathwayTemplate`, `PathwayPlan`, `FamilyReport`, `AdvisorReport`, `ConsentRecord`, `AuditLog`. Vectors and scoring configs are versioned so that re-derivation (P-5) never silently rewrites history.

### 7.6 Hosting, compliance, security
- **Data residency:** personal data of Uzbek citizens is stored and processed on servers physically located in Uzbekistan, per the Law on Personal Data (ZRU-547) and its localization requirement. This is a hosting-selection constraint from day one.
- **Minors:** parental consent + child assent flows, recorded as `ConsentRecord`; data minimization; deletion on request (E-8).
- TLS everywhere; encryption at rest; rate limiting; audit logs (7.2). No third-party analytics that exfiltrate personal data out of country.

---

## 8. Non-functional requirements

- **NFR-1 Device floor.** Fully usable on Android 8 / 2 GB RAM class devices inside the Telegram webview, and in low-end desktop browsers for lab mode.
- **NFR-2 Payload budget.** Mini App core interactive bundle ≤ ~300 KB gzipped; media lazy-loaded; usable on a ~500 kbps connection.
- **NFR-3 Performance.** p95 API latency < 500 ms in-country; assessment interactions render feedback < 100 ms locally.
- **NFR-4 Availability.** ≥ 99.5% in Phase 1; degraded-mode reads (cached explorer content) when the API is unreachable.
- **NFR-5 Locale parity.** 100% of UI strings in uz-Latn, uz-Cyrl, ru at every release; per-script rendered-screenshot QA (§11.1).
- **NFR-6 Resumability.** Any session chunk survives connection loss and device handoff without data loss (M2-F3, M5-F5).
- **NFR-7 Accessibility & literacy.** Adjustable text size; icon-supported navigation; reading level calibrated in Phase 0 for grade 7.
- **NFR-8 Auditability.** Every advisor access to individual data is logged and reviewable (E-3).

---

## 9. Ethics and data guardrails (binding)

- **E-1 Plural, provisional outputs.** Every report contains ≥3 pathways with explicitly provisional framing. No single verdicts, ever.
- **E-2 No type labels** in child- or parent-facing UI. RIASEC and successor structures are internal vocabulary only.
- **E-3 No ranked lists or individual score exports** anywhere in the product. Advisor access to individuals is one-at-a-time and logged. This is a product-level refusal designed to precede institutional requests for it.
- **E-4 Parents see congruence and options, never item-level answers.**
- **E-5 No gender- or region-conditional logic** in scoring or matching. Constraints enter only as explicit family-stated inputs.
- **E-6 Shared-device safety.** Every child-visible screen must be safe if seen by a parent.
- **E-7 Low-stakes framing.** No scores, no pass/fail, game language not exam language — both an ethics rule and the anti-gaming strategy.
- **E-8 Consent and data rights.** Parental consent + child assent; deletion on request; research exports de-identified; publications report aggregates only.
- **E-9 Migration content** appears on the consumer surface only; the school surface carries the softened variant.
- **E-10 Vocational dignity parity.** Trades and certificate routes get the same content production value and matching weight as university routes.

---

## 10. Phase plan and MVP scope

| Phase | Goal | Core scope | Exit criteria |
|---|---|---|---|
| **0 — Calibration pilot** | Calibrate items, formats, reading levels; not sales. | Pilot build: M1 subset (~60 cards, ~10 videos), M2 calibration item set, M3-lite, M6 telemetry. Three deliberately different sites: a Tashkent private school, a viloyat-center school, a rural school. Target n = 150–300 students, grades 7–9. | §11.4 pilot acceptance criteria met. |
| **1 — MVP, B2C via Telegram (free)** | Accumulate psychometric data, norms, and word of mouth; family module is the retention engine. | See MVP scope table below. | Norm baselines established; Phase-1 metrics (§13) trending to target for one school term. |
| **2 — B2B, private schools first** | The advisor's OS; reporting wedge. Districts (tuman) for public scale after. | M5 full, M7 async Q&A, lab mode, onboarding kit, manual invoicing, advisor micro-training. | ≥N paying schools renewed intent (set N in Decisions Log at Phase-2 start). |
| **3 — Universities** | First-year orientation, major-switching triage, employability. | Not designed yet, by intent. | Entry requires: local norms published, follow-up validity data from M6-F5, and brand evidence — universities will demand proof. |

### MVP scope (Phase 1) — binding

| In MVP | Out of MVP (deferred to) |
|---|---|
| Telegram Mini App + responsive web/PWA, account parity | School dashboard, lab mode (Phase 2) |
| Locales: uz-Latn, uz-Cyrl, ru at full parity | Karakalpak (later) |
| M1: ≥120 career cards, ≥30 videos with low-bandwidth variants | Payments of any kind (Phase 2, B2B first) |
| M2: triads, SJT, 2 mini-tasks, values sort, constraints intake; v1 scoring | Mentorship / Q&A threads (Phase 2) |
| M3: parent instrument, invitation flow, family congruence report, third seat | University features (Phase 3) |
| M4: template-based planner, ~40 pathway templates, plurality rule | ML-based matching (post-MVP, only with M6 evidence) |
| M6: telemetry, item stats pipeline, follow-up scheduler | Public API / integrations |
| Consent flows, data residency, audit logging | — |

**Build order for developers** (Phase-0 needs come first): (1) content model + M1 core + exposure telemetry; (2) M2 session engine + calibration items; (3) M3-lite invitation + report skeleton; (4) M6 pipelines; (5) M4 planner + full M3 report for the Phase-1 launch build.

---

## 11. Testing and quality

### 11.1 Product QA
- Device matrix: minimum three low-end Android devices in the Telegram client, one iOS Telegram client, and the two dominant lab-desktop browsers.
- Script/locale QA: rendered-screenshot review per release in both Uzbek scripts and Russian (NFR-5).
- **Transliteration regression suite:** the Latin⇄Cyrillic exception table has automated tests; any new breakage found in content review becomes a test case before it becomes a fix.
- Network testing: throttled profiles (500 kbps, 3G-class latency, intermittent drops) on the assessment and report flows; lab-mode soak tests in Phase 2.

### 11.2 Psychometric QA (research lead owns; release-blocking where marked)
- Per-item statistics after Phase 0 and continuously: usage balance for forced-choice options, discrimination, response-latency anomalies, comprehension flags.
- Reliability target: each scored dimension reaches ≥ .70 (internal-consistency or IRT-based equivalent) by the end of Phase-1 data collection; dimensions failing after item revision are candidates for re-clustering, not for quiet retention.
- Structure check: planned analysis of whether the six-factor interest space holds in Uzbek data (MDS/EFA over triad-derived responses); re-derivation is the expected path (P-5).
- Fairness checks: differential-functioning flags across region, script of administration, and gender — *for detecting item bias only*, never for conditioning outputs (E-5). **Release-blocking:** no item flagged for comprehension failure or severe bias ships in a scored set.

### 11.3 Content QA
- Every wage figure and pathway fact carries `sources[]` and `last_verified`; publishing is blocked if `last_verified` > 6 months for wage/cost data. Quarterly review cadence for the full card set.
- Editorial checklist per card: no gender coding; vocational dignity parity (E-10); reading level; both scripts reviewed by a human, not only the transliterator.

### 11.4 Phase-0 pilot acceptance criteria (numbers are targets; revise only via Decisions Log)
- Session completion ≥ 70% of started chunks across all three sites.
- Median unique career cards viewed ≥ 12 per student during the pilot window.
- Parent join rate ≥ 30% in at least one site (proves the M3 flow can work; site variance is expected and informative).
- < 10% of calibration items flagged for comprehension failure in either script.
- ≥ 60% of the item pool survives statistical screening into the v1 scored set.

---

## 12. Publishing and launch

### Phase-1 launch checklist (B2C)
- Telegram Mini App published; web/PWA live at parity; both scripts + Russian verified in production.
- Privacy policy and consent flows live in uz and ru; data-residency verification documented; deletion flow tested end-to-end.
- Content floor met: ≥120 cards, ≥30 videos with low-bandwidth variants, ≥40 pathway templates, all within freshness rules.
- Support channel live (Telegram bot triage + human escalation); crash and analytics dashboards on; rollback plan rehearsed.
- Brand register check: local, practical, slightly commercial. If it reads like an NGO intervention, revise before launch (§14).

### Phase-2 launch checklist (B2B)
- School onboarding kit: advisor micro-training, class-code rostering guide, data-processing agreement template, MOU template.
- Lab mode field-tested in ≥2 real school labs; report templates validated with ≥2 practicing advisors against their actual reporting obligations.
- Pricing sheet approved; manual invoicing acceptable at start.
- The §5 access matrix and E-3 non-features communicated to school leadership in writing during onboarding — expectation-setting before the first request for rankings, not after.

---

## 13. Success metrics (targets provisional; confirm at each phase start via Decisions Log)

| Phase | Metric | Target |
|---|---|---|
| 1 | Activation: signups completing ≥1 assessment chunk | ≥ 50% |
| 1 | Exposure breadth: median unique cards viewed / 30 days | ≥ 15 |
| 1 | Full assessment completion among activated users | ≥ 60% |
| 1 | Parent join rate on invited families | ≥ 25% |
| 1 | D30 retention (any meaningful event) | ≥ 20% |
| 1→ | Psychometric: dimension reliability | ≥ .70 |
| 2 | Advisor weekly-active among licensed advisors | ≥ 60% |
| 2 | Generated advisor reports per class per term | ≥ 1 |
| 2 | School renewal intent at term end | ≥ 70% |
| 1→ | Follow-up response rate (6-month, via Telegram) | ≥ 30% |

---

## 14. Risks and failure modes (with standing mitigations)

**Deterministic labeling.** Authority pronouncements stick hard in this system; a label from "the program" becomes destiny. Mitigation is structural: P-4, E-1, E-2 — plural provisional outputs are the only outputs that exist.

**Test-gaming.** The moment results acquire stakes, children optimize them. Mitigation: E-7 low-stakes framing, no visible scores, behavioral signals that are hard to fake, and school-facing outputs that are aggregate.

**Being read as teaching children to defy parents.** One viral story of this shape damages trust broadly. Mitigation: M3's overlap-first framing, values vocabulary parents already hold, and E-4/E-6.

**Institutional misuse.** A director wants rankings; a district wants a sorting tool. Mitigation: E-3 as a product-level refusal (the export does not exist), plus written expectation-setting at onboarding (§12).

**Content staleness.** Wrong wage figures destroy credibility faster than any bug. Mitigation: freshness rules and publishing blocks (§11.3).

**Transliteration credibility.** Script errors read as carelessness to exactly the audience we need to trust us. Mitigation: exception table as a tested artifact, human review of both scripts (§7.3, §11.1).

**Telegram platform dependency.** Policy or reach changes are outside our control. Mitigation: full web/PWA parity from MVP (§7.1) — the Mini App is a distribution choice, not the architecture.

**Regulatory drift.** Decree implementation details may shift advisor duties or reporting formats. Mitigation: M5-F3 report templates are content-configurable, not hard-coded; maintain contact with pilot advisors as early-warning.

**Donor-project aesthetics.** If the brand smells like an NGO intervention, both parents and private schools discount it. Mitigation: brand register check in the launch checklist (§12); pricing exists (Phase 2) because paid things are taken seriously.

**Copying.** The assessment shell is copyable; the moat is the content library, exposure-conditioned data, local norms, and the validation loop (M1 + M6). Protect the moat by investing there first.

---

## 15. Glossary

| Term | Meaning |
|---|---|
| RIASEC / Holland codes | Six-factor Western interest model (Realistic, Investigative, Artistic, Social, Enterprising, Conventional). Internal scaffold only here. |
| DTM | State Testing Center; administers university entrance exams. |
| Fan bloki | Subject block chosen for university admission; effectively locks pathway options around grades 9–10. |
| Grant / kontrakt | State-funded vs. fee-paying university places; kontrakt cost is a major household expense. |
| Kasbga yo'naltirish | Career orientation — the mandated school function. |
| Mahalla | Neighborhood community; a real audience for family status decisions. |
| Usta | Master craftsman; anchor of the skilled-trade arc (apprentice → usta → own shop). |
| Tuman / viloyat | District / region — administrative units; tuman is the public-school sales unit in Phase 2. |
| uz-Latn / uz-Cyrl | Uzbek in Latin and Cyrillic scripts. Canonical authoring is uz-Latn; uz-Cyrl via transliteration + exception table. |
| Mini App | Telegram's embedded web-app format; primary consumer surface. |
| Lab mode | Batch, low-bandwidth, resumable operation on shared school computers. |
| Forced-choice / ipsative | Item format where the respondent chooses between options instead of rating agreement; counters acquiescence bias. |
| SJT | Situational judgment test — scenario-based items grounded in local settings. |
| No-signal profile | A student whose responses show no differentiated pattern; a flag for human conversation, not a category. |

---

## 16. Decisions log

Amendments to this document are recorded here. Seeded with decisions already in force:

| Date | ID | Decision | Rationale | Owner |
|---|---|---|---|---|
| 2026-08-25 | D-1 | RIASEC retained as internal scaffold only; re-derivation from local data planned. | GT-2, GT-3, P-5. | Research lead |
| 2026-08-25 | D-2 | Primary audience grades 7–9. | Subject-block lock-in at 9–10 (GT-4). | Product |
| 2026-08-25 | D-3 | Telegram Mini App primary consumer surface with full web parity. | GT-6; platform-dependency risk (§14). | Product/Eng |
| 2026-08-25 | D-4 | No ranked lists or individual score exports, permanently. | E-3; institutional-misuse risk. | Product |
| 2026-08-25 | D-5 | B2B beachhead: private schools; public scale via tuman-level deals. | GT-7; sales-cycle reality. | Product |
| 2026-08-25 | D-6 | Migration pathway content on consumer surface only. | E-9; institutional sensitivity. | Content |
| | | *Next entries appended here; each references the section(s) amended.* | | |
