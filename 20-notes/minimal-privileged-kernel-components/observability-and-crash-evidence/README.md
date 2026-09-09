---
title: "Observability and crash evidence: internal services"
kind: map
created: "2026-09-09"
tags: [archive-navigation, directory-index, kernel-internal-services, microkernels]
aliases: []
---

# Observability and crash evidence: internal services

## Purpose

Expose bounded, authorized operational evidence and enrich the lower architecture's single terminal record without adding unsafe crash-time dependencies.

This directory decomposes [component 10: Observability and crash evidence](../observability-and-crash-evidence.md) into 5 internal-service studies. The parent remains the integrated contract; these are research boundaries, not necessarily separate privileged processes, exported APIs or source modules.

## What belongs here

Include service-level ownership, authority, transition, failure, alternative and verification analysis. Keep machine instruction/register contracts in the [hardware architecture layer](../../kernel-hardware-and-architecture-components/README.md), and keep BEAM execution, process-local tracing GC and supervision policy outside the privileged kernel. This work concerns the full system architecture, independently of PoC or emulator qualification.

## Composition obligations

Each service names its own state without duplicating its parent's lifecycle authority. Admission must allocate the metadata needed to track eventual cleanup. Logical rejection of new work, completion of old work, custody transfer and physical reuse are distinct results. Bounds depend on admitted participants, resources and hardware profiles; no universal latency is claimed.

The decomposition count follows the distinct state owners and failure/completion contracts below, not a fixed quota. The reports deliberately retain unresolved choices and unexecuted tests. Zig remains selected, but no compiler version or language feature substitutes for protected-state, concurrency or hardware proofs.

## Index

### Subdirectories

- None yet.

### Documents

- [Event schema and static probe control](event-schema-and-static-probe-control.md) — What diagnostic information may privileged code emit, at whose expense and under which authority?
- [Per-CPU buffers and snapshot lifetime](per-cpu-buffers-and-snapshot-lifetime.md) — How can readers obtain bounded diagnostic snapshots without racing an interrupted writer or freed backing?
- [Scoped inspection and redacted cursors](scoped-inspection-and-redacted-cursors.md) — How can an inspector traverse changing kernel state without gaining ambient authority or holding objects forever?
- [Post-seal crash enrichment](post-seal-crash-enrichment.md) — What higher-level evidence can be added after the architecture has sealed its terminal crash context?
- [Crash export and assurance boundaries](crash-export-and-assurance-boundaries.md) — What may a crash artifact legitimately claim about integrity, secrecy, persistence and causality?

## Cross-component connections

- [Containment escalation and terminal handoff](../fault-capture-and-containment/containment-escalation-and-terminal-handoff.md) — One lower terminal protocol owns fatal disposition.
- [Lifetime groups and activation pins](../typed-object-storage-and-explicit-memory/lifetime-groups-and-activation-pins.md) — Reading evidence needs a real backing-storage lifetime.

The [minimal-kernel map](../../../10-maps/minimal-privileged-kernel.md) provides selective routes; the [session journal](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) contains the exhaustive source manifest. The [contract inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) remains open.

## Maintaining this index

Inventory every direct service report and child directory. Update the parent component, [component inventory](../README.md), relevant map and meaningful incoming links together whenever a service is added, moved or renamed. Preserve the distinction between documented coverage and demonstrated correctness.
