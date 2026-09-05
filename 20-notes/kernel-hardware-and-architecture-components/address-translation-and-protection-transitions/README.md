---
title: "Address translation and protection transition components"
kind: map
created: "2026-09-04"
tags:
  - architecture-support
  - archive-navigation
  - directory-index
  - virtual-memory
aliases:
  - "Address-translation component reports"
---

# Address translation and protection transition components (`address-translation-and-protection-transitions`)

## Purpose

This directory contains the detailed implementation research for the nine
internal services proposed by [Address translation and protection
transitions](../address-translation-and-protection-transitions.md), component 3
of the kernel hardware and architecture support layer.

## What belongs here

Put subcomponent-level syntheses here when they develop one part of address-
space identity, validation, encoding, transaction execution, context tags,
invalidation, cross-CPU shootdown, reclamation, or privileged user access in
enough detail to state its evidence, objects, state machine, failure behavior,
cross-ISA obligations, and falsification plan. Keep the integrated transition
protocol in the parent component note.

Across the reports, `AddressSpaceIncarnation` always means the nominal compound
`(object_id, incarnation_generation)`, and a CPU target always means
`(cpu_identity, cpu_incarnation)`. A bare generation or recycled numeric CPU
identifier is never stable identity.

## Index

### Subdirectories

- None yet.

### Documents

- [Address-space object](address-space-object.md) — defines a sealed,
  capability-backed address-space identity with eleven separately typed
  domains: address-space incarnation, capability, mapping, mutation sequence,
  translation-catch-up incarnation, user-access borrow, context tag, reference
  admission, execution admission, code publication, and terminal completion.
- [Mapping validator](mapping-validator.md) — turns untrusted declarative
  requests into reserved, revalidatable plans while enforcing authority,
  range, permission, alias, memory-type, and quota invariants.
- [Page-table and protection encoder](page-table-and-protection-encoder.md) —
  confines raw entry construction and architecture-specific representability
  to a typed backend with explicit publication and hardware-owned-bit rules.
- [Mapping transaction](mapping-transaction.md) — defines preparation,
  acceptance, publication, invalidation, terminal failure, cancellation, and
  batching as one resource-owning operation.
- [Translation-context allocator](translation-context-allocator.md) — manages
  finite ASID/PCID-like namespaces as generation-tagged leases with explicit
  rollover and CPU-installation state.
- [Translation invalidation planner](invalidation-planner.md) — selects and records the
  least costly sound local and remote invalidation effect, with conservative
  strengthening under uncertainty or queue pressure.
- [Shootdown coordinator](shootdown-coordinator.md) — freezes incarnation-
  aware target sets, executes bounded per-CPU work, and separates transport,
  user-return closure, local maintenance, aggregate CPU-translation quiescence,
  lifecycle exclusion, and incomplete results.
- [Reclamation gate](reclamation-gate.md) — joins CPU, walker, software-reader,
  privileged-borrow, reference, executable-code, and DMA quiescence evidence
  before any identity, frame, or page-table memory is reused.
- [Safe user-access helpers](safe-user-access-helpers.md) — provides bounded,
  fault-recoverable, snapshot-aware copying without raw user pointers or an
  ambient privileged alias to user-owned frames.

## Maintaining this index

Inventory every direct report and keep the nine-service decomposition aligned
with the parent component. Whenever a report is added, renamed, moved,
archived, or superseded, update this index, the parent component index, the
kernel architecture map, the open inquiry, and the relevant deep-dive journal.
