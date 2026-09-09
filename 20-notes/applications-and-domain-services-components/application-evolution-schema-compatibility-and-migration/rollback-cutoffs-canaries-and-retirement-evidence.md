---
title: "Rollback cutoffs, canaries, and retirement evidence"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Rollback cutoffs, canaries, and retirement evidence

This study decomposes [Application evolution, schema compatibility, and migration](../application-evolution-schema-compatibility-and-migration.md).

Research question: When does rollback cease to mean restoring a valid prior application generation?

## Research basis and status

NixOS separates immutable configuration generations from mutable activation effects; selecting an old generation does not undo domain state. [1](../../../30-sources/dolstra-et-al-2008-nixos.md).

Sato separates interface expansion, client migration and contraction; the pattern is not a distributed correctness proof. [2](../../../30-sources/sato-2014-parallel-change.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own rollback preconditions, retained code and data dependencies, irreversible effect
boundaries and roll-forward repair options. A code generation can be selected again
without making its readers compatible with new state. Canary traffic and shadow
traffic have distinct authority.

### Admission, transitions and completion

Run shadow validation without live effect imports. Give real canaries unique
admitted work with ordinary outcome tracking. Before rollback, verify old readers,
workflow definitions, outcome lookup and required adapters remain valid for all new
writes. After an irreversible boundary, switch only under an explicit roll-forward
or compensation contract. Retire old artifacts after their dependency closure is
empty or policy explicitly changes.

### Failure and adversarial behavior

A duplicate canary payment cannot be undone by routing users back. Garbage
collection may delete old readers before the rollback window closes. Metrics
indicating a healthy process do not establish that every accepted workflow remains
completable.

### Alternatives and unresolved tradeoffs

Long rollback windows improve operational flexibility but retain storage, code and
security exposure. Early contraction reduces cost but narrows recovery choices.
Select windows from actual persistent dependencies and effect semantics, not a fixed
number of releases.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Attempt rollback after an unreadable new write and after an irreversible effect; both must produce the declared refusal or repair path.
- Retire a generation with a live old compensation dependency; collection must remain blocked or preserve a qualified replacement.

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

1. [NixOS](../../../30-sources/dolstra-et-al-2008-nixos.md).
2. [Parallel Change](../../../30-sources/sato-2014-parallel-change.md).
