---
title: "Teardown, revocation and safe reclamation: internal services"
kind: map
created: "2026-09-09"
tags: [archive-navigation, directory-index, kernel-internal-services, microkernels]
aliases: []
---

# Teardown, revocation and safe reclamation: internal services

## Purpose

Turn logical closure into a charged, resumable proof of effect completion or exact quarantine custody before the allocator can reuse backing.

This directory decomposes [component 9: Teardown, revocation and safe reclamation](../teardown-revocation-and-safe-reclamation.md) into 4 internal-service studies. The parent remains the integrated contract; these are research boundaries, not necessarily separate privileged processes, exported APIs or source modules.

## What belongs here

Include service-level ownership, authority, transition, failure, alternative and verification analysis. Keep machine instruction/register contracts in the [hardware architecture layer](../../kernel-hardware-and-architecture-components/README.md), and keep BEAM execution, process-local tracing GC and supervision policy outside the privileged kernel. This work concerns the full system architecture, independently of PoC or emulator qualification.

## Composition obligations

Each service names its own state without duplicating its parent's lifecycle authority. Admission must allocate the metadata needed to track eventual cleanup. Logical rejection of new work, completion of old work, custody transfer and physical reuse are distinct results. Bounds depend on admitted participants, resources and hardware profiles; no universal latency is claimed.

The decomposition count follows the distinct state owners and failure/completion contracts below, not a fixed quota. The reports deliberately retain unresolved choices and unexecuted tests. Zig remains selected, but no compiler version or language feature substitutes for protected-state, concurrency or hardware proofs.

## Index

### Subdirectories

- None yet.

### Documents

- [Effect ledger and dependency graph](effect-ledger-and-dependency-graph.md) — How can teardown know every effect that must finish without discovering dependencies after resources are already failing?
- [Charged reaper and resumable cursors](charged-reaper-and-resumable-cursors.md) — How can cleanup make bounded progress without monopolizing privileged execution or depending on the failed owner?
- [Software and hardware quiescence join](software-and-hardware-quiescence-join.md) — Which combination of evidence is sufficient to say that old effects cannot reach reusable memory?
- [Quarantine custody and reuse release](quarantine-custody-and-reuse-release.md) — When is quarantine a safe terminal disposition rather than a name for unknown damage?

## Cross-component connections

- [Sanitization and generation-safe reuse](../typed-object-storage-and-explicit-memory/sanitization-and-generation-safe-reuse.md) — Only the allocator completes sanitization and fresh publication.
- [Device completion and reset composition](../memory-mappings-and-architecture-resource-bindings/device-completion-and-reset-composition.md) — Device-specific graphs supply physical completion evidence.

The [minimal-kernel map](../../../10-maps/minimal-privileged-kernel.md) provides selective routes; the [session journal](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) contains the exhaustive source manifest. The [contract inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) remains open.

## Maintaining this index

Inventory every direct service report and child directory. Update the parent component, [component inventory](../README.md), relevant map and meaningful incoming links together whenever a service is added, moved or renamed. Preserve the distinction between documented coverage and demonstrated correctness.
