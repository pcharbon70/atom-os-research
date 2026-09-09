---
title: "Offline scarce rights and online effect gates"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Offline scarce rights and online effect gates

This study decomposes [Offline collaboration, replication, and conflict semantics](../offline-collaboration-replication-and-conflict-semantics.md).

Research question: Which offline changes can commit scarce resources, and which must remain proposals?

## Research basis and status

Bounded counters conserve distributed numeric rights under crash and intact-storage assumptions; Byzantine double spending is outside the paper's model. [1](../../../30-sources/balegas-et-al-2015-bounded-counters.md).

Invariant confluence relates coordination freedom to the exact operations, invariant and merge model. [2](../../../30-sources/bailis-et-al-2014-coordination-avoidance.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the relationship between collaborative content and numerical or exclusive
resource rights. Offline edits may change a draft while publication, payment or
device actuation remains online-only. Conserved allocations are scoped to object,
invariant, replica generation and allowed operation class; they are not arbitrary
signing credentials.

### Admission, transitions and completion

Admit local scarce-resource operations only against durable nonreusable rights under
the qualified failure model. Retain operation identity and consumption atomically.
When reconnecting, reconcile lineage without recreating unreachable allocations. A
content merge that requests an external effect creates a proposal for normal online
admission, not an automatic replay side effect.

### Failure and adversarial behavior

Cloning a device backup can clone its apparent rights if no anti-rollback or
replica-identity protection exists. Revocation cannot safely reclaim already
spendable offline allocations by timeout alone. A merged publication flag must not
cause every peer to publish independently.

### Alternatives and unresolved tradeoffs

Server-coordinated scarce operations are simpler and often appropriate. Escrow
enables bounded offline availability but strands rights and adds recovery
assumptions. A document can use both without falsely advertising every field as
equally available or authoritative.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Clone an offline replica and spend from both copies; reject the unsupported profile or demonstrate prevention of double allocation.
- Merge the same publish proposal at several peers; only one separately admitted online workflow may own execution.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Escrow rights conservation and transfer](../invariants-transactions-and-concurrency-policy/escrow-rights-conservation-and-transfer.md) — a cross-component contract this service must preserve.
- [Directed compatibility and behavioral fixture matrices](../application-evolution-schema-compatibility-and-migration/directed-compatibility-and-behavioral-fixture-matrices.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Bounded counters](../../../30-sources/balegas-et-al-2015-bounded-counters.md).
2. [Coordination Avoidance](../../../30-sources/bailis-et-al-2014-coordination-avoidance.md).
