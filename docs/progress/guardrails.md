<!-- GENERATED FILE - do not edit by hand.
     Source: docs/progress/data/*.json
     Regenerate: python3 tools/progress/progress.py build -->

# Guardrail board

Binding rules and the concrete symptom that says we are drifting. A guardrail is never “done”; it is upheld, at risk, or violated. Move a row to ⚠️ or 🚨 in the same pull request that introduces the risk.

As of 2026-08-26. [Back to the tracker](README.md).

**Binding:** ➖ 16 nothing to check yet

## Design principles

| ID | Guardrail | Status | Violation test | Governs | Source |
|---|---|---|---|---|---|
| `P-1` | **Exposure before assessment** — The explorer feeds the instrument. | ➖ Nothing to check yet | Any interest item referencing an occupation the child has not been shown, or any child-facing item using bare occupation names. | `M1-F3`, `M2-F2` | framework §4 |
| `P-2` | **Behavior over self-description** — Choices, task performance and usage traces outrank agree/disagree statements. | ➖ Nothing to check yet | Likert agree-scales appearing in the child flow; a release where telemetry-derived signals are not part of the profile. | `M2-F1`, `M6-F1` | framework §4 |
| `P-3` | **The family is the user** — Three-sided product - child, parent, advisor - and the flagship output is a structured family conversation. | ➖ Nothing to check yet | A launch plan or report design in which the parent has no role, or in which the child's result is framed as a verdict to be delivered to the parent. | `M3-F3`, `R-2` | framework §4 |
| `P-4` | **Pathways, not labels** — Output is always plural, provisional and concrete: next subject block, next course, next cost, plan B. | ➖ Nothing to check yet | Any UI surface showing a type label, a single recommendation, or a score; fewer than three pathways in any generated report. | `M4-F3`, `E-1`, `E-2` | framework §4 |
| `P-5` | **Local validity is built, not imported** — RIASEC is the starting hypothesis; every item is instrumented; the interest structure is re-derived from Uzbek data. | ➖ Nothing to check yet | Shipping item changes without telemetry; treating the Holland hexagon as settled truth in scoring code; hard-coding weights no one can trace to data. | `M6-F2`, `M6-F4`, `M2-F4` | framework §4 |

## Ethics and data guardrails

| ID | Guardrail | Status | Violation test | Governs | Source |
|---|---|---|---|---|---|
| `E-1` | **Plural, provisional outputs** — Every report contains at least three pathways with explicitly provisional framing. No single verdicts, ever. | ➖ Nothing to check yet | A generated report with fewer than three pathways, or output phrased as a settled recommendation. | `M4-F3`, `M3-F3` | framework §9 |
| `E-2` | **No type labels** — RIASEC and successor structures are internal vocabulary only; no type labels in child- or parent-facing UI. | ➖ Nothing to check yet | Any RIASEC letter, code, or type name reachable from a child or parent surface. | `M2-F5` | framework §9 |
| `E-3` | **No ranked lists or individual score exports** — A product-level refusal designed to precede institutional requests for it. Advisor access to individuals is one-at-a-time and logged. | ➖ Nothing to check yet | Any ordering of students by a score-derived value, or any export containing individual scores. | `M5-F6`, `M5-F2`, `NFR-8` | framework §9 |
| `E-4` | **Parents see congruence and options, never item-level answers** — The parent view is derived, never raw. | ➖ Nothing to check yet | Any parent-reachable response containing per-item child responses. | `M3-F5` | framework §9 |
| `E-5` | **No gender- or region-conditional logic** — Constraints enter scoring and matching only as explicit family-stated inputs. | ➖ Nothing to check yet | Any branch in scoring or matching code keyed on gender or region rather than on a stated constraint. | `M2-F6`, `M4-F2` | framework §9 |
| `E-6` | **Shared-device safety** — Every child-visible screen must be safe if seen by a parent. | ➖ Nothing to check yet | A child-facing screen whose disclosure to a parent would harm the child. | `M3-F5` | framework §9 |
| `E-7` | **Low-stakes framing** — No scores, no pass/fail, game language not exam language. Both an ethics rule and the anti-gaming strategy. | ➖ Nothing to check yet | The word 'test'/'imtihon' or any visible score in the child flow. | `M2-F5` | framework §9 |
| `E-8` | **Consent and data rights** — Parental consent plus child assent, deletion on request, de-identified research exports, aggregate-only publication. | ➖ Nothing to check yet | Any data collection before a recorded consent, or an export carrying identifiers. | `M6-F6` | framework §9 |
| `E-9` | **Migration content surface rule** — Migration content appears on the consumer surface only; the school surface carries the softened variant. | ➖ Nothing to check yet | Migration-flagged content rendered on a school-facing surface. | `M4-F4` | framework §9 |
| `E-10` | **Vocational dignity parity** — Trades and certificate routes get the same content production value and matching weight as university routes. | ➖ Nothing to check yet | A content batch or matching weight set in which vocational routes are systematically thinner. | `M1-F5`, `M4-F3` | framework §9 |

## Product-level refusals

| ID | Guardrail | Status | Violation test | Governs | Source |
|---|---|---|---|---|---|
| `M5-F6` | **Explicit non-features** — No ranked lists, no individual score exports, no class-results spreadsheet. Refused at the product level, permanently. | ➖ Nothing to check yet | Any endpoint, export, or dashboard view that returns students ordered by any score-derived value. | — | framework §6 M5-F6 |

## Mentorship (concept, not yet binding)

From the mentorship concept document. These become binding only when a slice graduates into the framework's Decisions Log.

| ID | Guardrail | Status | Violation test | Governs | Source |
|---|---|---|---|---|---|
| `MP-1` | **Broker provisioning** — The module's core purpose is supplying broker-poor families with a credible third voice; family-facing formats are the point, not an add-on. | 📐 Not yet binding | A roadmap in which family-visible formats trail child-only formats indefinitely. | — | mentorship §4 |
| `MP-2` | **Biographical matching** — Students are routed to mentors by pathway interest plus biographical proximity, never by assessment profile. | 📐 Not yet binding | Any matching logic that consumes ProfileVector data. | — | mentorship §4 |
| `MP-3` | **Show, decode, vouch - never prescribe** — The channel rule. Formats are structured so the mentor narrates their own path and decodes the terrain; prescription is out of scope. | 📐 Not yet binding | Session formats that ask mentors 'what should this student do?'; unscripted open advice formats for minors. | — | mentorship §4 |
| `MP-4` | **Family-visible by default** — Family-visible mentorship is both what parents expect and the safeguarding-correct default. | 📐 Not yet binding | Any early-phase format a parent cannot observe or review. | — | mentorship §4 |
| `MP-5` | **Curation, not marketplace** — Mentors are recruited, vetted, trained and few. One flaky or predatory mentor costs more than fifty good ones earn. | 📐 Not yet binding | Open sign-up flows; mentor counts as a vanity metric. | — | mentorship §4 |
| `MP-6` | **Observable formats only, for minors** — No private adult-minor channels in any early phase; all interaction happens in logged, observable formats. | 📐 Not yet binding | Any DM-like capability shipping before the T-6 preconditions are met. | — | mentorship §4 |
| `MP-7` | **Mentorship compounds into content** — Every mentor interaction should leave a permanent artifact that feeds the M1 content moat. | 📐 Not yet binding | Live formats with no capture-and-promote pipeline behind them. | — | mentorship §4 |
| `ME-1` | **No private adult-minor channels** — No DM-like capability exists before T-6, which itself requires preconditions plus an explicit Decisions Log entry. | 📐 Not yet binding | Any direct-message capability between a mentor and a minor. | — | mentorship §8 |
| `ME-2` | **Observable and logged** — Every live format is recorded or minuted, parent-visible by default, and auditable. | 📐 Not yet binding | A live session with no record and no parent visibility. | — | mentorship §8 |
| `ME-3` | **Channel rule enforced structurally** — Formats are scripted or moderated such that prescription has no slot; violations are a removal offense. | 📐 Not yet binding | An unscripted, unmoderated advice format reaching minors. | — | mentorship §8 |
| `ME-4` | **No solicitation, no off-platform contact, no side payments** — Mentors may not sell to platform families, take contact details, or accept payment outside the platform. Signed at entry. | 📐 Not yet binding | Any surface that exposes contact details, or an unmoderated channel where solicitation can occur. | — | mentorship §8 |
| `ME-5` | **Vetting before live contact** — The vetting pipeline is mandatory and async probation precedes any live format. | 📐 Not yet binding | A mentor reaching a live format without a completed probation record. | — | mentorship §8 |
| `ME-6` | **Gender-matching for live proximity formats** — A parent-selectable default for T-4/T-5/T-6. A family consent choice about who is in the room - explicitly distinct from E-5, which forbids gender-conditional logic in scoring and matching. | 📐 Not yet binding | Gender-matching logic leaking into pathway or scoring code rather than staying in session composition. | — | mentorship §8 |
| `ME-7` | **Incident handling** — Zero-tolerance removal for safeguarding or solicitation violations; incident log reviewed by product leadership; schools notified where school-hosted. | 📐 Not yet binding | No reachable reporting mechanism for students, parents and advisors. | — | mentorship §8 |
| `ME-8` | **Minimal data exposure** — Mentors operate on pathway interest and context, never on profiles. | 📐 Not yet binding | Any mentor-reachable response containing ProfileVector or item-level data. | — | mentorship §8 |
| `ME-9` | **Volunteer/paid clarity** — Each tier's compensation status is explicit and public to mentors; ambiguity breeds the solicitation behavior ME-4 bans. | 📐 Not yet binding | A recruited tier with no stated compensation status. | — | mentorship §8 |
