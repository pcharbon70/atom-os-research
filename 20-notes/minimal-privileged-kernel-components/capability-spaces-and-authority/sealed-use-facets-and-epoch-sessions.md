---
title: "Sealed use facets and epoch sessions"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Sealed use facets and epoch sessions

How can a replaceable recovery manager use authority without duplicating or exporting its control epoch?

## Research basis and status

Typed capability mechanisms are the substrate; sealed recovery facets and session intersections are proposed extensions. [1](../../../30-sources/sel4-foundation-2026-reference-manual.md), [2](../../../30-sources/zig-project-2026-language-reference-0-16.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../capability-spaces-and-authority.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

RecoveryLease.Use and ResetLease.Use are protected kernel facets with generation, current epoch, owning capability space and operation family. A Zig copy of a selector is not a new protected facet, but every invocation still checks the current epoch. Ordinary mint, copy and transfer operations must reject these facet types.

### Admission, transitions and completion

Derive a narrow session from the intersection of a current lease and separately held target authority. Bind it to the exact operation scope and close its anchor when takeover advances the lease epoch. Check the session again at a recipient's mutation commit boundary. Inspection, lifecycle, reset and publication rights remain distinct; one lease must not imply all of them.

### Failure and adversarial behavior

An old manager can resume after a successor starts. Checking its lease only when opening a long-lived connection leaves stale requests usable unless the connection carries a closeable session or commit-time fence. Kernel-enforced non-transferability also fails if a generic serialization helper exports an equivalent privileged handle.

### Alternatives and unresolved tradeoffs

Checking the lease for every operation is simple but adds repeated lookup. A cached session can reduce overhead only if its closure and already-admitted effects are precisely defined. Neither choice fences direct MMIO aliases or unfenceable external services by itself.

## Verification obligations

Copy selector bytes, attempt protected-cap duplication, replay old sessions and pause a manager before recipient commit. Require stale rejection and no rights amplification. Separately test an old already-admitted hardware operation whose valid completion must remain attributable to its original operation epoch.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Lifetime groups and activation pins](../typed-object-storage-and-explicit-memory/lifetime-groups-and-activation-pins.md) — Lookup admission must acquire a safe object lifetime.
- [Lease takeover and operation adoption](../failure-boundaries-and-recovery-topology/lease-takeover-and-operation-adoption.md) — Current authority and original operation identity remain distinct.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Zig 0.16.0 language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — comparative evidence; its methods and limits are recorded in the source note.
