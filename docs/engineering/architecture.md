# Engineering Architecture Baseline

This document captures what the product source of truth already fixes for engineering, and what remains intentionally undecided.

## Fixed by product requirements

### Surfaces

One backend must serve:

- Telegram Mini App for students and parents;
- responsive web/PWA with account parity;
- school dashboard in Phase 2.

For Phase 0, engineering should optimize for the first two consumer surfaces and avoid prematurely building school-specific infrastructure.

### Phase-0 build order

1. Content model + Occupation Explorer core + exposure telemetry (`M1`, `M6-F1`).
2. Assessment session engine + calibration items (`M2`).
3. Family invitation + report skeleton (`M3-lite`).
4. Research pipelines (`M6`).
5. Pathway planner + full family report for Phase 1 (`M4`, `M3`).

### Architectural constraints

- Server-side resumable session state (`M2-F3`, `NFR-6`).
- Role-based access control matching the product access matrix.
- Audit logging for advisor access to individual student data.
- Personal data must be stored and processed in Uzbekistan.
- No third-party analytics that exfiltrate personal data.
- Low-bandwidth operation is a core requirement, not an optimization.
- Locale parity across uz-Latn, uz-Cyrl, and ru at every release.
- Uzbek Cyrillic is produced from canonical uz-Latn through a tested transliteration + exception system; Russian is authored separately.
- Scoring configuration and profile vectors must be versioned and traceable.
- Ranked student lists and individual score exports do not exist as capabilities.

## Intentionally undecided

The product requirements do **not** currently fix:

- frontend framework;
- backend language/framework;
- database engine;
- hosting provider inside Uzbekistan;
- authentication vendor/implementation;
- telemetry implementation;
- media storage/transcoding implementation;
- CI provider beyond GitHub Actions being available to this repository.

These should be decided through ADRs, with the device floor, payload budget, data residency, privacy, and team maintainability as evaluation criteria.

## Proposed repository shape

Once ADR-0001 chooses the stack, prefer a small monorepo with boundaries approximately like:

```text
apps/
  consumer/      # responsive app; Telegram Mini App + web/PWA surface
  api/           # single backend API
packages/
  contracts/     # shared schemas/types if the chosen stack supports it
  i18n/          # locale keys + transliteration rules/tests
  config/        # versioned scoring/configuration, never secrets
content/         # source-controlled seed/pilot content where appropriate
docs/
  decisions/
  engineering/
  product/
  progress/       # generated delivery and compliance tracker
tools/
  progress/       # tracker generator; standard library only
```

This shape is a proposal, not yet an accepted architecture decision.

## First implementation milestone

The first runnable vertical slice should be intentionally narrow:

> A student can open one career card, the system records a versioned exposure event, the student can resume after reconnecting, and the event can be inspected in a de-identified development dataset.

That slice validates the most important early architecture: content, localization, telemetry, resumability, and data boundaries before assessment complexity is added.

Its requirements are tracked as `M1-F1`, `M1-F3`, `M2-F3`, `M6-F1` and `NFR-6` in the
[progress tracker](../progress/README.md).
