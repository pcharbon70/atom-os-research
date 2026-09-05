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

This directory collects the detailed implementation research for the eleven
components numbered 0 through 10 in the [kernel hardware and architecture
support layer](../kernel-hardware-and-architecture-support-layer.md).

## What belongs here

Put component-level architecture syntheses here when they develop one part of
the hardware-support boundary in enough detail to require its own evidence,
objects, state machines, cross-ISA realization, failure analysis, and
verification plan. Keep the integrated layer model and other broad operating-
system syntheses in the parent notes directory.

## Index

### Subdirectories

- [Address translation and protection transition components](address-translation-and-protection-transitions/README.md) —
  contains nine detailed internal-service reports for component 3, covering
  address-space identity through safe privileged user access.

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
  develops preallocated staging and terminal capture, typed decoding, and
  distinct local-resume and coordinated-containment proofs.
- [10. Typed kernel-facing architecture facade](typed-kernel-facing-architecture-facade.md) —
  exposes the components through sealed generational objects, typed contexts,
  split-phase tokens, explicit profiles, and backend conformance tests.

## Maintaining this index

Inventory every direct component note, preserve the 0-through-10 numbering,
and update the parent notes index and architecture-support map whenever a
component is added, renamed, moved, archived, or superseded.
