---
title: "Copying collection reserve and resumable progress"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - actor-model
  - beam
  - managed-runtime
  - system-architecture
aliases: []
---

# Copying collection reserve and resumable progress

This study decomposes [Terms, private heaps, shared binaries and tracing collection](../terms-private-heaps-shared-binaries-and-tracing-collection.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

The incremental Erlang study couples collection progress to allocation; resource-container work motivates charging collector work to the activity that causes it. [1](../../../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md), [2](../../../30-sources/banga-et-al-1999-resource-containers.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Automatic tracing collection and term interpretation remain unprivileged runtime responsibilities; kernel pages do not encode BEAM object ownership.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own the collection cycle, reserved destination capacity, forwarding/work queues and commit marker. A partially moved heap is a collector-owned state, not a normal mutator state. Automatic reachability tracing is mandatory; reference counting shared exceptions does not replace it.

### Admission, transitions and completion

Reserve enough space for the selected collection strategy before installing forwarding state. Trace exact roots, copy reachable objects, reconcile shared references and commit new roots/bounds together. Release old storage only after no residual root or operation can access it. If the collector is sliced, persist its cursor and rooting obligations explicitly.

### Failure and adversarial behavior

Post-hoc reduction charging does not bound one long tracing loop. A collector that yields to other actors can keep its own mutator stopped; allowing that mutator to resume during collection additionally needs a proved barrier/replication protocol. OOM after destructive forwarding cannot be handled by blindly resuming the old heap.

### Alternatives and unresolved tradeoffs

Stop-the-actor copying is the clearest baseline but large live graphs cause long pauses. Incremental collection adds metadata, reserve and proof costs. The historical hybrid collector does not establish a ready-made incremental implementation for this private-heap design.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Sweep high live ratios and root counts while measuring worst observed non-yielding intervals.
- Fail each reservation before forwarding and require an intact old heap.
- Pause at every proposed collection slice; verify no mutator sees half-forwarded state.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Root materialization](../code-execution-safe-points-and-version-publication/canonical-safe-point-and-native-helper-state.md) — a contract this service must compose with.
- [Physical and retained accounting](../resource-accounting-and-overload-control/hierarchical-reservations-and-ledger-reconciliation.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [Sagonas and Wilhelmsson: memory management](../../../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md).
2. [Resource containers](../../../30-sources/banga-et-al-1999-resource-containers.md).
