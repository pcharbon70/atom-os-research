---
title: "Notes"
kind: map
created: "2026-08-28"
tags:
  - archive-navigation
  - directory-index
aliases:
  - "Notes index"
---

# Notes (`20-notes`)

## Purpose

Notes preserve ideas, arguments, models, and syntheses in the author's own
words.

## What belongs here

Put independently useful conclusions and developing interpretations here.
Source summaries belong in `30-sources`; unresolved workbenches belong in
`40-inquiries`.

## Index

### Subdirectories

- None yet.

### Documents

- [Address translation and protection transitions](address-translation-and-protection-transitions.md) —
  proposes typed mapping transactions, centralized page-table mutation,
  generation-safe translation tags, explicit shootdown completion, and
  quiescence-gated reclamation across MMU and MPU/PMP profiles.
- [Architecture faults and diagnostics](architecture-faults-and-diagnostics.md) —
  proposes preallocated staging and terminal capture, typed decoding and
  recovery policy, and distinct local-resume versus coordinated-containment
  proofs.
- [AtomVM as an operating-system foundation](atomvm-as-an-operating-system-foundation.md) — assesses the
  current runtime boundary, empirical limits, missing OS responsibilities, and
  a proposed minimal-substrate architecture.
- [BEAM, ERTS, and OTP principles for a new operating system](beam-erts-and-otp-principles-for-a-new-operating-system.md) —
  separates the three layers, makes compiled-BEAM compatibility and
  process-local tracing collection explicit, identifies needed security and
  resource-control changes, and proposes a layered architecture.
- [Interrupt event fabric](interrupt-event-fabric.md) — models interrupt
  sources as flow-specific, generation-bound state machines with bounded event
  delivery, explicit completion, rebinding, overflow, and quarantine.
- [Kernel hardware and architecture support layer](kernel-hardware-and-architecture-support-layer.md) —
  develops the kernel-level contracts for privileged entry, execution context,
  translation, ordering and code publication, interrupts, time, logical CPUs,
  protected I/O, faults, and a portable typed facade.
- [Logical-CPU coordination and lifecycle](logical-cpu-coordination-and-lifecycle.md) —
  develops stable CPU identity, lifecycle generations, staged start and stop,
  acknowledged request sets, participation guards, and quarantine after
  incomplete removal.
- [Minimal privileged kernel layer](minimal-privileged-kernel-layer.md) —
  proposes a capability microkernel with explicit object memory, first-class
  execution-stop domains, bounded IPC and CPU budgets, revocation anchors,
  structured fault routes, and quiescence- or quarantine-gated recovery.
- [Normalized boot handoff and feature discovery](normalized-boot-handoff-and-feature-discovery.md) —
  treats boot and firmware inputs as untrusted provider claims and seals
  validated, bounded, provenance-carrying facts into an immutable snapshot.
- [Ordering, coherence, and code publication](ordering-coherence-and-code-publication.md) —
  keeps compiler, memory, device, DMA, translation, and instruction-fetch
  ordering distinct and gives executable code an explicit publication and
  retirement lifecycle.
- [Privileged entry, exit, and execution context](privileged-entry-exit-and-execution-context.md) —
  develops generated frame layouts, dedicated exceptional stacks, eager
  isolation of enabled processor state, and hostile return-frame validation.
- [Protected I/O and DMA ownership](protected-io-and-dma-ownership.md) —
  composes requester sets, mappings, buffers, queues, interrupts, reset, and
  quiescence into a revocable protected-I/O lifecycle.
- [Raw time and deadline programming](raw-time-and-deadline-programming.md) —
  separates monotonic counter and one-shot deadline mechanisms from clock
  conversion, timer queues, scheduling policy, and civil time.
- [Typed kernel-facing architecture facade](typed-kernel-facing-architecture-facade.md) —
  exposes architecture mechanisms through sealed generational objects, typed
  contexts, split-phase tokens, explicit feature profiles, and backend
  conformance tests.
- [Unsafe architecture-primitives capsule](unsafe-architecture-primitives-capsule.md) —
  confines privileged instructions, inline assembly, and raw architecture
  representations behind narrow reviewed safety contracts and generated-code
  checks.

## Maintaining this index

Index every direct note and describe its claim or role. Keep maturity values
honest and connect each note to evidence, related notes, or a map.
