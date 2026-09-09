---
title: "Escrow rights conservation and transfer"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Escrow rights conservation and transfer

This study decomposes [Invariants, transactions, and concurrency policy](../invariants-transactions-and-concurrency-policy.md).

Research question: When can a replica spend scarce quantity offline without exceeding the global bound?

## Research basis and status

Bounded counters conserve distributed numeric rights under crash and intact-storage assumptions; Byzantine double spending is outside the paper's model. [1](../../../30-sources/balegas-et-al-2015-bounded-counters.md).

Invariant confluence relates coordination freedom to the exact operations, invariant and merge model. [2](../../../30-sources/bailis-et-al-2014-coordination-avoidance.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own a numerical rights ledger, replica identities, allocation generation, consumed
rights and transfer lineage. Rights encode permission within one specific invariant,
not general access authority. Layer 4 must protect local durable state and
authenticate authorized spenders; a malicious replica with forgeable counters
invalidates the assumed model.

### Admission, transitions and completion

Allocate a conserved quantity across admitted replicas. Spend only from locally
available rights, atomically recording consumption and operation outcome. Transfer
by a durable protocol that never makes the same rights spendable at both endpoints.
When rights are unavailable locally, reject, queue a proposal or request transfer;
do not infer availability from a stale global total.

### Failure and adversarial behavior

An unreachable replica's rights cannot be recreated merely because its lease timed
out while offline spending remains possible. Recovery needs fencing, intact state or
explicit withdrawal of that replica's right to integrate old operations. Restoring
an old backup can replay spent rights; incarnation and anti-rollback requirements
are architectural obligations beyond the crash-only paper.

### Alternatives and unresolved tradeoffs

Escrow trades coordination latency for stranded capacity and ledger cost. A
centralized counter is simpler when availability during partitions is not required.
Arbitrary multi-object constraints do not become escrow-compatible because each
field is numeric.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Partition replicas, exhaust local allocation and duplicate transfers; total admitted spend must remain within the conserved bound.
- Restore an old replica snapshot and reuse its identity; reject its obsolete spending generation or demonstrate equivalent anti-rollback protection.

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

1. [Bounded counters](../../../30-sources/balegas-et-al-2015-bounded-counters.md).
2. [Coordination Avoidance](../../../30-sources/bailis-et-al-2014-coordination-avoidance.md).
