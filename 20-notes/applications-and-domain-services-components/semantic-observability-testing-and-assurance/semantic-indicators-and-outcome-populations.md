---
title: "Semantic indicators and outcome populations"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Semantic indicators and outcome populations

This study decomposes [Semantic observability, testing, and assurance](../semantic-observability-testing-and-assurance.md).

Research question: Which observations distinguish a responsive application from one that actually completed correct work?

## Research basis and status

Google SRE guidance starts indicators from user-relevant behavior and explicit measurement populations, not process uptime alone. [1](../../../30-sources/jones-et-al-2016-service-level-objectives.md).

DAGOR propagates admission priorities through request paths; its empirical policy is neither a hard resource ceiling nor universal fairness. [2](../../../30-sources/zhou-et-al-2018-dagor.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own indicator definitions, populations, observation windows and semantic
classifications. Separate attempted, admitted, committed, terminated and unresolved
operations. Layer 4 collects bounded measurements; only Layer 5 can define whether
an order, edit or workflow outcome met its promised postcondition.

### Admission, transitions and completion

Define each numerator and denominator with explicit treatment of pending work at the
window boundary. Measure admission delay, durable commit latency, projection
freshness and reconciliation age independently. Join sampled operational telemetry
to aggregate outcome evidence without turning sampled traces into a complete ledger.
Record missing data rather than treating unobserved requests as success.

### Failure and adversarial behavior

Measuring only completed calls hides permanently pending work. A retry storm
inflates attempted counts without increasing logical operations. A fast stale
response can improve latency while failing usefulness. High-cardinality entity
labels can leak data and exhaust the collector; use controlled dimensions and
authorized drill-down.

### Alternatives and unresolved tradeoffs

One availability score is convenient for dashboards but obscures semantic modes.
Several indicators cost more explanation yet distinguish refusal from lost
responsibility. Numerical targets require workload and user evidence; this research
does not choose arbitrary percentiles as accepted service guarantees.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Construct a workload with fast refusals and indefinitely pending effects; indicators must not report full semantic availability.
- Lose telemetry while retaining outcome records; report measurement coverage separately from known business commitment.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Operation identity and honest outcome ledgers](../typed-commands-queries-events-and-protocol-contracts/operation-identity-and-honest-outcome-ledgers.md) — a cross-component contract this service must preserve.
- [Semantic admission classes and protected recovery reserve](../cross-layer-placement-tenancy-overload-and-recovery-topology/semantic-admission-classes-and-protected-recovery-reserve.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Service Level Objectives](../../../30-sources/jones-et-al-2016-service-level-objectives.md).
2. [DAGOR](../../../30-sources/zhou-et-al-2018-dagor.md).
