---
title: "Reduction scheduler and kernel scheduling contexts: internal services"
kind: map
created: "2026-09-09"
tags:
  - actor-model
  - beam
  - managed-runtime
  - system-architecture
  - directory-index
aliases: []
---

# Reduction scheduler and kernel scheduling contexts: internal services

## Purpose

Decompose the [parent component](../reduction-scheduler-and-kernel-scheduling-contexts.md) into independently
reviewable research contracts. These 4 studies separate state owners,
visibility decisions and residual lifetimes; they are not implementation phases.

## What belongs here

Keep service-level ownership, protocol alternatives, source findings, failure
cases and falsifiers here. Preserve the parent as the integrated component
model. Runtime reductions select actors; kernel contexts enforce CPU authority. Neither is a hard real-time guarantee by itself.

The split follows actual semantic and lifecycle distinctions, not a uniform
number of reports. All studies remain developing and their tests unexecuted.
They concern the full system architecture rather than a particular boot fixture.

## Shared contracts

- Preserve the parent compatibility profile; label restricted behavior and
  new APIs explicitly. Public OTP behavior and internal ERTS mechanisms are
  different evidence classes.
- Keep ordinary actors and automatic process-local tracing collection outside
  the privileged kernel. Native runtime corruption can compromise the domain.
- Bind operations to the relevant object, actor, domain and service generations;
  a transport session is not automatically a new external BEAM identity.
- Distinguish private preparation, publication, terminal semantic outcome and
  final storage reclamation. Cancellation and wakeups are not universal
  completion receipts.
- Charge deferred work and preserve finite recovery/evidence capacity. No
  literature throughput result establishes a hard latency bound here.

## Index

### Subdirectories

- None.

### Documents

- [Activation ownership, wakeup and work stealing](activation-ownership-wakeup-and-work-stealing.md) — covers each actor's runnable/running/waiting claim, local queue membership and wakeup generation.
- [Reduction costs and yieldable work continuations](reduction-costs-and-yieldable-work-continuations.md) — covers the work-cost catalog and continuation records for BIFs, copying, receive scans, collection, table operations and cleanup.
- [Kernel budget reconciliation and worker lifecycle](kernel-budget-reconciliation-and-worker-lifecycle.md) — covers worker-to-context bindings, CPU observations and lifecycle state.
- [Priority classes and funded runtime progress](priority-classes-and-funded-runtime-progress.md) — covers runtime work-class queues, priority selection state and capped control/GC/cleanup reserve.

## Cross-component boundaries

- [Safe-point handoff](../code-execution-safe-points-and-version-publication/canonical-safe-point-and-native-helper-state.md) — shared ownership or observation boundary.
- [Funded control and recovery](../resource-accounting-and-overload-control/pressure-states-and-protected-recovery-capacity.md) — shared ownership or observation boundary.
- [Runtime component inventory](../README.md) — all thirteen parent components.
- [Managed-runtime map](../../../10-maps/managed-actor-runtime.md) — selective research routes.
- [Open inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — decisions awaiting evidence.
- [Dated source manifest](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — exact session provenance.

## Maintaining this index

Inventory every direct child, link directories through their README, and keep
the parent, component inventory, map and session evidence connected. Add a new
service only for a distinct responsibility; do not split or merge to meet a
numerical quota. Do not turn research completion into checked implementation.
