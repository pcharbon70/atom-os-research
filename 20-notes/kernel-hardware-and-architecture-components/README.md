---
title: "Kernel hardware and architecture components"
kind: map
created: "2026-09-02"
tags:
  - architecture-support
  - archive-navigation
  - directory-index
  - operating-systems
aliases:
  - "Kernel architecture component notes"
---

# Kernel hardware and architecture components (`kernel-hardware-and-architecture-components`)

## Purpose

This directory collects the detailed system-architecture research for the eleven
components numbered 0 through 10 in the [kernel hardware and architecture
support layer](../kernel-hardware-and-architecture-support-layer.md).

All eleven components now have internal-service research decompositions:
70 reports in total. These develop the full system architecture, independently
of delivery milestones or emulator qualification. They preserve the parent
components' integrated protocols and do not constitute implementation evidence.

## What belongs here

Put component-level architecture syntheses here when they develop one part of
the hardware-support boundary in enough detail to require its own evidence,
objects, state machines, cross-ISA realization, failure analysis, and
verification plan. Keep the integrated layer model and other broad operating-
system syntheses in the parent notes directory.

## Index

### Subdirectories

- [0. Normalized boot handoff and feature discovery: internal services](normalized-boot-handoff-and-feature-discovery/README.md) —
  contains 6 architecture-service reports with ownership, protocols,
  failure analysis, cross-ISA obligations and unexecuted falsification tests.
- [1. Unsafe architecture-primitives capsule: internal services](unsafe-architecture-primitives-capsule/README.md) —
  contains 5 architecture-service reports with ownership, protocols,
  failure analysis, cross-ISA obligations and unexecuted falsification tests.
- [2. Privileged entry, exit and execution context: internal services](privileged-entry-exit-and-execution-context/README.md) —
  contains 6 architecture-service reports with ownership, protocols,
  failure analysis, cross-ISA obligations and unexecuted falsification tests.
- [3. Address translation and protection transition components](address-translation-and-protection-transitions/README.md) —
  contains nine detailed internal-service reports, covering address-space
  identity through safe privileged user access.
- [4. Ordering, coherence and code publication: internal services](ordering-coherence-and-code-publication/README.md) —
  contains 7 architecture-service reports with ownership, protocols,
  failure analysis, cross-ISA obligations and unexecuted falsification tests.
- [5. Interrupt event fabric: internal services](interrupt-event-fabric/README.md) —
  contains 6 architecture-service reports with ownership, protocols,
  failure analysis, cross-ISA obligations and unexecuted falsification tests.
- [6. Raw time and deadline programming: internal services](raw-time-and-deadline-programming/README.md) —
  contains 6 architecture-service reports with ownership, protocols,
  failure analysis, cross-ISA obligations and unexecuted falsification tests.
- [7. Logical-CPU coordination and lifecycle: internal services](logical-cpu-coordination-and-lifecycle/README.md) —
  contains 6 architecture-service reports with ownership, protocols,
  failure analysis, cross-ISA obligations and unexecuted falsification tests.
- [8. Protected I/O and DMA ownership: internal services](protected-io-and-dma-ownership/README.md) —
  contains 7 architecture-service reports with ownership, protocols,
  failure analysis, cross-ISA obligations and unexecuted falsification tests.
- [9. Architecture fault and diagnostic components](architecture-faults-and-diagnostics/README.md) —
  contains six detailed internal-service reports, covering bounded raw capture
  through recursive-fault termination and evidence custody.
- [10. Typed kernel-facing architecture facade: internal services](typed-kernel-facing-architecture-facade/README.md) —
  contains 6 architecture-service reports with ownership, protocols,
  failure analysis, cross-ISA obligations and unexecuted falsification tests.

### Documents

- [0. Normalized boot handoff and feature discovery](normalized-boot-handoff-and-feature-discovery.md) —
  treats boot inputs as untrusted claims and seals validated, bounded,
  provenance-carrying facts into an immutable snapshot.
- [1. Unsafe architecture-primitives capsule](unsafe-architecture-primitives-capsule.md) —
  confines privileged instructions, inline assembly, and raw architecture
  representations behind narrow reviewed contracts.
- [2. Privileged entry, exit, and execution context](privileged-entry-exit-and-execution-context.md) —
  develops generated frame layouts, dedicated exceptional stacks, explicit
  state ownership, and hostile return-frame validation.
- [3. Address translation and protection transitions](address-translation-and-protection-transitions.md) —
  develops typed mapping transactions, generation-safe translation tags,
  acknowledged shootdowns, and quiescence-gated reclamation.
- [4. Ordering, coherence, and code publication](ordering-coherence-and-code-publication.md) —
  separates memory and device-ordering contracts and gives executable code an
  explicit cross-CPU publication and retirement lifecycle.
- [5. Interrupt event fabric](interrupt-event-fabric.md) — models interrupt
  sources as flow-specific, generation-bound state machines with bounded
  delivery, completion, rebinding, overflow, and quarantine.
- [6. Raw time and deadline programming](raw-time-and-deadline-programming.md) —
  separates counter continuity and conversion from one-shot deadline channels,
  scheduling policy, and civil time.
- [7. Logical-CPU coordination and lifecycle](logical-cpu-coordination-and-lifecycle.md) —
  develops stable CPU identity, staged start and stop, acknowledged request
  sets, participation guards, and quarantine after incomplete removal.
- [8. Protected I/O and DMA ownership](protected-io-and-dma-ownership.md) —
  composes requester sets, mappings, buffers, queues, interrupts, reset, and
  quiescence into a revocable protected-I/O lifecycle.
- [9. Architecture faults and diagnostics](architecture-faults-and-diagnostics.md) —
  develops preallocated staging and terminal capture, a separate deferred
  decoder and capture-time disposition gate, explicit sink/custody claims, and
  distinct local-resume and coordinated-containment proofs.
- [10. Typed kernel-facing architecture facade](typed-kernel-facing-architecture-facade.md) —
  exposes the components through sealed generational objects, typed contexts,
  split-phase tokens, explicit profiles, and backend conformance tests.

## Maintaining this index

Inventory every direct component note, preserve the 0-through-10 numbering,
and update the parent notes index and architecture-support map whenever a
component is added, renamed, moved, archived, or superseded.
