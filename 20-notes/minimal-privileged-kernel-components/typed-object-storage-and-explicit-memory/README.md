---
title: "Typed object storage and explicit memory: internal services"
kind: map
created: "2026-09-09"
tags: [archive-navigation, directory-index, kernel-internal-services, microkernels]
aliases: []
---

# Typed object storage and explicit memory: internal services

## Purpose

Give every privileged object explicit backing, accounting and lifetime, with allocator reuse dependent on completed teardown rather than capability count alone.

This directory decomposes [component 1: Typed object storage and explicit memory](../typed-object-storage-and-explicit-memory.md) into 5 internal-service studies. The parent remains the integrated contract; these are research boundaries, not necessarily separate privileged processes, exported APIs or source modules.

## What belongs here

Include service-level ownership, authority, transition, failure, alternative and verification analysis. Keep machine instruction/register contracts in the [hardware architecture layer](../../kernel-hardware-and-architecture-components/README.md), and keep BEAM execution, process-local tracing GC and supervision policy outside the privileged kernel. This work concerns the full system architecture, independently of PoC or emulator qualification.

## Composition obligations

Each service names its own state without duplicating its parent's lifecycle authority. Admission must allocate the metadata needed to track eventual cleanup. Logical rejection of new work, completion of old work, custody transfer and physical reuse are distinct results. Bounds depend on admitted participants, resources and hardware profiles; no universal latency is claimed.

The decomposition count follows the distinct state owners and failure/completion contracts below, not a fixed quota. The reports deliberately retain unresolved choices and unexecuted tests. Zig remains selected, but no compiler version or language feature substitutes for protected-state, concurrency or hardware proofs.

## Index

### Subdirectories

- None yet.

### Documents

- [Backing pools and retyping](backing-pools-and-retyping.md) — How can memory become typed kernel objects without introducing hidden allocation authority?
- [Object creation and publication](object-creation-and-publication.md) — How can a multi-input constructor either publish one fully owned object or have no externally visible effect?
- [Quota accounts and charge transfer](quota-accounts-and-charge-transfer.md) — Who pays for a shared object when the creator, users and cleanup owner differ?
- [Lifetime groups and activation pins](lifetime-groups-and-activation-pins.md) — How are object lifetime ownership and temporary dereference safety represented independently?
- [Sanitization and generation-safe reuse](sanitization-and-generation-safe-reuse.md) — When may an old object's bytes and identifier safely become a new object?

## Cross-component connections

- [Quarantine custody and reuse release](../teardown-revocation-and-safe-reclamation/quarantine-custody-and-reuse-release.md) — The reaper proves eligibility; the allocator performs final reuse.
- [Product authority and durable detachment](../capability-spaces-and-authority/product-authority-and-durable-detachment.md) — Creation must attach the correct lifetime dependencies.

The [minimal-kernel map](../../../10-maps/minimal-privileged-kernel.md) provides selective routes; the [session journal](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) contains the exhaustive source manifest. The [contract inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) remains open.

## Maintaining this index

Inventory every direct service report and child directory. Update the parent component, [component inventory](../README.md), relevant map and meaningful incoming links together whenever a service is added, moved or renamed. Preserve the distinction between documented coverage and demonstrated correctness.
