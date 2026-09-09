---
title: "Invariant catalog and coordination selection"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Invariant catalog and coordination selection

This study decomposes [Invariants, transactions, and concurrency policy](../invariants-transactions-and-concurrency-policy.md).

Research question: Which properties actually require coordination, and which can survive independent decisions?

## Research basis and status

Invariant confluence relates coordination freedom to the exact operations, invariant and merge model. [1](../../../30-sources/bailis-et-al-2014-coordination-avoidance.md).

Evans separates domain rules from application coordination; this is a pattern vocabulary, not a recovery proof. [2](../../../30-sources/evans-2015-domain-driven-design-reference.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own a versioned invariant catalog containing quantified state, allowed initial
states, every mutating operation, external facts and permitted merge. Include
lifecycle, authorization-sensitive transitions and cross-field constraints, not
merely data-type checks. Each property names its authoritative owner and an
executable reference predicate.

### Admission, transitions and completion

Analyze aggregate-local transitions first. For independent replicas, search for two
valid histories from a common ancestor whose merge violates the property. A found
counterexample requires coordination, a restricted operation set or a changed
business rule. A bounded search without a counterexample is evidence only within its
bounds, not a universal confluence proof.

### Failure and adversarial behavior

An omitted refund, deletion, import or migration can invalidate an otherwise
convincing argument about sales. Authorization changes may require coordination even
if content edits merge. A new policy or schema changes the analyzed system and must
reopen its qualification; a familiar CRDT label is not acceptance evidence.

### Alternatives and unresolved tradeoffs

Local serialization is a conservative baseline for a complete local invariant.
Escrow can reformulate numerical constraints into disjoint rights. General
cross-aggregate coordination costs availability; a workflow is acceptable only if
visible intermediate states satisfy the domain's weaker contract.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Generate concurrent histories for uniqueness, bounded stock and last-administrator removal; preserve counterexamples as fixtures.
- Add a migration or repair command to an approved model and require re-analysis before classifying it coordination-free.

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

1. [Coordination Avoidance](../../../30-sources/bailis-et-al-2014-coordination-avoidance.md).
2. [DDD Reference](../../../30-sources/evans-2015-domain-driven-design-reference.md).
