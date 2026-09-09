---
title: "Scheduling contexts and temporal authority: internal services"
kind: map
created: "2026-09-09"
tags: [archive-navigation, directory-index, kernel-internal-services, microkernels]
aliases: []
---

# Scheduling contexts and temporal authority: internal services

## Purpose

Conserve execution budget across binding and donation, separately fund causal work and recovery, and avoid confusing availability budgets with timing confidentiality.

This directory decomposes [component 5: Scheduling contexts and temporal authority](../scheduling-contexts-and-temporal-authority.md) into 5 internal-service studies. The parent remains the integrated contract; these are research boundaries, not necessarily separate privileged processes, exported APIs or source modules.

## What belongs here

Include service-level ownership, authority, transition, failure, alternative and verification analysis. Keep machine instruction/register contracts in the [hardware architecture layer](../../kernel-hardware-and-architecture-components/README.md), and keep BEAM execution, process-local tracing GC and supervision policy outside the privileged kernel. This work concerns the full system architecture, independently of PoC or emulator qualification.

## Composition obligations

Each service names its own state without duplicating its parent's lifecycle authority. Admission must allocate the metadata needed to track eventual cleanup. Logical rejection of new work, completion of old work, custody transfer and physical reuse are distinct results. Bounds depend on admitted participants, resources and hardware profiles; no universal latency is claimed.

The decomposition count follows the distinct state owners and failure/completion contracts below, not a fixed quota. The reports deliberately retain unresolved choices and unexecuted tests. Zig remains selected, but no compiler version or language feature substitutes for protected-state, concurrency or hardware proofs.

## Index

### Subdirectories

- None yet.

### Documents

- [Scheduling control and capacity admission](scheduling-control-and-capacity-admission.md) — Who may allocate CPU service, and what admission argument makes that allocation meaningful?
- [Budget accounting and bounded refills](budget-accounting-and-bounded-refills.md) — How can finite replenishment metadata preserve the promised service envelope?
- [Exclusive binding, donation and migration](exclusive-binding-donation-and-migration.md) — How can one execution budget follow a call chain or migrate without becoming usable in two places?
- [Causal charging and independent recovery reserves](causal-charging-and-independent-recovery-reserves.md) — Which work must remain attributable, and what resource independence makes recovery possible?
- [Timing-protection profile](timing-protection-profile.md) — What additional contract is needed when allocating CPU time must also prevent information leakage through timing?

## Cross-component connections

- [Kernel activation checkpoints](../protection-domains-threads-and-address-spaces/kernel-activation-checkpoints.md) — Kernel work must reach a consistent, bounded checkpoint.
- [Recovery escrow and reserve admission](../failure-boundaries-and-recovery-topology/recovery-escrow-and-reserve-admission.md) — Recovery needs authority and metadata as well as CPU time.

The [minimal-kernel map](../../../10-maps/minimal-privileged-kernel.md) provides selective routes; the [session journal](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) contains the exhaustive source manifest. The [contract inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) remains open.

## Maintaining this index

Inventory every direct service report and child directory. Update the parent component, [component inventory](../README.md), relevant map and meaningful incoming links together whenever a service is added, moved or renamed. Preserve the distinction between documented coverage and demonstrated correctness.
