<!-- GENERATED FILE - do not edit by hand.
     Source: docs/progress/data/*.json
     Regenerate: python3 tools/progress/progress.py build -->

# Requirement register

Every stable ID from the product framework and the mentorship concept, with its current state. As of 2026-08-26. [Back to the tracker](README.md).

**Contents:** [Ground truths](#ground-truths) · [Design principles](#design-principles) · [Users and roles](#users-and-roles) · [Modules](#modules) · [Functional requirements](#functional-requirements) · [Non-functional requirements](#non-functional-requirements) · [Ethics and data guardrails](#ethics-and-data-guardrails) · [Mentorship principles (concept)](#mentorship-principles-concept) · [Mentorship supply tiers (concept)](#mentorship-supply-tiers-concept) · [Mentorship formats (concept)](#mentorship-formats-concept) · [Mentorship safeguarding (concept)](#mentorship-safeguarding-concept)

## Ground truths

### `GT-1` The deciding unit is the household, not the child

Career choice is a family portfolio decision; social evaluation is a real utility term. A tool that only talks to the teenager gets overridden at the dinner table.

**Design implication.** The core deliverable is a negotiation artifact for the family (M3); the parent is a first-class user (R-2).

Leads to: `M3`, `R-2`, `P-3` · Source: framework §3

### `GT-2` Occupational awareness is narrow, and Soviet-inflected at the parent level

An interest inventory administered over unfamiliar occupations measures familiarity and prestige, not interest.

**Design implication.** Exposure (M1) precedes and feeds assessment (M2); exposure history is a first-class data stream.

Leads to: `M1`, `M2-F2`, `P-1` · Source: framework §3

### `GT-3` Self-report psychometrics degrade in predictable ways

Acquiescence bias, social desirability, unfamiliar Likert conventions, the instinct that every test has a correct answer, and a parent beside the child on a shared phone.

**Design implication.** Format-level countermeasures, not translation-level ones. No 'test' language, no visible score.

Leads to: `M2-F1`, `P-2`, `E-7` · Source: framework §3

### `GT-4` The prestige economy and the wage economy have diverged, and lock-in comes early

Medicine and law are oversubscribed relative to returns; subject-block choice around grades 9-10 forecloses paths before discovery normally happens.

**Design implication.** Primary audience grades 7-9; every recommendation carries a financing path and a subject-block plan; vocational routes get production parity.

Leads to: `M4`, `E-10`, `R-1` · Source: framework §3

### `GT-5` Constraints are structured by gender and geography

Some families cap a daughter's options by marriage timing; some professions are socially coded; mobility to Tashkent is a live constraint for regional children.

**Design implication.** Constraints enter only as explicit family-stated inputs, never as platform-encoded rules. The possibility space is expanded through content.

Leads to: `M2-F6`, `E-5`, `M1-F5` · Source: framework §3

### `GT-6` Infrastructure realities

Telegram is the distribution layer; cheap shared Android devices; thin regional bandwidth; two Uzbek scripts plus Russian; in-country hosting required; users are minors.

**Design implication.** Mini App primary with full web parity; single-source content with transliteration; low-bandwidth defaults; residency, consent and shared-device safety are architectural.

Leads to: `NFR-1`, `NFR-2`, `E-6`, `E-8` · Source: framework §3

### `GT-7` The state has already created our category

The September 2025 decree on mandatory school advisors turned a vague obligation into a named, staffed, under-tooled role.

**Design implication.** The B2B pitch is the advisor's operating system, not extra work. Private schools are the beachhead.

Leads to: `M5`, `R-4` · Source: framework §3

## Design principles

| ID | Rule | Status | Violation test |
|---|---|---|---|
| `P-1` | **Exposure before assessment** — The explorer feeds the instrument. | ➖ Nothing to check yet | Any interest item referencing an occupation the child has not been shown, or any child-facing item using bare occupation names. |
| `P-2` | **Behavior over self-description** — Choices, task performance and usage traces outrank agree/disagree statements. | ➖ Nothing to check yet | Likert agree-scales appearing in the child flow; a release where telemetry-derived signals are not part of the profile. |
| `P-3` | **The family is the user** — Three-sided product - child, parent, advisor - and the flagship output is a structured family conversation. | ➖ Nothing to check yet | A launch plan or report design in which the parent has no role, or in which the child's result is framed as a verdict to be delivered to the parent. |
| `P-4` | **Pathways, not labels** — Output is always plural, provisional and concrete: next subject block, next course, next cost, plan B. | ➖ Nothing to check yet | Any UI surface showing a type label, a single recommendation, or a score; fewer than three pathways in any generated report. |
| `P-5` | **Local validity is built, not imported** — RIASEC is the starting hypothesis; every item is instrumented; the interest structure is re-derived from Uzbek data. | ➖ Nothing to check yet | Shipping item changes without telemetry; treating the Holland hexagon as settled truth in scoring code; hard-coding weights no one can trace to data. |

## Users and roles

| ID | Role | First phase | Description |
|---|---|---|---|
| `R-1` | Student | 0 | Grades 7-9 primary, 10-11 secondary. Uses explorer, assessment, pathway planner. |
| `R-2` | Parent / guardian | 0 | Runs the parallel parent instrument, receives the family congruence report, holds consent. |
| `R-3` | Family broker (optional) | 1 | The relative whose opinion actually carries. Invited as a viewer of the family report. |
| `R-4` | School advisor | 2 | The decree-mandated role and primary B2B user: aggregates, one-at-a-time summaries, report generation, parent-meeting log. |
| `R-5` | School administrator / director | 2 | The buyer. Sees aggregate analytics only. |
| `R-6` | Content editor (internal) | 0 | Maintains career cards, pathway templates, media, translations and verification dates. |
| `R-7` | Research lead (internal) | 0 | Owns the item bank, telemetry analysis, norms and validation studies. |

## Modules

| ID | Module | Phase | Status | Features |
|---|---|---|---|---|
| `M1` | Occupation Explorer | 0 | ⬜ Not started | 0/5 done · 0% |
| `M2` | Assessment Suite | 0 | ⬜ Not started | 0/6 done · 0% |
| `M3` | Family Module | 0 | ⬜ Not started | 0/5 done · 0% |
| `M4` | Pathway Planner | 1 | ⬜ Not started | 0/4 done · 0% |
| `M5` | School Layer | 2 | ⬜ Not started | 0/5 done · 0% |
| `M6` | Research Layer | 0 | ⬜ Not started | 0/6 done · 0% |
| `M7` | Mentorship (deferred by design) | 2 | 💤 Deferred | 0/0 done · 0% |

- **`M1` Occupation Explorer** — The content engine and the moat: builds occupational awareness, supplies the assessment's item pool, logs exposure.
- **`M2` Assessment Suite** — Produces a student profile from behavior and structured choice rather than self-description.
- **`M3` Family Module** — Converts the child's profile and the parents' aspirations into a structured negotiation, not a confrontation.
- **`M4` Pathway Planner** — Turns profiles and constraints into named, financed, plural routes.
- **`M5` School Layer** — The advisor's operating system, including the reporting the role already owes.
- **`M6` Research Layer** — Turns usage into validity: item statistics, local norms, and the evidence base Phase 3 requires.
- **`M7` Mentorship (deferred by design)** — Async Q&A first, then group formats. The only MVP-era dependency is that career cards can host threaded content later.

## Functional requirements

| ID | Requirement | Phase | MVP | Status | Owner | Traces to | Links |
|---|---|---|---|---|---|---|---|
| `M1-F1` | **Career card model** — Every card carries titles and body in uz-Latn/uz-Cyrl/ru, cluster tags, daily reality, entry routes, subject-block mapping, cost band, regional wage ranges at years 1/5/10, geography of demand, related cards, media refs, sources[] and last_verified. | 0 | yes | ⬜ Not started | Engineering | — | — |
| `M1-F2` | **Video content** — 60-90 second 'bir kun' day-in-the-life videos with real people; every video has a low-bandwidth variant (audio + stills). | 0 | yes | ⬜ Not started | Content | — | — |
| `M1-F3` | **Exposure logging** — Every card view logs dwell time, replays, returns and completion; this stream gates M2 scoring eligibility and feeds M6. | 0 | yes | ⬜ Not started | Engineering | `P-1` | [#2](https://github.com/davletovb/ufq/issues/2) |
| `M1-F4` | **Browse and search** — Browse and search by cluster, tag and free text, in all three locales and both scripts. | 0 | yes | ⬜ Not started | Engineering | — | — |
| `M1-F5` | **Content policy (enforced at review)** — Deliberate over-indexing on regional role models, women in nontraditional fields shown matter-of-factly, dignified skilled-trade arcs. No gender-coded card copy. | 0 | yes | ⬜ Not started | Content | `GT-5`, `E-10` | — |
| `M2-F1` | **Item formats** — Forced-choice triads over illustrated activities, situational-judgment items in local scenes, performance mini-tasks with timing, an 8-card values sort, and constraints intake. | 0 | yes | ⬜ Not started | Research | `P-2` | — |
| `M2-F2` | **Exposure rule** — Interest items reference only activities or occupations already surfaced via M1. Bare occupation names are forbidden in the child flow. | 0 | yes | ⬜ Not started | Research | `P-1` | — |
| `M2-F3` | **Session engine** — 10-15 minute resumable chunks with server-side state; a full profile accumulates across sessions. Designed for shared devices and 45-minute lessons. | 0 | yes | ⬜ Not started | Engineering | `NFR-6` | — |
| `M2-F4` | **Scoring v1** — Internal vectors only - interest, values, aptitude, constraints. Scoring must be traceable to item data; weights are configuration, not constants buried in code. | 1 | yes | ⬜ Not started | Research | `P-5` | — |
| `M2-F5` | **Child-facing output** — Playful, non-evaluative feedback plus unlocked pathway suggestions. No scores, no types, no pass/fail. | 0 | yes | ⬜ Not started | Product | `E-2`, `E-7` | — |
| `M2-F6` | **Constraints intake** — Explicit family-context questions - budget band, mobility, non-negotiables - stored as stated constraints and used by M4. Never inferred. | 0 | yes | ⬜ Not started | Product | `GT-5`, `E-5` | — |
| `M3-F1` | **Parent instrument** — About 10 minutes: aspiration picks, non-negotiables, an occupational-map exercise surfacing outdated assumptions gently, and flexibility items. | 0 | yes | ⬜ Not started | Research | — | — |
| `M3-F2` | **Invitation flow** — Child or advisor invites the parent by Telegram deep link; parent onboarding completes in one sitting on a low-end phone. | 0 | yes | ⬜ Not started | Engineering | — | — |
| `M3-F3` | **Family congruence report** — Where child profile and parent aspirations overlap, where they diverge (framed neutrally), three concrete pathways inside the overlap, and a conversation guide. | 1 | yes | ⬜ Not started | Product | `P-3`, `P-4` | — |
| `M3-F4` | **Third seat** — Optional invited viewer for the family broker who actually moves the decision. | 1 | yes | ⬜ Not started | Product | `R-3` | — |
| `M3-F5` | **Hard privacy rules** — Parents see fit and options, never the child's item-level answers. All child-visible output must be safe if seen by a parent on a shared device. | 0 | yes | ⬜ Not started | Engineering | `E-4`, `E-6` | — |
| `M4-F1` | **Pathway template model** — Target occupations, education step, subject block and exam requirements, cost band, financing options, timeline, plausible first job, plan-B link, region variants, surface flags. | 1 | yes | ⬜ Not started | Content | — | — |
| `M4-F2` | **Matching engine v1** — Rules and template matching over profile x constraints. No ML in MVP; every match must be explainable in one sentence. | 1 | yes | ⬜ Not started | Engineering | — | — |
| `M4-F3` | **Plurality rule** — Every generated plan contains at least three routes, always including at least one non-university route where constraints allow. | 1 | yes | ⬜ Not started | Product | `P-4`, `E-1` | — |
| `M4-F4` | **Surface flags** — Migration-related pathway content renders on the consumer surface only; the school-facing surface receives the softened variant. | 1 | yes | ⬜ Not started | Engineering | `E-9` | — |
| `M5-F1` | **Rostering** — Class codes; no school-side IT integration required in Phase 2. | 2 | — | ⬜ Not started | Engineering | — | — |
| `M5-F2` | **Advisor dashboard** — Class-level aggregate heatmaps, no-signal flags for profiles needing a human conversation, one-at-a-time student summaries with access logging. | 2 | — | ⬜ Not started | Engineering | `E-3`, `NFR-8` | — |
| `M5-F3` | **Report generator** — One-click generation of the career-orientation documentation the advisor role requires, from aggregates. Templates are content-configurable, not hard-coded. | 2 | — | ⬜ Not started | Product | — | — |
| `M5-F4` | **Parent-meeting log** — Tied to family reports, with the family's consent. | 2 | — | ⬜ Not started | Engineering | — | — |
| `M5-F5` | **Lab mode** — Batch student sessions on shared lab machines: low bandwidth, resumable, queue-and-sync tolerant of connectivity drops. | 2 | — | ⬜ Not started | Engineering | `NFR-6` | — |
| `M5-F6` | **Explicit non-features** — No ranked lists, no individual score exports, no class-results spreadsheet. Refused at the product level, permanently. | 2 | — | ➖ Nothing to check yet | Product | `E-3` | — |
| `M6-F1` | **Telemetry schema** — Exposure events, item responses with latency, session events - versioned, and present from the first pilot build. | 0 | yes | ⬜ Not started | Engineering | `P-5` | [#2](https://github.com/davletovb/ufq/issues/2) |
| `M6-F2` | **Item bank and statistics pipeline** — Per-item statistics: usage balance for forced-choice, discrimination, latency flags, comprehension flags. | 1 | yes | ⬜ Not started | Research | — | — |
| `M6-F3` | **Norms jobs** — Norms by cohort, region, and language/script of administration. | 1 | yes | ⬜ Not started | Research | — | — |
| `M6-F4` | **Structure analysis readiness** — Export shapes suitable for testing whether the six-factor interest structure holds locally, with re-clustering as the expected outcome rather than a failure. | 1 | yes | ⬜ Not started | Research | `P-5` | — |
| `M6-F5` | **Follow-up scheduler** — 6- and 18-month follow-ups via Telegram (choice made, satisfaction, persistence) - the criterion-validation loop. | 1 | yes | ⬜ Not started | Engineering | — | — |
| `M6-F6` | **De-identified research exports** — Research exports are de-identified only. | 0 | yes | ⬜ Not started | Engineering | `E-8` | — |

## Non-functional requirements

| ID | Requirement | Phase | MVP | Status | Owner | Traces to | Links |
|---|---|---|---|---|---|---|---|
| `NFR-1` | **Device floor** — Fully usable on Android 8 / 2 GB RAM class devices inside the Telegram webview, and in low-end desktop browsers for lab mode. | 0 | — | ⬜ Not started | Engineering | `GT-6` | — |
| `NFR-2` | **Payload budget** — Mini App core interactive bundle at or under ~300 KB gzipped; media lazy-loaded; usable on a ~500 kbps connection. | 0 | — | ⬜ Not started | Engineering | `GT-6` | — |
| `NFR-3` | **Performance** — p95 API latency under 500 ms in-country; assessment interactions render feedback in under 100 ms locally. | 1 | — | ⬜ Not started | Engineering | — | — |
| `NFR-4` | **Availability** — At least 99.5% in Phase 1, with degraded-mode reads of cached explorer content when the API is unreachable. | 1 | — | ⬜ Not started | Engineering | — | — |
| `NFR-5` | **Locale parity** — 100% of UI strings in uz-Latn, uz-Cyrl and ru at every release, with per-script rendered-screenshot QA. | 0 | — | ⬜ Not started | Content | `GT-6` | — |
| `NFR-6` | **Resumability** — Any session chunk survives connection loss and device handoff without data loss. | 0 | — | ⬜ Not started | Engineering | — | — |
| `NFR-7` | **Accessibility and literacy** — Adjustable text size, icon-supported navigation, reading level calibrated in Phase 0 for grade 7. | 0 | — | ⬜ Not started | Product | — | — |
| `NFR-8` | **Auditability** — Every advisor access to individual data is logged and reviewable. | 2 | — | ⬜ Not started | Engineering | `E-3` | — |

## Ethics and data guardrails

| ID | Rule | Status | Violation test |
|---|---|---|---|
| `E-1` | **Plural, provisional outputs** — Every report contains at least three pathways with explicitly provisional framing. No single verdicts, ever. | ➖ Nothing to check yet | A generated report with fewer than three pathways, or output phrased as a settled recommendation. |
| `E-2` | **No type labels** — RIASEC and successor structures are internal vocabulary only; no type labels in child- or parent-facing UI. | ➖ Nothing to check yet | Any RIASEC letter, code, or type name reachable from a child or parent surface. |
| `E-3` | **No ranked lists or individual score exports** — A product-level refusal designed to precede institutional requests for it. Advisor access to individuals is one-at-a-time and logged. | ➖ Nothing to check yet | Any ordering of students by a score-derived value, or any export containing individual scores. |
| `E-4` | **Parents see congruence and options, never item-level answers** — The parent view is derived, never raw. | ➖ Nothing to check yet | Any parent-reachable response containing per-item child responses. |
| `E-5` | **No gender- or region-conditional logic** — Constraints enter scoring and matching only as explicit family-stated inputs. | ➖ Nothing to check yet | Any branch in scoring or matching code keyed on gender or region rather than on a stated constraint. |
| `E-6` | **Shared-device safety** — Every child-visible screen must be safe if seen by a parent. | ➖ Nothing to check yet | A child-facing screen whose disclosure to a parent would harm the child. |
| `E-7` | **Low-stakes framing** — No scores, no pass/fail, game language not exam language. Both an ethics rule and the anti-gaming strategy. | ➖ Nothing to check yet | The word 'test'/'imtihon' or any visible score in the child flow. |
| `E-8` | **Consent and data rights** — Parental consent plus child assent, deletion on request, de-identified research exports, aggregate-only publication. | ➖ Nothing to check yet | Any data collection before a recorded consent, or an export carrying identifiers. |
| `E-9` | **Migration content surface rule** — Migration content appears on the consumer surface only; the school surface carries the softened variant. | ➖ Nothing to check yet | Migration-flagged content rendered on a school-facing surface. |
| `E-10` | **Vocational dignity parity** — Trades and certificate routes get the same content production value and matching weight as university routes. | ➖ Nothing to check yet | A content batch or matching weight set in which vocational routes are systematically thinner. |

## Mentorship principles (concept)

| ID | Rule | Status | Violation test |
|---|---|---|---|
| `MP-1` | **Broker provisioning** — The module's core purpose is supplying broker-poor families with a credible third voice; family-facing formats are the point, not an add-on. | 📐 Not yet binding | A roadmap in which family-visible formats trail child-only formats indefinitely. |
| `MP-2` | **Biographical matching** — Students are routed to mentors by pathway interest plus biographical proximity, never by assessment profile. | 📐 Not yet binding | Any matching logic that consumes ProfileVector data. |
| `MP-3` | **Show, decode, vouch - never prescribe** — The channel rule. Formats are structured so the mentor narrates their own path and decodes the terrain; prescription is out of scope. | 📐 Not yet binding | Session formats that ask mentors 'what should this student do?'; unscripted open advice formats for minors. |
| `MP-4` | **Family-visible by default** — Family-visible mentorship is both what parents expect and the safeguarding-correct default. | 📐 Not yet binding | Any early-phase format a parent cannot observe or review. |
| `MP-5` | **Curation, not marketplace** — Mentors are recruited, vetted, trained and few. One flaky or predatory mentor costs more than fifty good ones earn. | 📐 Not yet binding | Open sign-up flows; mentor counts as a vanity metric. |
| `MP-6` | **Observable formats only, for minors** — No private adult-minor channels in any early phase; all interaction happens in logged, observable formats. | 📐 Not yet binding | Any DM-like capability shipping before the T-6 preconditions are met. |
| `MP-7` | **Mentorship compounds into content** — Every mentor interaction should leave a permanent artifact that feeds the M1 content moat. | 📐 Not yet binding | Live formats with no capture-and-promote pipeline behind them. |

## Mentorship supply tiers (concept)

| ID | Requirement | Phase | MVP | Status | Owner | Traces to | Links |
|---|---|---|---|---|---|---|---|
| `MS-1` | **Mentor-as-content** — Anyone filmed for a 'bir kun' video. Proof function at zero marginal cost; filming is the onboarding ritual. | 0 | — | 📐 Concept | — | — | — |
| `MS-2` | **Near-peers (workhorse tier)** — University students 3-6 years older from the same region: relatable proof plus decoding at scale, and lower safeguarding risk. | 3 | — | 📐 Concept | — | — | — |
| `MS-3` | **Professionals** — Working adults across pathways. Time-poor, so deploy in one-to-many formats rather than 1:1. | 2 | — | 📐 Concept | — | — | — |
| `MS-4` | **Ustalar** — Vocational masters. Must be recruited deliberately - vocational dignity parity fails by default otherwise. | 2 | — | 📐 Concept | — | `E-10` | — |
| `MS-5` | **Diaspora professionals** — Uzbeks abroad: decoding for study and work-abroad routes, async-friendly. Migration-adjacent content follows the E-9 surface rule. | 2 | — | 📐 Concept | — | `E-9` | — |

## Mentorship formats (concept)

| ID | Requirement | Phase | MVP | Status | Owner | Traces to | Links |
|---|---|---|---|---|---|---|---|
| `T-1` | **Mentor as content** — Filmed 'bir kun' profiles; interview overflow becomes a pre-loaded Q&A bank under each card. No safeguarding surface because there is no interaction. | 0 | — | 📐 Concept | — | — | — |
| `T-2` | **Async public Q&A under career cards** — Students ask under a card, vetted mentors answer, everything public and moderated before publication. Best answers are promoted into permanent card content. | 2 | — | 📐 Concept | — | — | — |
| `T-3` | **School group sessions** — One mentor, one class or interest group, hosted and scheduled through the school advisor. One mentor-hour serves 25+ students. | 2 | — | 📐 Concept | — | — | — |
| `T-4` | **Path cohorts** — Six to ten students on the same pathway, one mentor, four semi-scripted sessions. The script is the channel-rule enforcement mechanism. | 3 | — | 📐 Concept | — | — | — |
| `T-5` | **Family consultations** — The mentor joins the family's congruence conversation as the credible third voice - broker provisioning, operationalized. | 3 | — | 📐 Concept | — | `MP-1` | — |
| `T-6` | **True 1:1** — Only much later, for older students: vetted, logged, gender-matched, parent-consented, and only by an explicit Decisions Log entry. | 3 | — | 📐 Concept | — | — | — |

## Mentorship safeguarding (concept)

| ID | Rule | Status | Violation test |
|---|---|---|---|
| `ME-1` | **No private adult-minor channels** — No DM-like capability exists before T-6, which itself requires preconditions plus an explicit Decisions Log entry. | 📐 Not yet binding | Any direct-message capability between a mentor and a minor. |
| `ME-2` | **Observable and logged** — Every live format is recorded or minuted, parent-visible by default, and auditable. | 📐 Not yet binding | A live session with no record and no parent visibility. |
| `ME-3` | **Channel rule enforced structurally** — Formats are scripted or moderated such that prescription has no slot; violations are a removal offense. | 📐 Not yet binding | An unscripted, unmoderated advice format reaching minors. |
| `ME-4` | **No solicitation, no off-platform contact, no side payments** — Mentors may not sell to platform families, take contact details, or accept payment outside the platform. Signed at entry. | 📐 Not yet binding | Any surface that exposes contact details, or an unmoderated channel where solicitation can occur. |
| `ME-5` | **Vetting before live contact** — The vetting pipeline is mandatory and async probation precedes any live format. | 📐 Not yet binding | A mentor reaching a live format without a completed probation record. |
| `ME-6` | **Gender-matching for live proximity formats** — A parent-selectable default for T-4/T-5/T-6. A family consent choice about who is in the room - explicitly distinct from E-5, which forbids gender-conditional logic in scoring and matching. | 📐 Not yet binding | Gender-matching logic leaking into pathway or scoring code rather than staying in session composition. |
| `ME-7` | **Incident handling** — Zero-tolerance removal for safeguarding or solicitation violations; incident log reviewed by product leadership; schools notified where school-hosted. | 📐 Not yet binding | No reachable reporting mechanism for students, parents and advisors. |
| `ME-8` | **Minimal data exposure** — Mentors operate on pathway interest and context, never on profiles. | 📐 Not yet binding | Any mentor-reachable response containing ProfileVector or item-level data. |
| `ME-9` | **Volunteer/paid clarity** — Each tier's compensation status is explicit and public to mentors; ambiguity breeds the solicitation behavior ME-4 bans. | 📐 Not yet binding | A recruited tier with no stated compensation status. |
