---
title: "Authoritative state profiles and persistence boundaries"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Authoritative state profiles and persistence boundaries

This study decomposes [Durable state, journals, snapshots, and projections](../durable-state-journals-snapshots-and-projections.md).

Research question: Which stored representation is authoritative for each domain object?

## Research basis and status

Overeem and colleagues report practitioner experience with event evolution and recovery costs, not universal event-sourcing benefits. [1](../../../30-sources/overeem-et-al-2021-event-sourced-systems.md).

ARIES makes recovery depend on durable ordering metadata; its storage log is not a domain-event model. [2](../../../30-sources/mohan-et-al-1992-aries.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own a persistence profile per aggregate or context: current state, current state
with change history, event history, or an explicitly replicated operation
representation. Record authoritative roots, schema readers, revision rules,
integrity checks, outcome retention and the recovery service. A serialized actor
heap is not this contract.

### Admission, transitions and completion

Select the profile from domain requirements, then map it to a Layer 4 store with an
explicit durability scope. Commit semantic state with outcome and accepted-intent
records. Recovery validates ownership, schema, integrity and invariants before
opening writers. A backup restore is a new recovery event requiring generation
fencing, not transparent continuation from any available bytes.

### Failure and adversarial behavior

Current state plus a casually written log can disagree about truth after a crash. An
event stream lacking required reader code can be as unusable as lost state. A
recovery tool must not skip an unreadable committed record and declare a later state
authoritative.

### Alternatives and unresolved tradeoffs

Event sourcing supports temporal interpretation when its costs are justified;
current-state persistence avoids mandatory replay. Hybrid profiles need one named
authority rather than two mutually reparable truths. Physical store recovery belongs
below Layer 5 even when business recovery rejects its valid bytes.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Restore state with mismatched outcome and intent frontiers; fail qualification rather than admit writes.
- Compare current-state and history-based recovery on the same domain workload, including old readers and bounded storage.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Aggregate commit bundles and revision validation](../invariants-transactions-and-concurrency-policy/aggregate-commit-bundles-and-revision-validation.md) — a cross-component contract this service must preserve.
- [Shadow migration checkpoints and validation](../application-evolution-schema-compatibility-and-migration/shadow-migration-checkpoints-and-validation.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Event-sourced systems study](../../../30-sources/overeem-et-al-2021-event-sourced-systems.md).
2. [ARIES](../../../30-sources/mohan-et-al-1992-aries.md).
