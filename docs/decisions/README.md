# Architecture Decision Records

Use this directory for engineering decisions that are expensive to reverse, affect multiple modules, or carry security/privacy implications.

The product framework's Decisions Log remains authoritative for **product** decisions. ADRs document **implementation** decisions and must not silently override the product framework.

## Naming

```text
0001-short-decision-name.md
0002-another-decision.md
```

## Suggested ADR shape

```markdown
# ADR-0001: Decision title

- Status: proposed | accepted | superseded
- Date: YYYY-MM-DD
- Product references: M1-F3, NFR-2, E-8, ...

## Context

## Decision

## Alternatives considered

## Consequences

## Follow-ups
```

Start an ADR before committing to choices such as the frontend/runtime stack, API framework, database, Uzbekistan hosting provider, authentication implementation, telemetry stack, media pipeline, or transliteration implementation.
