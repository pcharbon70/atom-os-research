---
title: "Workflow-generation handoff and publication fences"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Workflow-generation handoff and publication fences

This study decomposes [Application evolution, schema compatibility, and migration](../application-evolution-schema-compatibility-and-migration.md).

Research question: How do accepted operations cross a release boundary without acquiring two owners or none?

## Research basis and status

Sagas permit visible intermediate commits and semantic compensation; they do not supply outer transaction isolation. [1](../../../30-sources/garcia-molina-salem-1987-sagas.md).

NixOS separates immutable configuration generations from mutable activation effects; selecting an old generation does not undo domain state. [2](../../../30-sources/dolstra-et-al-2008-nixos.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the handoff inventory of old operation IDs, workflow states, compensation
definitions, effect intents and status lookup routes. Layer 4 owns the atomic route
and datastore writer-generation transition. Layer 5 certifies that each accepted
responsibility is terminal or assigned to a compatible new owner.

### Admission, transitions and completion

Close old write admission, reach the declared safe state, finish or durably transfer
outstanding responsibilities and validate the transfer against current state.
Atomically advance writer fence and publication generation. Old non-writing cleanup
may drain afterward, but every mutation path must reject the obsolete fence.

### Failure and adversarial behavior

Publishing first and draining writers later permits simultaneous authority over
incompatible state. A workflow may depend on an old compensation adapter even if its
next forward step uses the new protocol. A failed handoff must keep publication
closed; reopening old admission is safe only while its authority remains current.

### Alternatives and unresolved tradeoffs

Letting old workflows finish under retained code avoids many transforms but
increases coexistence cost. State-specific handoff can reduce that lifetime while
enlarging verification. Generic code replacement without an obligation inventory is
not a migration strategy.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Crash between responsibility transfer and publication; exactly one authoritative owner remains discoverable for each accepted operation.
- Resume an old writer after publication and invoke an old compensation; validate distinct mutation and retained-repair permissions.

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

1. [Sagas](../../../30-sources/garcia-molina-salem-1987-sagas.md).
2. [NixOS](../../../30-sources/dolstra-et-al-2008-nixos.md).
