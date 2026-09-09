---
title: "Semantic repositories and query-model boundaries"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Semantic repositories and query-model boundaries

This study decomposes [Bounded contexts, domain model, and application services](../bounded-contexts-domain-model-and-application-services.md).

Research question: What does a repository promise beyond access to serialized records?

## Research basis and status

Evans separates domain rules from application coordination; this is a pattern vocabulary, not a recovery proof. [1](../../../30-sources/evans-2015-domain-driven-design-reference.md).

Overeem and colleagues report practitioner experience with event evolution and recovery costs, not universal event-sourcing benefits. [2](../../../30-sources/overeem-et-al-2021-event-sourced-systems.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own loading and persistence contracts expressed as domain identity, expected
revision, authoritative schema and named commit evidence. Query models separately
own projections, completeness and freshness. Neither exposes raw store addresses or
gives an application permission to inspect another realm's records.

### Admission, transitions and completion

Resolve a current authorized store facet, load an identified revision and validate
its interpretation. Submit proposed changes through the aggregate commit boundary.
Queries specify required frontiers, acceptable staleness, redaction and pagination
budgets. A result from a derived read model is evidence about a projection, not a
reservation or write authorization.

### Failure and adversarial behavior

A convenient repository that writes several records independently can violate the
aggregate atomicity contract. A projection silently serving yesterday's policy may
leak data even when its business fields are fresh. Rebind data partitions and policy
generations together; do not interpret a missing cache row as authoritative entity
absence.

### Alternatives and unresolved tradeoffs

Current-state storage is a useful ordinary profile. Event sourcing adds meaningful
history when its replay and evolution costs are justified. CQRS can use either
profile; splitting reads and writes does not require a universal append-only domain
log.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Lose a store reply during compare-and-commit; reconcile revision and operation result rather than overwriting again.
- Page through a changing projection under revoked read authority; tokens must enforce the declared snapshot and policy contract.

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
2. [Event-sourced systems study](../../../30-sources/overeem-et-al-2021-event-sourced-systems.md).
