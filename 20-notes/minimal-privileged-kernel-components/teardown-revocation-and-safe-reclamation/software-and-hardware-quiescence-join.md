---
title: "Software and hardware quiescence join"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Software and hardware quiescence join

Which combination of evidence is sufficient to say that old effects cannot reach reusable memory?

## Research basis and status

Hazard pointers and epoch reclamation address software access, while their progress assumptions expose the limits of forced cleanup. [1](../../../30-sources/michael-2004-hazard-pointers.md), [2](../../../30-sources/brown-2015-reclaiming-lock-free-memory.md), [3](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../teardown-revocation-and-safe-reclamation.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

The completion join names software activations, capability lineage, execution-stop acknowledgements, translation invalidations, IRQ/timer drainage and device-specific completion tokens. Each item carries the original object/operation generation and participant identity. Absence of an effect class is valid only if the constructor made that effect impossible.

### Admission, transitions and completion

Close admission first, then gather each completion through its owning subsystem. A software grace period removes old reader access but does not replace a CPU-domain stop or hardware invalidation. Join only evidence matching the immutable operation and exact target set. Late valid completions can advance the old operation after manager takeover, while stale mutations remain fenced.

### Failure and adversarial behavior

Force-clearing a stalled reader may hide an interrupted kernel invariant. A CPU reset without checkpoint recovery cannot safely certify its locks and references. A device timeout cannot stand in for DMA completion. Any such unsupported substitution invalidates the reuse claim even if most branches finished.

### Alternatives and unresolved tradeoffs

Explicit pins provide precise retention but add per-activation state; epoch schemes can reduce read cost while coupling reclamation to stalled participants. The join should accept either proven software discipline without confusing it with the separate hardware classes.

## Verification obligations

Satisfy every branch except one, in turn, and require retention. Reincarnate a CPU or object before delivering old evidence. Test that a node-fatal checkpoint failure cannot be downgraded to successful domain-only cleanup.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Sanitization and generation-safe reuse](../typed-object-storage-and-explicit-memory/sanitization-and-generation-safe-reuse.md) — Only the allocator completes sanitization and fresh publication.
- [Device completion and reset composition](../memory-mappings-and-architecture-resource-bindings/device-completion-and-reset-composition.md) — Device-specific graphs supply physical completion evidence.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Hazard pointers: Safe memory reclamation for lock-free objects](../../../30-sources/michael-2004-hazard-pointers.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Reclaiming memory for lock-free data structures: there has to be a better way](../../../30-sources/brown-2015-reclaiming-lock-free-memory.md) — comparative evidence; its methods and limits are recorded in the source note.
3. [Read-copy update: Using execution history to solve concurrency problems](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md) — comparative evidence; its methods and limits are recorded in the source note.
