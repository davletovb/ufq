# UFQ

Career discovery platform for students and families in Uzbekistan.

## Status

Early product and engineering setup. The project is currently preparing for **Phase 0 — Calibration Pilot**.

**[Progress tracker](docs/progress/README.md)** — delivery state, phase gates, guardrails and
decisions, generated from `docs/progress/data/` and updated with every pull request. The same
data renders as a [visual dashboard](docs/progress/dashboard.html).

The product is designed around a few non-negotiable ideas:

- exposure before assessment;
- behavior over self-description;
- the family as a first-class user;
- plural pathways instead of deterministic labels;
- local validity built from Uzbek data rather than assumed from imported models.

## Product surfaces

The planned product has one backend serving:

1. a Telegram Mini App for students and parents;
2. a responsive web/PWA with account parity;
3. a school dashboard in a later phase.

## Repository setup

The repository is being bootstrapped now. Architecture and implementation choices that are not yet fixed by the product source of truth should be recorded explicitly before they become hard dependencies.

## Documentation

| Path | Contents |
|---|---|
| [`docs/product/`](docs/product/) | The product source of truth and the mentorship concept document. |
| [`docs/progress/`](docs/progress/README.md) | Progress tracker: requirement register, phase gates, guardrail board, decision ledger. |
| [`docs/engineering/`](docs/engineering/architecture.md) | Engineering architecture baseline. |
| [`docs/decisions/`](docs/decisions/README.md) | Architecture decision records. |
