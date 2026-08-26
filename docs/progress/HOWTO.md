# Keeping the tracker true

The tracker is generated. You edit data, not documents.

```text
docs/progress/data/*.json   <- you edit this
        |
        |  python3 tools/progress/progress.py build
        v
docs/progress/README.md, roadmap.md, requirements.md,
guardrails.md, decisions.md, dashboard.html   <- generated, committed, never hand-edited
```

## The loop, per pull request

1. Do the work.
2. Update `docs/progress/data/requirements.json` for anything whose state changed.
3. Run `python3 tools/progress/progress.py build`.
4. Commit the data change and the regenerated views together with the code.
5. Reference the requirement IDs in the pull-request description.

CI fails the pull request if the views are stale or if a cited ID does not exist,
and posts a comment showing the status changes the pull request makes.

## What a status means

Delivery items — modules, functional requirements, non-functional requirements:

| Status | Meaning |
|---|---|
| `not-started` | No code. |
| `in-progress` | Started, not merged, or merged but incomplete. |
| `shipped` | Merged and working. |
| `verified` | Shipped *and* evidenced — tests, a pilot result, a QA pass. Add the link under `evidence`. |
| `blocked` | Cannot proceed. Say why in `note`. |
| `deferred` | Deliberately out of the current phase. Excluded from percentages. |
| `concept` | Documented, not yet a commitment. Excluded from percentages. |

Compliance items — principles, guardrails, product-level refusals:

| Status | Meaning |
|---|---|
| `upheld` | Something exists that could violate this rule, and it does not. |
| `at-risk` | A change makes violating it plausible. Say how in `note`. |
| `violated` | We are breaking it. This is a bug with a deadline. |
| `not-applicable` | Nothing built yet that could violate it. |
| `not-yet-binding` | From the mentorship concept; binding only once it graduates into the framework's Decisions Log. |

A guardrail is never "done". It moves to `at-risk` or `violated` in the same pull
request that introduces the risk — not in a later cleanup pass.

## Adding a requirement

Requirements come from the product documents in `docs/product/`. If you need an ID
that does not exist there, the product document changes first, through its Decisions
Log. Then add the item:

```json
{ "id": "M1-F6", "kind": "feature", "parent": "M1", "track": "delivery",
  "title": "Short name", "phase": "0", "mvp": true, "owner": "eng",
  "source": "framework §6 M1-F6", "summary": "One sentence, plain language.",
  "derives_from": ["GT-2"], "evidence": [], "tracking": [] }
```

One item per line keeps the diff readable: a changed requirement is a changed line.

| Field | Notes |
|---|---|
| `id` | Must match the product document exactly. |
| `kind` | `ground-truth`, `principle`, `role`, `module`, `feature`, `nfr`, `guardrail`, or a `mentor-*` kind. |
| `track` | `delivery` (built), `compliance` (upheld), `context` (reference only). |
| `phase` | Must be a phase in `roadmap.json`. |
| `mvp` | `true` for Phase-1 binding scope. Drives the MVP meter. |
| `source` | Where the requirement is defined. Required. |
| `derives_from` | Ground truths, principles or guardrails this serves. Every ID must exist. |
| `evidence` | Links that justify `shipped` or `verified`. |
| `tracking` | Issue or pull-request links. |
| `focus` | `true` puts it in the "Now and next" list. Keep this to a handful. |
| `violation_test` | Required on every compliance item. |

Module status is rolled up from its features. Setting it by hand is a validation error.

## Other data files

- `roadmap.json` — phases and exit criteria, the content floor, success metrics,
  launch checklists, risks. Update `current` on a criterion or metric as soon as
  there is a real number; `null` renders as "no data yet", which is honest and useful.
- `decisions.json` — product decisions mirroring the framework's Decisions Log, the
  ADR index, and open questions. Add an ADR entry when you open one in
  `docs/decisions/`.

## Commands

```bash
python3 tools/progress/progress.py build      # regenerate every view
python3 tools/progress/progress.py validate   # data integrity only
python3 tools/progress/progress.py check      # what CI runs
python3 tools/progress/progress.py html --fragment > /tmp/dash.html   # for publishing
```

Python 3.9+, standard library only. No install step, and no dependency on the stack
decision that ADR-0001 has yet to make.

## The visual dashboard

`dashboard.html` is generated alongside the Markdown and opens directly in a browser.
It is also the source for the shared dashboard page — regenerate with `--fragment` and
republish to the same URL so the link stays stable.
