---
title: "Lineage and one-way revocation anchors"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Lineage and one-way revocation anchors

How can future admission stop promptly while a large derivation structure is cleaned incrementally?

## Research basis and status

Recursive revocation cost motivates comparing kernel-held closure anchors with user-level delegation policy. [1](../../../30-sources/parmer-2016-capability-based-os-design.md), [2](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../capability-spaces-and-authority.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A stable lineage node is not a reusable cap slot. A RevocationAnchor has a protected identity, monotonic epoch and one-way OPEN-to-CLOSED state. Entries retain the bounded anchor path that governs them, and tombstones remain funded while descendants, pins or cursors can still reference the old lineage.

### Admission, transitions and completion

Close the selected anchor at one admission linearization point. All later acquisitions through that anchor fail, while earlier admitted operations remain recorded. Traverse descendant entries in charged slices, checking generation and cursor identity on resumption. Physical deletion releases references only after concurrent users are excluded; logical close does not synchronously enumerate every descendant.

### Failure and adversarial behavior

Reopening an anchor resurrects copies that may be unreachable to the current owner. Treat renewed access as a new authority generation instead. Traversing first and closing last permits delegation to outrun revocation. Saying revocation is constant-time is misleading: only the bounded gate publication has that property; traversal and effect drainage depend on admitted state.

### Alternatives and unresolved tradeoffs

A user-level manager can track delegation outside the kernel, reducing privileged policy but adding reliance on that manager's availability and correctness. Kernel anchors retain a narrow deny-new-admission invariant while leaving recovery policy outside. Their path-length bound and storage cost need analysis.

## Verification obligations

Continuously copy and mint while closing an ancestor; move entries during cursor traversal; delete an intermediate parent before its descendants. Require no post-close admission and no tombstone reuse until the last reference, while unrelated anchor trees remain usable.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Lifetime groups and activation pins](../typed-object-storage-and-explicit-memory/lifetime-groups-and-activation-pins.md) — Lookup admission must acquire a safe object lifetime.
- [Lease takeover and operation adoption](../failure-boundaries-and-recovery-topology/lease-takeover-and-operation-adoption.md) — Current authority and original operation identity remain distinct.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Capability-based OS Design](../../../30-sources/parmer-2016-capability-based-os-design.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Read-copy update: Using execution history to solve concurrency problems](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md) — comparative evidence; its methods and limits are recorded in the source note.
