---
title: "Domain vocabulary, value model, and rule ownership"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Domain vocabulary, value model, and rule ownership

This study decomposes [Bounded contexts, domain model, and application services](../bounded-contexts-domain-model-and-application-services.md).

Research question: Where do concepts and invariants belong when several services use the same words?

## Research basis and status

Evans separates domain rules from application coordination; this is a pattern vocabulary, not a recovery proof. [1](../../../30-sources/evans-2015-domain-driven-design-reference.md).

Liskov and Wing treat substitution as preservation of behavioral properties, beyond compatible representation. [2](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own a context vocabulary, value equality and normalization rules, entity types,
aggregate boundaries and named domain policies. A customer identifier in billing is
not automatically the same semantic concept as an account in authentication. A
business-tenant designation remains distinct from its Layer 4 authenticated
security-realm binding.

### Admission, transitions and completion

Define representative examples and counterexamples before choosing modules or
actors. Separate pure decisions from effectful coordination. A domain decision
accepts explicit facts and versions and yields either a reasoned rejection or a
proposed transition. Commit and authorization remain separate checks; a correct
calculation must not confer permission to apply it.

### Failure and adversarial behavior

Two modules can independently validate plausible states yet disagree about units,
rounding, time zones or lifecycle meaning. Persist canonical values and required
interpretation versions. Bound parsing and arithmetic; invalid or overflowing input
is not normalized into a different valid business request.

### Alternatives and unresolved tradeoffs

A shared kernel of domain vocabulary can reduce duplication among closely
coordinated contexts, but makes their evolution coupled. Independent models with
translations cost more code yet allow distinct meanings. Use a pure function unless
persistent identity, sequencing or isolation justifies an actor.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Generate boundary values for equality, units and rounding; equivalent inputs must have the declared canonical meaning.
- Change one context's definition of customer eligibility; unrelated contexts must not silently inherit it.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Invariant catalog and coordination selection](../invariants-transactions-and-concurrency-policy/invariant-catalog-and-coordination-selection.md) — a cross-component contract this service must preserve.
- [Operation identity and honest outcome ledgers](../typed-commands-queries-events-and-protocol-contracts/operation-identity-and-honest-outcome-ledgers.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [DDD Reference](../../../30-sources/evans-2015-domain-driven-design-reference.md).
2. [Behavioral subtyping](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).
