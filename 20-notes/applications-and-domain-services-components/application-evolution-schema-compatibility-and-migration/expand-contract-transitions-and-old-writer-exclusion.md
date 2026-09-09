---
title: "Expand-contract transitions and old-writer exclusion"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Expand-contract transitions and old-writer exclusion

This study decomposes [Application evolution, schema compatibility, and migration](../application-evolution-schema-compatibility-and-migration.md).

Research question: When is it safe to remove the old representation or protocol?

## Research basis and status

Sato separates interface expansion, client migration and contraction; the pattern is not a distributed correctness proof. [1](../../../30-sources/sato-2014-parallel-change.md).

F1 uses safe intermediate schemas under a bounded version-lag assumption; arbitrary actor upgrades do not inherit its proof. [2](../../../30-sources/rae-et-al-2013-online-schema-change-f1.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the ordered intermediate representations, old/new reader and writer permissions,
migration completion frontier and contraction certificate. Layer 4 enforces
generation publication and writer fencing. Supporting both encodings is not
equivalent to preserving every old/new interleaving.

### Admission, transitions and completion

Expand with explicitly compatible read and write behavior; migrate data and clients
under checkpoints; verify old writes are excluded or translated safely; only then
contract. Model deletion and backfill races, not just additions. Every intermediate
state must preserve current invariants and a declared recovery path.

### Failure and adversarial behavior

An old writer can recreate a removed field or leave a new index incomplete after
backfill. A stale process may resume after apparent quiescence. The F1
one-version-lag condition is a specific assumption, not permission for unlimited
offline client versions. Exclusion must be enforced at the actual mutation boundary.

### Alternatives and unresolved tradeoffs

Dual-write can support migration but needs atomic coupling or a reconciliation
protocol for divergence. Delegating old APIs to one canonical writer reduces
duplicate logic where semantics permit it. Long-lived coexistence may be preferable
to contraction when offline clients cannot be safely retired.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Race old deletion and new backfill, then crash; no orphaned authoritative representation may be published.
- Resume an old writer after contraction and verify sink-side refusal rather than reliance on deployment inventory.

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

1. [Parallel Change](../../../30-sources/sato-2014-parallel-change.md).
2. [F1 schema evolution](../../../30-sources/rae-et-al-2013-online-schema-change-f1.md).
