# Mentorship System (Ustoz–Shogird)
## Concept & Design Document — Companion to the Platform Source of Truth

| Field | Value |
|---|---|
| Version | 0.1 (concept draft for review) |
| Date | 25 August 2026 |
| Status | **Concept — not yet binding.** Elaborates module M7 of the main framework document. Nothing here is implemented until selected items graduate into the Source of Truth via its Decisions Log (§16 there). |
| Audience | Product, project management, developers, content team, research lead |
| ID conventions | Principles `MP-n`, supply tiers `MS-n`, formats `T-n`, guardrails `ME-n`. References to `GT-n`, `P-n`, `E-n`, `M-n` point to the main framework document. |

---

## 1. Purpose of this document

The main framework deliberately deferred mentorship (M7) because supply-side bootstrapping is hard and the safeguarding stakes are high. This document does the thinking that deferral bought: what a mentor actually *is* inside this system, which formats are viable in this market, in what order, and under what guardrails. It is a decision-support document. When the team approves a slice of it, that slice is rewritten as binding requirements in the Source of Truth and logged there.

---

## 2. The role of a mentor in this system

In the Western platforms the word comes from, a mentor is a guide — a wiser individual helping a younger individual self-actualize. That definition mis-imports here, because in this system guidance is already distributed across actors:

| Actor | What it supplies |
|---|---|
| Platform (M1–M2) | Exposure to the occupational landscape; behavior-based profile |
| Family (M3) | The actual decision, and its legitimacy |
| Advisor (M5) | Institutional shepherding and the mandated process |
| **Mentor (M7)** | **What none of the above can supply — three functions below** |

**Function 1 — Proof.** A career card claims a path exists; a mentor is a living instance of it. In a low-occupational-awareness environment (GT-2) this evidentiary function is primary, and it is strongest when the mentor is *biographically proximate*: "did IT from Namangan with no money" is worth ten Tashkent-elite mentors to a rural student. Design consequence: matching is biographical (region, constraint profile, starting point), not psychometric (MP-2).

**Function 2 — Decoding.** The formal pathway is legible — DTM, subject blocks, kontrakt. The real pathway runs through tacit knowledge: which certificates employers actually respect, how hiring actually happens, how tanish-bilish works when you don't have it, how someone actually gets from a viloyat to IT Park. Career cards cannot encode this well because it is informal-economy knowledge (GT-4). The mentor is the interface to it.

**Function 3 — Legitimation.** The culturally decisive function, and the one the module should be built around. The framework already recognizes the family broker (R-3) — the relative whose word moves parents. Broker access is unevenly distributed: connected families have one; most families do not. Mentorship here is best conceived as **broker provisioning** — supplying broker-poor families with a credible outside adult whose authority transfers to the parents (GT-1). Consequence: the highest-leverage mentor conversation may not be with the child at all; it may be with the family, around the congruence report (T-5). It is also, plausibly, the first thing parents in this market would pay for — access to a credible person, not software.

---

## 3. Framing: ustoz–shogird, not "mentoring"

The word "mentoring" reads as donor-program vocabulary (see the donor-aesthetics risk, main §14). The system should indigenize the relationship as **ustoz–shogird**.

**What the frame buys.** Parental trust and gravitas; a recruitment register that actually works here — ustozlik framed as an honor; giving back framed through hashar or sadaqa jariya for volunteers; identity maintenance for diaspora professionals.

**What the frame risks.** Ustoz authority slides naturally into verdict-issuing, and an ustoz pronouncing "become a doctor" is exactly as deterministic as the type label E-1 exists to prevent — arguably worse, because it arrives with personal authority. The mitigation is the **channel rule** (MP-3): mentors show their own path, decode paths, and vouch for feasibility — they never prescribe. Semi-scripted formats enforce this far more reliably than a guidelines PDF (see T-4 and Appendix A).

---

## 4. Design principles for mentorship

**MP-1 — Broker provisioning.** The module's core purpose is supplying broker-poor families with a credible third voice; family-facing formats are not an add-on but the point.
*Violation test:* a roadmap in which family-visible formats trail child-only formats indefinitely.

**MP-2 — Biographical matching.** Students are routed to mentors by pathway interest plus biographical proximity (region, starting constraints), never by assessment profile. The chain is: assessment → pathways (M4) → mentors who walked those pathways.
*Violation test:* any matching logic that consumes `ProfileVector` data.

**MP-3 — Show, decode, vouch — never prescribe.** The channel rule. Formats are structured so the mentor narrates their own path and decodes the terrain; prescription is out of scope and moderated out.
*Violation test:* session formats that ask mentors "what should this student do?"; unscripted open advice formats for minors.

**MP-4 — Family-visible by default.** Western mentorship prizes mentee confidentiality; here, family-visible mentorship is both what parents expect and the safeguarding-correct default. Safety and culture align — take the gift.
*Violation test:* any early-phase format a parent cannot observe or review.

**MP-5 — Curation, not marketplace.** Supply is scarce and variable; in a low-trust market one flaky or predatory mentor costs more than fifty good ones earn. Mentors are recruited, vetted, trained, and few — not self-listed.
*Violation test:* open sign-up flows; mentor counts as a vanity metric.

**MP-6 — Observable formats only, for minors.** No private adult–minor channels in any early phase; all interaction happens in logged, observable formats (see ME-1, ME-2).
*Violation test:* any DM-like capability shipping before the T-6 preconditions in §10 are met.

**MP-7 — Mentorship compounds into content.** Every mentor interaction should leave a permanent artifact: filmed profiles, Q&A answers promoted into career cards, verification badges. The mentorship program feeds the content moat (M1), and this knowledge base does not currently exist in Uzbek anywhere.
*Violation test:* live formats with no capture-and-promote pipeline behind them.

---

## 5. Supply model

### 5.1 Supply tiers

| ID | Tier | Who | Role | Notes |
|---|---|---|---|---|
| MS-1 | Mentor-as-content | Anyone filmed for a "bir kun" video | Proof function at zero marginal cost | Filming is the onboarding ritual; interview answers seed pre-loaded Q&A before anything is live. |
| MS-2 | Near-peers (**workhorse tier**) | University students 3–6 years older, same region | Relatable proof + decoding at scale | Recruitable with stipends and status; lower safeguarding risk profile; conveniently builds the university relationships Phase 3 needs. |
| MS-3 | Professionals | Working adults across pathways | Decoding + legitimation in group formats | Time-poor; deploy in 1:many formats (T-3, T-4), not 1:1. |
| MS-4 | Ustalar | Vocational masters | Proof + legitimation for trade routes | Must be recruited deliberately — vocational dignity parity (E-10) fails by default otherwise. |
| MS-5 | Diaspora professionals | Uzbeks abroad | Decoding for study/work-abroad routes; async-friendly | Identity-maintenance framing; time zones favor T-2 async formats. Migration-adjacent content follows E-9 surface rules. |

### 5.2 Supply equity targets

Default mentor supply will skew Tashkent, IT, and male. Like the M1 content policy, the mentor roster carries explicit recruitment targets for regional mentors, women (including in nontraditional fields, shown matter-of-factly), and ustalar. Targets are set at Phase-2 entry via the Decisions Log; the principle is binding now.

### 5.3 Vetting pipeline (before any live contact)

Application → verification of employment or enrollment → interview → safeguarding basics + channel-rule training → **async-only probation** (T-2 answers, moderated) → eligibility for live formats. Signed no-solicitation and no-off-platform-contact agreement at entry (ME-4).

**The fake-mentor problem.** Expect applicants whose goal is selling paid courses, "guaranteed admission," or visa services to families. This is a primary threat, not an edge case: it motivates the vetting pipeline, the no-solicitation rule, moderation of all public answers, and the ban on off-platform contact.

---

## 6. Format ladder

Ordered cheapest and safest first. Each format lists its safeguarding profile and phase; phases align with the main §10 plan.

**T-1 — Mentor as content.** Filmed "bir kun" profiles; interview overflow becomes a pre-loaded Q&A bank under each card.
*Safeguarding:* none needed (no interaction). *Supply cost:* absorbed by M1 production. *Phase:* 0–1.

**T-2 — Async public Q&A under career cards.** Students ask under a card; vetted mentors answer; everything is public and moderated before publication. Best answers are promoted into permanent card content (MP-7) and can earn the card a "verified by someone in this job" badge — which simultaneously gives M1 a distributed editorial board and solves part of content-freshness QA (main §11.3).
*Safeguarding:* public, moderated, no direct channels. *Supply cost:* low; fits MS-3/MS-5 time budgets. *Phase:* 2 (live), with the pre-loaded bank shipping in 1.

**T-3 — School group sessions.** One mentor, one class or interest group, hosted and scheduled through the school advisor (M5). Solves supply math and safeguarding simultaneously; buffers the shyness a student feels one-on-one with a high-status adult; gives the B2B offer a differentiator schools can market to parents.
*Safeguarding:* advisor present; school setting. *Supply cost:* one mentor-hour serves 25+ students. *Phase:* 2.

**T-4 — Path cohorts.** Six to ten students interested in the same pathway, one mentor, four semi-scripted sessions (Appendix A). The script is the quality-control and channel-rule enforcement mechanism (MP-3).
*Safeguarding:* group format, logged sessions, parent-visible schedule; session 4 includes parents. *Supply cost:* moderate; MS-2 near-peers are the default staffing. *Phase:* 3.

**T-5 — Family consultations.** The mentor joins the family's congruence conversation (M3) as the credible third voice — the synthetic broker of MP-1, operationalized. Natural premium-offering candidate (monetization is an open question, §11).
*Safeguarding:* parents present by construction. *Supply cost:* high per family; reserve for MS-3/MS-4 with strong vetting history. *Phase:* 3.

**T-6 — True 1:1.** Only much later, for older students (grades 10–11+ / Phase-3 university users): vetted, logged, gender-matched, parent-consented, with the preconditions in §10 met first.
*Safeguarding:* maximal controls; see ME-1, ME-6. *Phase:* 3+, and only by explicit Decisions Log entry.

---

## 7. Integration points with existing modules

- **M1 Explorer.** Filming pipeline doubles as MS-1 onboarding; T-2 answers promote into card content; "verified by" badges; mentors as distributed editorial board for freshness review.
- **M3 Family module.** T-5 attaches to the congruence report; R-3 (family broker) generalizes — where a family lacks a broker, the platform can offer one. The family report gains an optional "discuss with an ustoz" action.
- **M4 Pathway planner.** Each pathway template gains optional `mentor_refs[]`; routing is pathway → mentors who walked it (MP-2).
- **M5 School layer.** Advisors host and gate T-3; group sessions appear in the advisor's term planning and reporting; mentorship becomes a line in the B2B pitch.
- **M6 Research layer.** Mentor interactions are logged as high-intensity exposure events in the telemetry schema. Measurable questions: does mentor contact shift exploration breadth, family congruence, and eventual decisions and persistence (via the 6/18-month follow-ups)? Format comparisons (T-2 vs T-3 vs T-4) are a natural study design. Nobody in this market can currently demonstrate any of this; the evidence is both a moat and publishable.

**Access-matrix extension (extends main §5; binding once graduated).**

| Data | Mentor |
|---|---|
| Student assessment profiles / `ProfileVector` | **Never** |
| Student item-level responses | **Never** |
| Student pathway interest + first name + grade band + region | Only within an active, consented format (T-3/T-4/T-5) |
| Family congruence report | Only in T-5, at the family's invitation |
| Contact details of students or parents | **Never** (all communication in-platform) |

---

## 8. Safeguarding and ethics guardrails

- **ME-1 No private adult–minor channels.** No DM-like capability exists before T-6, and T-6 requires the §10 preconditions plus an explicit Decisions Log entry.
- **ME-2 Observable and logged.** Every live format is recorded or minuted, parent-visible by default, and auditable (extends NFR-8).
- **ME-3 Channel rule enforced structurally.** Formats are scripted or moderated such that prescription has no slot; violations are a removal offense. Reporting mechanism available to students, parents, and advisors.
- **ME-4 No solicitation, no off-platform contact, no side payments.** Mentors may not sell courses or services to platform families, take contact details, or accept payment outside the platform. Signed at entry; enforced by moderation; violation = removal.
- **ME-5 Vetting before live contact.** The §5.3 pipeline is mandatory; async probation precedes any live format.
- **ME-6 Gender-matching for live proximity formats.** For T-4/T-5/T-6, gender-matching is the parent-selectable default. This is a safeguarding and consent measure chosen by families — explicitly distinct from E-5, which forbids gender-conditional logic in scoring and pathway matching. The platform never narrows a student's *options* by gender; families may configure who is in the room.
- **ME-7 Incident handling.** Zero-tolerance removal for safeguarding or solicitation violations; incident log reviewed by product leadership; schools notified where a school-hosted format is involved.
- **ME-8 Minimal data exposure.** Mentors operate on the access-matrix row in §7 — pathway interest and context, never profiles.
- **ME-9 Volunteer/paid clarity.** Each tier's compensation status (stipend, honorarium, volunteer) is explicit and public to mentors; ambiguity here breeds exactly the solicitation behavior ME-4 bans.

---

## 9. Measurement

Success for this module is *not* mentor headcount (MP-5). Candidate metrics, to be finalized at each format's graduation:

| Area | Metric |
|---|---|
| Reach | Share of active students with ≥1 mentor touchpoint (any tier, T-1 counts) per term |
| Quality | T-2 answer approval rate; promotion-to-card rate; student/parent session ratings for T-3/T-4/T-5 |
| Equity | Regional / gender / vocational distribution of the roster vs targets (§5.2) |
| Effect | Change in exploration breadth after mentor contact; family congruence shift after T-5; follow-up outcomes (choice, persistence) vs matched non-mentored comparisons via M6 |
| Safety | Incidents (target: zero); time-to-moderation for T-2; probation failure rate (a healthy pipeline rejects some applicants) |

---

## 10. Phasing and graduation criteria

| Phase | Mentorship scope | Entry criteria |
|---|---|---|
| 0–1 | T-1 only, plus the pre-loaded Q&A bank harvested from filming. | None beyond M1 production. |
| 2 | T-2 live; T-3 school group sessions. | Moderation capacity staffed; vetting pipeline operational; initial roster meeting minimum equity targets; advisor hosting flow built in M5. |
| 3 | T-4 cohorts; T-5 family consultations; formal near-peer program with partner universities. | Cohort scripts piloted; ≥1 university partnership signed for MS-2 supply; T-5 pricing/monetization decision logged. |
| 3+ | T-6 1:1, if ever. | All prior formats running incident-free for a defined period; legal review of minor-adult contact obligations completed; explicit Decisions Log entry. |

---

## 11. Open questions (decide before implementation)

1. **Monetization of T-5.** Premium family offering vs. bundled into B2B vs. free during validity-building — and what paid mentorship does to the volunteer framing in §3.
2. **Stipend levels and funding source for MS-2 near-peers**, and whether university partners co-fund in exchange for the Phase-3 relationship.
3. **Moderation staffing** for T-2 at launch scale (in-house vs. trained senior mentors as moderators).
4. **Who moderates T-3 content** — advisor, platform, or both — and what the advisor training adds for hosting duties.
5. **Karakalpak and regional-language mentor supply** timing relative to locale expansion.
6. **Legal review** of obligations around organized minor–adult contact under Uzbek law (required before any T-4+ format, per §10).
7. **Whether T-2 answers are attributable by full name or first name + role** — credibility vs. mentor privacy trade-off.

---

## 12. Glossary additions

| Term | Meaning |
|---|---|
| Ustoz / shogird | Master / apprentice-disciple; the indigenous mentorship frame. Ustozlik — the standing of being an ustoz, framed as an honor. |
| Hashar | Communal voluntary work tradition; recruitment framing for volunteer mentors. |
| Sadaqa jariya | Ongoing charity whose reward continues; framing for knowledge-sharing as giving back. |
| Tanish-bilish | Connections/acquaintance networks through which much hiring actually operates; what decoding (§2) makes legible for those without it. |
| Near-peer | Mentor 3–6 years older than the student, typically a university student from the same region (MS-2). |
| Broker provisioning | Supplying broker-poor families with a credible third voice (MP-1); the module's core purpose. |

---

## Appendix A — Seed script outline for T-4 path cohorts (four sessions)

The script is the quality-control mechanism (MP-3). Draft outline for piloting, to be localized and tested in Phase 3 entry:

1. **"Mening yo'lim" (My path).** The mentor narrates their own route, including failures, costs, and turning points. No advice — biography only. Students ask about the story.
2. **"Haqiqiy kun" (The real day).** Decoding the work itself: what the job actually consists of, what surprised them, what the career card can't show. Structured around the pathway's career cards.
3. **"Xarita" (The map).** How entry actually happens: which credentials mattered, how hiring worked, what things cost, what tanish-bilish looked like from inside, what they would check before committing. Feasibility, not prescription.
4. **Family session.** Parents invited. The mentor answers family questions about the pathway's realism, costs, and stability — vouching for feasibility in the values vocabulary of M3, never recommending a choice for a specific child.

Each session: 45–60 minutes, group of 6–10, logged, with a one-page parent summary generated afterward.
