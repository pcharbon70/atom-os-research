---
title: "Capability spaces and authority: internal services"
kind: map
created: "2026-09-09"
tags: [archive-navigation, directory-index, kernel-internal-services, microkernels]
aliases: []
---

# Capability spaces and authority: internal services

## Purpose

Resolve current typed authority, fund its propagation and preserve effect-bearing lifetime dependencies through logical closure and eventual revocation.

This directory decomposes [component 2: Capability spaces and authority](../capability-spaces-and-authority.md) into 5 internal-service studies. The parent remains the integrated contract; these are research boundaries, not necessarily separate privileged processes, exported APIs or source modules.

## What belongs here

Include service-level ownership, authority, transition, failure, alternative and verification analysis. Keep machine instruction/register contracts in the [hardware architecture layer](../../kernel-hardware-and-architecture-components/README.md), and keep BEAM execution, process-local tracing GC and supervision policy outside the privileged kernel. This work concerns the full system architecture, independently of PoC or emulator qualification.

## Composition obligations

Each service names its own state without duplicating its parent's lifecycle authority. Admission must allocate the metadata needed to track eventual cleanup. Logical rejection of new work, completion of old work, custody transfer and physical reuse are distinct results. Bounds depend on admitted participants, resources and hardware profiles; no universal latency is claimed.

The decomposition count follows the distinct state owners and failure/completion contracts below, not a fixed quota. The reports deliberately retain unresolved choices and unexecuted tests. Zig remains selected, but no compiler version or language feature substitutes for protected-state, concurrency or hardware proofs.

## Index

### Subdirectories

- None yet.

### Documents

- [Selector resolution and admission](selector-resolution-and-admission.md) — What must a successful capability lookup prove at the exact point an operation becomes admitted?
- [Slot mutation and consented transfer](slot-mutation-and-consented-transfer.md) — How can authority be delegated without allowing a sender to exhaust or overwrite a receiver's namespace?
- [Lineage and one-way revocation anchors](lineage-and-one-way-revocation-anchors.md) — How can future admission stop promptly while a large derivation structure is cleaned incrementally?
- [Product authority and durable detachment](product-authority-and-durable-detachment.md) — Which input authorities must continue to constrain a newly created object after its constructor returns?
- [Sealed use facets and epoch sessions](sealed-use-facets-and-epoch-sessions.md) — How can a replaceable recovery manager use authority without duplicating or exporting its control epoch?

## Cross-component connections

- [Lifetime groups and activation pins](../typed-object-storage-and-explicit-memory/lifetime-groups-and-activation-pins.md) — Lookup admission must acquire a safe object lifetime.
- [Lease takeover and operation adoption](../failure-boundaries-and-recovery-topology/lease-takeover-and-operation-adoption.md) — Current authority and original operation identity remain distinct.

The [minimal-kernel map](../../../10-maps/minimal-privileged-kernel.md) provides selective routes; the [session journal](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) contains the exhaustive source manifest. The [contract inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) remains open.

## Maintaining this index

Inventory every direct service report and child directory. Update the parent component, [component inventory](../README.md), relevant map and meaningful incoming links together whenever a service is added, moved or renamed. Preserve the distinction between documented coverage and demonstrated correctness.
