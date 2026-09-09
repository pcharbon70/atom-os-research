---
title: "Aggregate commit bundles and revision validation"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Aggregate commit bundles and revision validation

This study decomposes [Invariants, transactions, and concurrency policy](../invariants-transactions-and-concurrency-policy.md).

Research question: What must commit together for one accepted domain transition to be recoverable?

## Research basis and status

ARIES makes recovery depend on durable ordering metadata; its storage log is not a domain-event model. [1](../../../30-sources/mohan-et-al-1992-aries.md).

RIFL couples mutations to retained completion records; its guarantees require participating storage and recoverable request identity. [2](../../../30-sources/lee-et-al-2015-rifl.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the semantic transaction bundle: expected revision, new state or events,
operation outcome, outbox intents and workflow starts. Layer 4 supplies an admitted
atomic durability profile. The aggregate determines which values jointly express one
legal transition; it does not implement its own block ordering or WAL.

### Admission, transitions and completion

Validate current writer fence, realm binding, operation identity and invariant
dependencies. Apply one conditional commit, then publish the resulting receipt. If
the result is lost, query the same operation and revision. Any read dependency
affecting correctness must be included in the transaction's conflict validation or
protected by a separately qualified coordination protocol.

### Failure and adversarial behavior

A serial mailbox cannot prevent another writer or a migration tool from changing the
store. Writing state before the outcome permits duplicate replay; writing an outbox
after acknowledgment permits lost effects. If the substrate cannot atomically retain
the whole promised bundle, narrow the transaction contract rather than paper over
the gap.

### Alternatives and unresolved tradeoffs

Single-record encoding can simplify atomicity at a size and contention cost.
Multi-record transactions permit clearer partitions but require a stronger
substrate. Optimistic retries are safe only for pure proposal construction, with
bounded attempts and no external actions inside the retry body.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Inject crashes between every physical write and flush boundary in the selected store; no acknowledged partial bundle may recover.
- Race two valid proposals with the same expected revision and distinct IDs; at most one wins without a fresh decision.

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

1. [ARIES](../../../30-sources/mohan-et-al-1992-aries.md).
2. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
