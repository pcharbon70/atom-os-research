---
title: "Aggregate turns and asynchronous continuations"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Aggregate turns and asynchronous continuations

This study decomposes [Durable domain identity, aggregate actors, and lifecycle](../durable-domain-identity-aggregate-actors-and-lifecycle.md).

Research question: How can an aggregate remain responsive without letting reentrant work invalidate its decision?

## Research basis and status

Evans separates domain rules from application coordination; this is a pattern vocabulary, not a recovery proof. [1](../../../30-sources/evans-2015-domain-driven-design-reference.md).

Liskov and Wing treat substitution as preservation of behavioral properties, beyond compatible representation. [2](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the current aggregate revision, bounded command queue and explicit pending
proposals. The ordinary profile is one non-reentrant decision turn per active
aggregate. Long computation and remote I/O use separately budgeted workers; workers
receive copied values and cannot commit aggregate state.

### Admission, transitions and completion

Validate command, generation and expected revision; compute a bounded proposal;
request one commit and record its outcome. If work must leave the actor, record the
continuation identity, input revision and allowed response protocol. A returned
result starts a fresh decision against current state. It is not permission to resume
mutating the old snapshot as if no other command ran.

### Failure and adversarial behavior

Awaiting a remote callback while retaining an implicit transaction can deadlock
cyclic calls or admit an intervening mutation. Killing a timed-out worker does not
retract effects it previously requested. Pure computational results can be discarded
when stale, but accepted effectful work needs its own durable owner.

### Alternatives and unresolved tradeoffs

Reentrancy can improve throughput for carefully partitioned state, but requires an
explicit invariant-preserving interleaving argument. Keeping everything synchronous
is simpler only while worst-case turn cost is bounded. A large aggregate hotspot may
require redesigned invariants rather than more worker threads.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Interleave a slow price calculation with an inventory update; stale computed output must be revalidated.
- Inject recursive calls and worker timeout; unrelated aggregates must progress without losing accepted obligations.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Aggregate commit bundles and revision validation](../invariants-transactions-and-concurrency-policy/aggregate-commit-bundles-and-revision-validation.md) — a cross-component contract this service must preserve.
- [Workflow-generation handoff and publication fences](../application-evolution-schema-compatibility-and-migration/workflow-generation-handoff-and-publication-fences.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [DDD Reference](../../../30-sources/evans-2015-domain-driven-design-reference.md).
2. [Behavioral subtyping](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).
