---
title: "Lifetime groups and activation pins"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Lifetime groups and activation pins

How are object lifetime ownership and temporary dereference safety represented independently?

## Research basis and status

Hazard pointers and RCU provide alternative software-reference disciplines, with different retention costs. [1](../../../30-sources/michael-2004-hazard-pointers.md), [2](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md), [3](../../../30-sources/brown-2015-reclaiming-lock-free-memory.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../typed-object-storage-and-explicit-memory.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A LifetimeGroup records who is responsible for terminal cleanup; an activation pin records a particular admitted kernel use. Neither is equivalent to the number of capabilities. The object header retains its immutable identity and closure state while pins and dependent products remain.

### Admission, transitions and completion

Make lookup-to-pin acquisition atomic with respect to admission closure. A pin holder accesses only the protected generation and releases at a declared checkpoint. Closing the group rejects new relationships, then delegates enumeration to the charged reaper. Shared objects need explicit lifetime consent: deleting one user's last cap must not destroy an object that independent users legitimately retain.

### Failure and adversarial behavior

Incrementing a reference counter after an unprotected pointer load can touch freed memory. Conversely, a stalled pin can safely retain storage forever while defeating an availability goal. Force-clearing it is permitted only after execution and checkpoint evidence proves no later dereference; resetting a CPU does not automatically restore interrupted kernel invariants.

### Alternatives and unresolved tradeoffs

A coarse lock plus bounded pins is easier to audit than a universal lock-free framework. Hazard-style slots constrain retained references; epoch schemes can make reads cheaper but amplify stalled-participant retention. The choice must name participant bounds and exceptional-context behavior.

## Verification obligations

Pause immediately between selector lookup and pin publication; close and attempt reuse from another CPU. Stall one holder while unrelated objects are reclaimed. Check safety, retained-storage accounting and admission backpressure separately rather than treating a safe leak as successful recovery.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Quarantine custody and reuse release](../teardown-revocation-and-safe-reclamation/quarantine-custody-and-reuse-release.md) — The reaper proves eligibility; the allocator performs final reuse.
- [Product authority and durable detachment](../capability-spaces-and-authority/product-authority-and-durable-detachment.md) — Creation must attach the correct lifetime dependencies.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Hazard pointers: Safe memory reclamation for lock-free objects](../../../30-sources/michael-2004-hazard-pointers.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Read-copy update: Using execution history to solve concurrency problems](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md) — comparative evidence; its methods and limits are recorded in the source note.
3. [Reclaiming memory for lock-free data structures: there has to be a better way](../../../30-sources/brown-2015-reclaiming-lock-free-memory.md) — comparative evidence; its methods and limits are recorded in the source note.
