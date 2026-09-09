---
title: "Terms, private heaps, shared binaries and tracing collection: internal services"
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

# Terms, private heaps, shared binaries and tracing collection: internal services

## Purpose

Decompose the [parent component](../terms-private-heaps-shared-binaries-and-tracing-collection.md) into independently
reviewable research contracts. These 5 studies separate state owners,
visibility decisions and residual lifetimes; they are not implementation phases.

## What belongs here

Keep service-level ownership, protocol alternatives, source findings, failure
cases and falsifiers here. Preserve the parent as the integrated component
model. Automatic tracing collection and term interpretation remain unprivileged runtime responsibilities; kernel pages do not encode BEAM object ownership.

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

- [Term representation and copy boundary](term-representation-and-copy-boundary.md) — covers tag/layout descriptors, checked object sizes and a total classification of private, immediate and explicitly shared values.
- [Private heap allocation and generational invariants](private-heap-allocation-and-generational-invariants.md) — covers young/old areas, allocation tops, stack boundaries, remembered information and a generation-stamped allocator account.
- [Exact root capture and collector handoff](exact-root-capture-and-collector-handoff.md) — covers a root-map version and actor-local collection handshake.
- [Copying collection reserve and resumable progress](copying-collection-reserve-and-resumable-progress.md) — covers the collection cycle, reserved destination capacity, forwarding/work queues and commit marker.
- [Shared binary, literal and fragment lifetimes](shared-binary-literal-and-fragment-lifetimes.md) — covers reference/lease records for immutable large binaries, literal areas and incoming heap fragments.

## Cross-component boundaries

- [Root materialization](../code-execution-safe-points-and-version-publication/canonical-safe-point-and-native-helper-state.md) — shared ownership or observation boundary.
- [Physical and retained accounting](../resource-accounting-and-overload-control/hierarchical-reservations-and-ledger-reconciliation.md) — shared ownership or observation boundary.
- [Runtime component inventory](../README.md) — all thirteen parent components.
- [Managed-runtime map](../../../10-maps/managed-actor-runtime.md) — selective research routes.
- [Open inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — decisions awaiting evidence.
- [Dated source manifest](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — exact session provenance.

## Maintaining this index

Inventory every direct child, link directories through their README, and keep
the parent, component inventory, map and session evidence connected. Add a new
service only for a distinct responsibility; do not split or merge to meet a
numerical quota. Do not turn research completion into checked implementation.
