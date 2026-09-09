---
title: "Bootstrap and root-authority handoff: internal services"
kind: map
created: "2026-09-09"
tags: [archive-navigation, directory-index, kernel-internal-services, microkernels]
aliases: []
---

# Bootstrap and root-authority handoff: internal services

## Purpose

Turn sealed machine facts and an authorized construction description into a private, audited authority graph, then permanently remove bootstrap admission.

This directory decomposes [component 0: Bootstrap and root-authority handoff](../bootstrap-and-root-authority-handoff.md) into 5 internal-service studies. The parent remains the integrated contract; these are research boundaries, not necessarily separate privileged processes, exported APIs or source modules.

## What belongs here

Include service-level ownership, authority, transition, failure, alternative and verification analysis. Keep machine instruction/register contracts in the [hardware architecture layer](../../kernel-hardware-and-architecture-components/README.md), and keep BEAM execution, process-local tracing GC and supervision policy outside the privileged kernel. This work concerns the full system architecture, independently of PoC or emulator qualification.

## Composition obligations

Each service names its own state without duplicating its parent's lifecycle authority. Admission must allocate the metadata needed to track eventual cleanup. Logical rejection of new work, completion of old work, custody transfer and physical reuse are distinct results. Bounds depend on admitted participants, resources and hardware profiles; no universal latency is claimed.

The decomposition count follows the distinct state owners and failure/completion contracts below, not a fixed quota. The reports deliberately retain unresolved choices and unexecuted tests. Zig remains selected, but no compiler version or language feature substitutes for protected-state, concurrency or hardware proofs.

## Index

### Subdirectories

- None yet.

### Documents

- [Manifest decoding and policy validation](manifest-decoding-and-policy-validation.md) — What must be established before a boot description may influence privileged object creation?
- [Capacity and construction planning](capacity-and-construction-planning.md) — How can initialization promise that exceptional paths remain funded before any service is allowed to run?
- [Private object construction transaction](private-object-construction-transaction.md) — Where is the boundary between initialization that can roll back and authority that has escaped?
- [Authority-graph installation and audit](authority-graph-installation-and-audit.md) — How can the initialized authority graph be checked without inventing a universal administrative capability?
- [One-way root handoff and abort](one-way-root-handoff-and-abort.md) — What evidence permits a root service to begin ordinary operation, and what happens if it never accepts?

## Cross-component connections

- [Product authority and durable detachment](../capability-spaces-and-authority/product-authority-and-durable-detachment.md) — Construction must preserve effect-bearing authority.
- [Recovery escrow and reserve admission](../failure-boundaries-and-recovery-topology/recovery-escrow-and-reserve-admission.md) — Bootstrap must provision an independently usable recovery path.

The [minimal-kernel map](../../../10-maps/minimal-privileged-kernel.md) provides selective routes; the [session journal](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) contains the exhaustive source manifest. The [contract inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) remains open.

## Maintaining this index

Inventory every direct service report and child directory. Update the parent component, [component inventory](../README.md), relevant map and meaningful incoming links together whenever a service is added, moved or renamed. Preserve the distinction between documented coverage and demonstrated correctness.
