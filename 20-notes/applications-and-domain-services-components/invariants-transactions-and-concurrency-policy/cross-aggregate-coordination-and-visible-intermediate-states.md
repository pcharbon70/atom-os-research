---
title: "Cross-aggregate coordination and visible intermediate states"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Cross-aggregate coordination and visible intermediate states

This study decomposes [Invariants, transactions, and concurrency policy](../invariants-transactions-and-concurrency-policy.md).

Research question: How should a domain choose between a true atomic transaction and a long-running workflow?

## Research basis and status

Sagas permit visible intermediate commits and semantic compensation; they do not supply outer transaction isolation. [1](../../../30-sources/garcia-molina-salem-1987-sagas.md).

Invariant confluence relates coordination freedom to the exact operations, invariant and merge model. [2](../../../30-sources/bailis-et-al-2014-coordination-avoidance.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the cross-aggregate obligation, allowed intermediate states, participants and
named decision authority. Distinguish serializable transactions among participating
stores from workflows whose committed steps are visible. The kernel and runtime do
not decide whether reserved inventory without payment is a legal business state.

### Admission, transitions and completion

First state the indivisible invariant and required observer history. If all relevant
stores participate in a qualified transaction, use its prepare, decision and
recovery contract. Otherwise model reservations, deadlines, pivots and compensation
as explicit domain states. Exclusive resources use sink-checked fences; coordinator
ownership alone cannot exclude a stale participant.

### Failure and adversarial behavior

A saga can fail after another actor acts on an intermediate fact. Compensation
cannot erase that observer's action. Losing quorum must not create a fabricated
commit decision. A lease that expires while an unfenceable device acts supplies no
exclusive-effect guarantee; such a profile must expose uncertainty or be rejected.

### Alternatives and unresolved tradeoffs

Broad distributed transactions simplify some invariants but increase failure
coupling and blocking risks. Smaller aggregates plus reservations may scale better
while changing business semantics. Neither approach wins universally; compare
allowed histories, recovery burden and workload measurements.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Observe and act on a partially completed workflow, then compensate it; surviving consequences must remain represented.
- Partition the coordinator and resume an obsolete participant; demonstrate sink rejection or explicitly unresolved effect status.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Authoritative state profiles and persistence boundaries](../durable-state-journals-snapshots-and-projections/authoritative-state-profiles-and-persistence-boundaries.md) — a cross-component contract this service must preserve.
- [Compensation, pivots, and manual repair](../workflows-process-managers-timers-and-compensation/compensation-pivots-and-manual-repair.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Sagas](../../../30-sources/garcia-molina-salem-1987-sagas.md).
2. [Coordination Avoidance](../../../30-sources/bailis-et-al-2014-coordination-avoidance.md).
