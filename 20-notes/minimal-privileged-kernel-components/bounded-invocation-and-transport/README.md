---
title: "Bounded invocation and transport: internal services"
kind: map
created: "2026-09-09"
tags: [archive-navigation, directory-index, kernel-internal-services, microkernels]
aliases: []
---

# Bounded invocation and transport: internal services

## Purpose

Keep small protected calls, coalescing notifications and shared-buffer transport finite, explicitly funded and honest about accepted effects.

This directory decomposes [component 4: Bounded invocation and transport](../bounded-invocation-and-transport.md) into 5 internal-service studies. The parent remains the integrated contract; these are research boundaries, not necessarily separate privileged processes, exported APIs or source modules.

## What belongs here

Include service-level ownership, authority, transition, failure, alternative and verification analysis. Keep machine instruction/register contracts in the [hardware architecture layer](../../kernel-hardware-and-architecture-components/README.md), and keep BEAM execution, process-local tracing GC and supervision policy outside the privileged kernel. This work concerns the full system architecture, independently of PoC or emulator qualification.

## Composition obligations

Each service names its own state without duplicating its parent's lifecycle authority. Admission must allocate the metadata needed to track eventual cleanup. Logical rejection of new work, completion of old work, custody transfer and physical reuse are distinct results. Bounds depend on admitted participants, resources and hardware profiles; no universal latency is claimed.

The decomposition count follows the distinct state owners and failure/completion contracts below, not a fixed quota. The reports deliberately retain unresolved choices and unexecuted tests. Zig remains selected, but no compiler version or language feature substitutes for protected-state, concurrency or hardware proofs.

## Index

### Subdirectories

- None yet.

### Documents

- [Endpoint admission and call records](endpoint-admission-and-call-records.md) — What must be reserved before a request can become an accepted service invocation?
- [Reply authority and outcome arbitration](reply-authority-and-outcome-arbitration.md) — What can a caller safely conclude when reply, cancellation and failure race?
- [Passive handler abort and donation drain](passive-handler-abort-and-donation-drain.md) — How may caller-funded work be terminated without returning a scheduling context that is still executing elsewhere?
- [Notifications and sticky event state](notifications-and-sticky-event-state.md) — How can a bounded wakeup primitive avoid both lost transitions and a false promise of event counting?
- [Shared-ring ownership and incarnation](shared-ring-ownership-and-incarnation.md) — What contract surrounds a shared queue when either endpoint may fail or supply hostile descriptors?

## Cross-component connections

- [Exclusive binding, donation and migration](../scheduling-contexts-and-temporal-authority/exclusive-binding-donation-and-migration.md) — Call acceptance and donation share a commit boundary.
- [Recipient fences and service publication](../failure-boundaries-and-recovery-topology/recipient-fences-and-service-publication.md) — Replacement must preserve old call outcomes.

The [minimal-kernel map](../../../10-maps/minimal-privileged-kernel.md) provides selective routes; the [session journal](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) contains the exhaustive source manifest. The [contract inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) remains open.

## Maintaining this index

Inventory every direct service report and child directory. Update the parent component, [component inventory](../README.md), relevant map and meaningful incoming links together whenever a service is added, moved or renamed. Preserve the distinction between documented coverage and demonstrated correctness.
