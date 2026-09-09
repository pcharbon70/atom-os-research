---
title: "Object creation and publication"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Object creation and publication

How can a multi-input constructor either publish one fully owned object or have no externally visible effect?

## Research basis and status

Explicit allocation and typed capability mechanisms provide the comparison; Atom's multi-input transaction is a separate proposal. [1](../../../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md), [2](../../../30-sources/sel4-foundation-2026-reference-manual.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../typed-object-storage-and-explicit-memory.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

The constructor owns a private ObjectHeader, reservation set and proposed initial capability. Immutable type, identity generation, payer, lifetime group, anchors and effect-ledger capacity must exist before publication. A successful allocation alone is not a successful object creation.

### Admission, transitions and completion

Resolve and pin every input authority, validate type and rights, compute the product's inherited anchors, and reserve backing plus indirect metadata. Initialize privately, then commit account debit, pool consumption, lifetime attachment and initial cap publication as one logical operation. The implementation may use a short lock-based critical section, but no fallible allocation or arbitrary callback belongs inside it.

### Failure and adversarial behavior

Closing an input after validation but before publication must compete with the same admission decision; a cached rights check cannot authorize a new product after closure. If a failure occurs before commit, restore every reservation. If completion reporting fails after commit, preserve the existing object identity and provide reconciliation rather than rerunning the constructor blindly.

### Alternatives and unresolved tradeoffs

A universal generic constructor reduces duplicated checks but risks hiding type-specific effect rules. Prefer a common transaction skeleton with explicit per-type schemas, checked at review and in executable models. Zig error unions describe failure outcomes but do not enforce transaction rollback.

## Verification obligations

Inject exhaustion at each reservation, close every input at each publication boundary, and lose the success reply. Check conservation of backing and quotas, exactly one published identity, and explicit distinction between rejection and committed-but-unobserved creation.

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
