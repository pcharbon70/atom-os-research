---
title: "Activation recovery and writer fencing"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Activation recovery and writer fencing

This study decomposes [Durable domain identity, aggregate actors, and lifecycle](../durable-domain-identity-aggregate-actors-and-lifecycle.md).

Research question: What must an aggregate recover before its activation is allowed to write?

## Research basis and status

The 2014 Orleans report separates logical actor identity from activation; its cloud model is not the BEAM process contract. [1](../../../30-sources/bernstein-et-al-2014-orleans.md).

RIFL couples mutations to retained completion records; its guarantees require participating storage and recoverable request identity. [2](../../../30-sources/lee-et-al-2015-rifl.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own activation progress and a recoverable association between DomainRef, state
revision and outstanding operation outcomes. Layer 4 owns lease issuance, routing
and persistent fencing. A runtime actor is a candidate owner only; its belief that
it is active cannot authorize a store commit.

### Admission, transitions and completion

Acquire a current writer generation, load the authoritative state and outcome
frontier, validate schema and invariants, then open command admission. A replacement
activation must recover pending accepted work before exposing a clean state. Every
commit carries the fence and expected revision. Handoff preserves the records needed
for old request IDs before routes change.

### Failure and adversarial behavior

During partition two activations can both run. Sink-side fencing prevents the
obsolete one from committing, but only if every write path participates. If fencing
cannot be established, stop authoritative writes and expose unavailable or pending
status. Lease expiration does not prove an already dispatched external effect
failed.

### Alternatives and unresolved tradeoffs

A strictly single-host writer avoids distributed leases but still needs crash
recovery and stale-generation checks. Pooled activations reduce memory at the cost
of scheduling and isolation analysis. Do not select a virtual-actor library merely
because its naming abstraction resembles the desired identity model.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Pause the old writer across lease replacement, then resume it against both state and effect sinks.
- Recover state without completion metadata and attempt a duplicate command; admission must remain closed or reconcile safely.

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

1. [Orleans virtual actors](../../../30-sources/bernstein-et-al-2014-orleans.md).
2. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
