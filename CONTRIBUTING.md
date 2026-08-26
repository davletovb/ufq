# Contributing to UFQ

## Working model

- `main` should stay reviewable and releasable.
- Use short-lived branches named by intent, for example `feat/exposure-logging`, `fix/session-resume`, or `chore/dev-tooling`.
- Open a pull request for non-trivial changes.
- Keep commits focused and explain *why* when a change implements a product constraint.

## Requirement traceability

The product framework defines stable requirement IDs such as `GT-n`, `P-n`, `M1-F1`, `NFR-n`, and `E-n`.

When a change implements or materially affects one of these requirements, reference the relevant ID in the PR description and, when useful, the commit message. Example:

```text
feat(explorer): log career-card exposure events (M1-F3, M6-F1)
```

Do not silently change a binding product requirement in code. Product-level changes belong in the product Decisions Log first.

## Before merging

A PR should make clear:

1. what changed;
2. why it changed;
3. which product requirements or engineering decisions it touches;
4. how it was tested;
5. whether it changes data collection, consent, localization, or access control.

## Engineering decisions

Implementation choices not fixed by the product framework should be documented as an ADR in `docs/decisions/` when they are expensive to reverse, security/privacy relevant, or affect multiple parts of the system.

## Security and data

Never commit secrets, production personal data, raw pilot exports, or identifiable research data. Treat data residency, minors' consent, shared-device safety, and access logging as architectural requirements rather than later hardening work.
