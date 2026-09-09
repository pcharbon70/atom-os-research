---
title: "Protection domains, threads and address spaces: internal services"
kind: map
created: "2026-09-09"
tags: [archive-navigation, directory-index, kernel-internal-services, microkernels]
aliases: []
---

# Protection domains, threads and address spaces: internal services

## Purpose

Make domains exact execution-stop boundaries while keeping accounting, actors, service identity and recovery policy separate.

This directory decomposes [component 3: Protection domains, threads and address spaces](../protection-domains-threads-and-address-spaces.md) into 5 internal-service studies. The parent remains the integrated contract; these are research boundaries, not necessarily separate privileged processes, exported APIs or source modules.

## What belongs here

Include service-level ownership, authority, transition, failure, alternative and verification analysis. Keep machine instruction/register contracts in the [hardware architecture layer](../../kernel-hardware-and-architecture-components/README.md), and keep BEAM execution, process-local tracing GC and supervision policy outside the privileged kernel. This work concerns the full system architecture, independently of PoC or emulator qualification.

## Composition obligations

Each service names its own state without duplicating its parent's lifecycle authority. Admission must allocate the metadata needed to track eventual cleanup. Logical rejection of new work, completion of old work, custody transfer and physical reuse are distinct results. Bounds depend on admitted participants, resources and hardware profiles; no universal latency is claimed.

The decomposition count follows the distinct state owners and failure/completion contracts below, not a fixed quota. The reports deliberately retain unresolved choices and unexecuted tests. Zig remains selected, but no compiler version or language feature substitutes for protected-state, concurrency or hardware proofs.

## Index

### Subdirectories

- None yet.

### Documents

- [Domain roots and membership](domain-roots-and-membership.md) — What state makes one protection domain a well-defined containment boundary?
- [Root gates and close linearization](root-gates-and-close-linearization.md) — How can a domain stop acquiring new work without first walking every object it owns?
- [Thread readiness and reversible suspension](thread-readiness-and-reversible-suspension.md) — How can administrative suspension preserve a thread's logical wait state without confusing it with terminal stop?
- [Kernel activation checkpoints](kernel-activation-checkpoints.md) — What must be true before a stopped CPU activation can be acknowledged as safe?
- [SMP stop and completion evidence](smp-stop-and-completion-evidence.md) — How can a domain stop certificate cover every CPU that might still execute its old incarnation?

## Cross-component connections

- [Passive handler abort and donation drain](../bounded-invocation-and-transport/passive-handler-abort-and-donation-drain.md) — Accepted passive handlers require a valid stop/checkpoint path.
- [Software and hardware quiescence join](../teardown-revocation-and-safe-reclamation/software-and-hardware-quiescence-join.md) — Execution stop is only one condition of final reclamation.

The [minimal-kernel map](../../../10-maps/minimal-privileged-kernel.md) provides selective routes; the [session journal](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) contains the exhaustive source manifest. The [contract inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) remains open.

## Maintaining this index

Inventory every direct service report and child directory. Update the parent component, [component inventory](../README.md), relevant map and meaningful incoming links together whenever a service is added, moved or renamed. Preserve the distinction between documented coverage and demonstrated correctness.
