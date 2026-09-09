---
title: "Selector resolution and admission"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Selector resolution and admission

What must a successful capability lookup prove at the exact point an operation becomes admitted?

## Research basis and status

The seL4 manual supplies typed capability-space precedent; the integrated admission gate is Atom's proposed contract. [1](../../../30-sources/sel4-foundation-2026-reference-manual.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../capability-spaces-and-authority.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A selector is a slot index and generation interpreted only in its current CSpace. The protected entry names an object generation, type, rights, facet, stable lineage and bounded anchor path. A reported object identifier is not a portable capability, and a badge identifies a selected endpoint facet rather than authenticating an arbitrary sender identity.

### Admission, transitions and completion

Walk a bounded-depth, caller-funded table; validate slot and object generations; pin the entry and object; then check required rights, current anchors, domain gates and object lifecycle. Admission and closure must have an unambiguous order. The pin proves that an already admitted operation may finish according to its operation schema, not that it may create unrestricted future authority.

### Failure and adversarial behavior

Checking a generation only after dereferencing backing is too late. Cached validity must be invalidated by the same closure protocol or restricted to one pinned activation. Reusing a slot must not let a stale selector acquire a new object, even when type and rights happen to match.

### Alternatives and unresolved tradeoffs

A shallow radix table bounds lookup work at the cost of explicitly allocated intermediate nodes. A flat table simplifies checking but can waste addressable capacity. Either choice needs a language-level concurrency model; volatile fields do not provide a publication protocol.

## Verification obligations

Race slot reuse, object close and anchor closure at every lookup step. Attempt cross-CSpace selector reuse and type confusion. Check that every success identifies one protected generation and every operation admitted after closure is rejected, without dereferencing reclaimed storage.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Lifetime groups and activation pins](../typed-object-storage-and-explicit-memory/lifetime-groups-and-activation-pins.md) — Lookup admission must acquire a safe object lifetime.
- [Lease takeover and operation adoption](../failure-boundaries-and-recovery-topology/lease-takeover-and-operation-adoption.md) — Current authority and original operation identity remain distinct.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
