---
title: "Fault capture and containment: internal services"
kind: map
created: "2026-09-09"
tags: [archive-navigation, directory-index, kernel-internal-services, microkernels]
aliases: []
---

# Fault capture and containment: internal services

## Purpose

Produce bounded fault evidence, route it independently and grant only the narrow repair or termination authority justified by the fault contract.

This directory decomposes [component 7: Fault capture and containment](../fault-capture-and-containment.md) into 4 internal-service studies. The parent remains the integrated contract; these are research boundaries, not necessarily separate privileged processes, exported APIs or source modules.

## What belongs here

Include service-level ownership, authority, transition, failure, alternative and verification analysis. Keep machine instruction/register contracts in the [hardware architecture layer](../../kernel-hardware-and-architecture-components/README.md), and keep BEAM execution, process-local tracing GC and supervision policy outside the privileged kernel. This work concerns the full system architecture, independently of PoC or emulator qualification.

## Composition obligations

Each service names its own state without duplicating its parent's lifecycle authority. Admission must allocate the metadata needed to track eventual cleanup. Logical rejection of new work, completion of old work, custody transfer and physical reuse are distinct results. Bounds depend on admitted participants, resources and hardware profiles; no universal latency is claimed.

The decomposition count follows the distinct state owners and failure/completion contracts below, not a fixed quota. The reports deliberately retain unresolved choices and unexecuted tests. Zig remains selected, but no compiler version or language feature substitutes for protected-state, concurrency or hardware proofs.

## Index

### Subdirectories

- None yet.

### Documents

- [Fault taxonomy and bounded capture](fault-taxonomy-and-bounded-capture.md) — How can the kernel record a fault without overstating either its cause or its containment?
- [Fault routing and overflow fallback](fault-routing-and-overflow-fallback.md) — How does fault delivery remain useful when the normal handler is full, blocked or inside the failed scope?
- [One-shot resolvers and repair admission](one-shot-resolvers-and-repair-admission.md) — What authority lets a fault handler repair one blocked thread without gaining ambient control over its domain?
- [Containment escalation and terminal handoff](containment-escalation-and-terminal-handoff.md) — Who may promote a fault into domain termination or a node-fatal decision?

## Cross-component connections

- [SMP stop and completion evidence](../protection-domains-threads-and-address-spaces/smp-stop-and-completion-evidence.md) — Fatal domain handling uses the existing stop protocol.
- [Post-seal crash enrichment](../observability-and-crash-evidence/post-seal-crash-enrichment.md) — Higher-level evidence enriches, but never replaces, lower fatal capture.

The [minimal-kernel map](../../../10-maps/minimal-privileged-kernel.md) provides selective routes; the [session journal](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) contains the exhaustive source manifest. The [contract inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) remains open.

## Maintaining this index

Inventory every direct service report and child directory. Update the parent component, [component inventory](../README.md), relevant map and meaningful incoming links together whenever a service is added, moved or renamed. Preserve the distinction between documented coverage and demonstrated correctness.
