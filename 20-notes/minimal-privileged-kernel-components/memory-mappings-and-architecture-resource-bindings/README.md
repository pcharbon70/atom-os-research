---
title: "Memory mappings and architecture-resource bindings: internal services"
kind: map
created: "2026-09-09"
tags: [archive-navigation, directory-index, kernel-internal-services, microkernels]
aliases: []
---

# Memory mappings and architecture-resource bindings: internal services

## Purpose

Bind current authority to lower-layer mapping, interrupt and device effects while preserving exact generations and profile-specific completion evidence.

This directory decomposes [component 6: Memory mappings and architecture-resource bindings](../memory-mappings-and-architecture-resource-bindings.md) into 6 internal-service studies. The parent remains the integrated contract; these are research boundaries, not necessarily separate privileged processes, exported APIs or source modules.

## What belongs here

Include service-level ownership, authority, transition, failure, alternative and verification analysis. Keep machine instruction/register contracts in the [hardware architecture layer](../../kernel-hardware-and-architecture-components/README.md), and keep BEAM execution, process-local tracing GC and supervision policy outside the privileged kernel. This work concerns the full system architecture, independently of PoC or emulator qualification.

## Composition obligations

Each service names its own state without duplicating its parent's lifecycle authority. Admission must allocate the metadata needed to track eventual cleanup. Logical rejection of new work, completion of old work, custody transfer and physical reuse are distinct results. Bounds depend on admitted participants, resources and hardware profiles; no universal latency is claimed.

The decomposition count follows the distinct state owners and failure/completion contracts below, not a fixed quota. The reports deliberately retain unresolved choices and unexecuted tests. Zig remains selected, but no compiler version or language feature substitutes for protected-state, concurrency or hardware proofs.

## Index

### Subdirectories

- None yet.

### Documents

- [Mapping authority and rights ceilings](mapping-authority-and-rights-ceilings.md) — Which authorities bound a mapping throughout its lifetime, including later protection changes?
- [Frame authority epochs and quarantine](frame-authority-epochs-and-quarantine.md) — How can quarantine prevent old grants from becoming valid again when memory is eventually released?
- [Interrupt and timer binding lifetimes](interrupt-and-timer-binding-lifetimes.md) — What lifetime object connects an authorized consumer to asynchronous architecture events?
- [Device profiles and requester trust sets](device-profiles-and-requester-trust-sets.md) — What deployment facts are required before separate device handles can be advertised as isolated authority?
- [Submission alias fencing](submission-alias-fencing.md) — When does revoking a device manager actually prevent it from submitting more work?
- [Device completion and reset composition](device-completion-and-reset-composition.md) — Which evidence can release a device effect, especially when recovery authority changes mid-operation?

## Cross-component connections

- [Effect ledger and dependency graph](../teardown-revocation-and-safe-reclamation/effect-ledger-and-dependency-graph.md) — Every admitted binding contributes its completion obligations.
- [Lease takeover and operation adoption](../failure-boundaries-and-recovery-topology/lease-takeover-and-operation-adoption.md) — Takeover must preserve valid old-operation evidence.

The [minimal-kernel map](../../../10-maps/minimal-privileged-kernel.md) provides selective routes; the [session journal](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) contains the exhaustive source manifest. The [contract inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) remains open.

## Maintaining this index

Inventory every direct service report and child directory. Update the parent component, [component inventory](../README.md), relevant map and meaningful incoming links together whenever a service is added, moved or renamed. Preserve the distinction between documented coverage and demonstrated correctness.
