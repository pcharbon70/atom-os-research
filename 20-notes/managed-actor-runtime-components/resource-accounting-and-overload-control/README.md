---
title: "Resource accounting and overload control: internal services"
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

# Resource accounting and overload control: internal services

## Purpose

Decompose the [parent component](../resource-accounting-and-overload-control.md) into independently
reviewable research contracts. These 5 studies separate state owners,
visibility decisions and residual lifetimes; they are not implementation phases.

## What belongs here

Keep service-level ownership, protocol alternatives, source findings, failure
cases and falsifiers here. Preserve the parent as the integrated component
model. Runtime ledgers attribute consumption beneath hard kernel domain limits; actor policy cannot mint memory, CPU or cleanup reserve.

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

- [Hierarchical reservations and ledger reconciliation](hierarchical-reservations-and-ledger-reconciliation.md) — covers account hierarchy, resource-class totals, reservation generations and terminal release records.
- [Pressure states and protected recovery capacity](pressure-states-and-protected-recovery-capacity.md) — covers class-specific pressure thresholds, hysteresis, admission-close state and protected reserve balances.
- [ETS table identity, ownership and heir transfer](ets-table-identity-ownership-and-heir-transfer.md) — covers table identity/generation, type, access rights, current owner, configured heir and ledger account.
- [ETS atomic bulk work and adaptive storage](ets-atomic-bulk-work-and-adaptive-storage.md) — covers per-table operation descriptors, private preparation, mutation commit and retired storage.
- [Persistent terms and shared counter lifecycle](persistent-terms-and-shared-counter-lifecycle.md) — covers global immutable term bindings, counter-array generations and pending reader-drain/reclamation work.

## Cross-component boundaries

- [Shared-object retention](../terms-private-heaps-shared-binaries-and-tracing-collection/shared-binary-literal-and-fragment-lifetimes.md) — shared ownership or observation boundary.
- [Bounded shared-operation work](../reduction-scheduler-and-kernel-scheduling-contexts/reduction-costs-and-yieldable-work-continuations.md) — shared ownership or observation boundary.
- [Runtime component inventory](../README.md) — all thirteen parent components.
- [Managed-runtime map](../../../10-maps/managed-actor-runtime.md) — selective research routes.
- [Open inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — decisions awaiting evidence.
- [Dated source manifest](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — exact session provenance.

## Maintaining this index

Inventory every direct child, link directories through their README, and keep
the parent, component inventory, map and session evidence connected. Add a new
service only for a distinct responsibility; do not split or merge to meet a
numerical quota. Do not turn research completion into checked implementation.
