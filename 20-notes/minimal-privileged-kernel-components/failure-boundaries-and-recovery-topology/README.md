---
title: "Failure boundaries and recovery topology: internal services"
kind: map
created: "2026-09-09"
tags: [archive-navigation, directory-index, kernel-internal-services, microkernels]
aliases: []
---

# Failure boundaries and recovery topology: internal services

## Purpose

Keep recovery authority and resources outside the failed scope, fence replacement managers, and leave application-state recovery policy unprivileged.

This directory decomposes [component 8: Failure boundaries and recovery topology](../failure-boundaries-and-recovery-topology.md) into 5 internal-service studies. The parent remains the integrated contract; these are research boundaries, not necessarily separate privileged processes, exported APIs or source modules.

## What belongs here

Include service-level ownership, authority, transition, failure, alternative and verification analysis. Keep machine instruction/register contracts in the [hardware architecture layer](../../kernel-hardware-and-architecture-components/README.md), and keep BEAM execution, process-local tracing GC and supervision policy outside the privileged kernel. This work concerns the full system architecture, independently of PoC or emulator qualification.

## Composition obligations

Each service names its own state without duplicating its parent's lifecycle authority. Admission must allocate the metadata needed to track eventual cleanup. Logical rejection of new work, completion of old work, custody transfer and physical reuse are distinct results. Bounds depend on admitted participants, resources and hardware profiles; no universal latency is claimed.

The decomposition count follows the distinct state owners and failure/completion contracts below, not a fixed quota. The reports deliberately retain unresolved choices and unexecuted tests. Zig remains selected, but no compiler version or language feature substitutes for protected-state, concurrency or hardware proofs.

## Index

### Subdirectories

- None yet.

### Documents

- [Failure scope and dependency inventory](failure-scope-and-dependency-inventory.md) — Which apparently separate components must actually fail or recover together?
- [Recovery escrow and reserve admission](recovery-escrow-and-reserve-admission.md) — How can a successor recover a domain when both the child and its replaceable supervisor are unusable?
- [Lease takeover and operation adoption](lease-takeover-and-operation-adoption.md) — How can a new manager take control without losing valid completion evidence from already admitted work?
- [Recipient fences and service publication](recipient-fences-and-service-publication.md) — Where must an epoch be checked to prevent a stale manager from changing a recovered service?
- [State reconstruction and root fallback](state-reconstruction-and-root-fallback.md) — What state may a replacement trust, and where does recovery stop when its final independent controller fails?

## Cross-component connections

- [Sealed use facets and epoch sessions](../capability-spaces-and-authority/sealed-use-facets-and-epoch-sessions.md) — Lease enforcement relies on protected facets and closed sessions.
- [Charged reaper and resumable cursors](../teardown-revocation-and-safe-reclamation/charged-reaper-and-resumable-cursors.md) — A successor must continue the same teardown operation.

The [minimal-kernel map](../../../10-maps/minimal-privileged-kernel.md) provides selective routes; the [session journal](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) contains the exhaustive source manifest. The [contract inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) remains open.

## Maintaining this index

Inventory every direct service report and child directory. Update the parent component, [component inventory](../README.md), relevant map and meaningful incoming links together whenever a service is added, moved or renamed. Preserve the distinction between documented coverage and demonstrated correctness.
