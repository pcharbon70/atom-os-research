---
title: "Backing pools and retyping"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Backing pools and retyping

How can memory become typed kernel objects without introducing hidden allocation authority?

## Research basis and status

The untyped-memory model supplies a precedent for caller-supplied object backing. [1](../../../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md), [2](../../../30-sources/sel4-foundation-2026-reference-manual.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../typed-object-storage-and-explicit-memory.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A backing pool owns a disjoint physical extent and a checked partition of that extent. Retyping consumes available child ranges into immutable object types. Pool ownership does not confer authority over live object contents, and an object capability does not permit arbitrary reinterpretation of its backing.

### Admission, transitions and completion

Validate alignment, size, type-layout version and overlap against protected pool metadata. Split into charged child extents and reserve object headers before construction. Use fixed-layout slabs for small metadata and explicitly supplied contiguous ranges for larger types. A parent range may merge only after all children have reached physically reusable state; logical deletion is insufficient. Preserve non-RAM profiles that prohibit ordinary zero-and-reuse treatment.

### Failure and adversarial behavior

Allocator coalescing based only on an empty capability table can alias a still-active mapping or retired object. Moving a live object also invalidates internal references unless an independent relocation protocol exists; the baseline should not silently compact live kernel storage. Generation exhaustion retires the affected identity instead of wrapping.

### Alternatives and unresolved tradeoffs

Buddy-style splitting provides simple disjointness arguments but internal fragmentation. Per-type slabs reduce waste while introducing slab occupancy and final-page release obligations. Compare both with measured metadata pressure, not just allocation throughput.

## Verification obligations

Exercise split/merge permutations, misaligned sizes, overlapping grants and child objects retained by delayed teardown. Require unique backing ownership and no parent reuse before the last child's release receipt. Measure fragmentation separately from charged live and retained bytes.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Quarantine custody and reuse release](../teardown-revocation-and-safe-reclamation/quarantine-custody-and-reuse-release.md) — The reaper proves eligibility; the allocator performs final reuse.
- [Product authority and durable detachment](../capability-spaces-and-authority/product-authority-and-durable-detachment.md) — Creation must attach the correct lifetime dependencies.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Kernel design for isolation and assurance of physical memory](../../../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
