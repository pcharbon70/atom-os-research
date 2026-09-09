---
title: "Shadow migration checkpoints and validation"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Shadow migration checkpoints and validation

This study decomposes [Application evolution, schema compatibility, and migration](../application-evolution-schema-compatibility-and-migration.md).

Research question: How can data conversion be interrupted without damaging the source or guessing progress?

## Research basis and status

F1 uses safe intermediate schemas under a bounded version-lag assumption; arbitrary actor upgrades do not inherit its proof. [1](../../../30-sources/rae-et-al-2013-online-schema-change-f1.md).

Proteus relates update safety to code, data and update points; type safety is weaker than domain or effect safety. [2](../../../30-sources/stoyle-et-al-2005-safe-predictable-dynamic-updating.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own migration ID, exact source generation and frontier, target schema, range
checkpoints, transformation digest and validation results. Workers receive bounded
source-read and private-target-write facets. They do not receive publication,
arbitrary effect or source-deletion authority.

### Admission, transitions and completion

Reserve shadow and recovery capacity, transform deterministic ranges, persist
digests and checkpoints, then validate schemas, invariants, references and accepted
obligations. Capture ongoing source changes through an explicit delta protocol or
quiesce writers. A completion certificate names the exact source frontier and
transformed target; publication requires current evidence.

### Failure and adversarial behavior

A checkpoint written before target durability can skip lost data. A migration that
consults live external facts may produce different results on resume. Copying state
without outcome, outbox or workflow records loses responsibility even if every
entity row matches its expected schema.

### Alternatives and unresolved tradeoffs

Copy-transform isolates failures at additional storage cost. In-place conversion can
fit smaller systems but requires stronger exclusive-writer and recovery proofs. Pure
upcasting is appropriate for retained histories only when all required semantics
remain available.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Crash after every range write and checkpoint; resume to the same validated target digest.
- Remove one pending operation or workflow intent from a shadow copy; validation must reject publication despite valid entity rows.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Retention, erasure, and recovery dependency closure](../durable-state-journals-snapshots-and-projections/retention-erasure-and-recovery-dependency-closure.md) — a cross-component contract this service must preserve.
- [Compensation, pivots, and manual repair](../workflows-process-managers-timers-and-compensation/compensation-pivots-and-manual-repair.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [F1 schema evolution](../../../30-sources/rae-et-al-2013-online-schema-change-f1.md).
2. [Mutatis Mutandis](../../../30-sources/stoyle-et-al-2005-safe-predictable-dynamic-updating.md).
