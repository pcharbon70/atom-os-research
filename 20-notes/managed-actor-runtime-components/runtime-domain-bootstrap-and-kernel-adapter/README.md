---
title: "Runtime-domain bootstrap and kernel adapter: internal services"
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

# Runtime-domain bootstrap and kernel adapter: internal services

## Purpose

Decompose the [parent component](../runtime-domain-bootstrap-and-kernel-adapter.md) into independently
reviewable research contracts. These 4 studies separate state owners,
visibility decisions and residual lifetimes; they are not implementation phases.

## What belongs here

Keep service-level ownership, protocol alternatives, source findings, failure
cases and falsifiers here. Preserve the parent as the integrated component
model. The adapter consumes kernel authority; it does not make BEAM terms into capabilities or put the managed runtime in privileged code.

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

- [Launch descriptor and bootstrap transaction](launch-descriptor-and-bootstrap-transaction.md) — An immutable launch snapshot owns descriptor version, runtime epoch, image/profile hashes, initial resource grants and route identities.
- [Host dependency and adapter operation contract](host-dependency-and-adapter-operation-contract.md) — covers a dependency inventory grouped by clocks, memory, threading, files, entropy, networking and dynamic code.
- [Page, context and route grant adoption](page-context-and-route-grant-adoption.md) — covers grant generations, adoption state and the association between runtime pools and kernel accounts.
- [Admission close and domain quiescence](admission-close-and-domain-quiescence.md) — covers a monotonic admissions-closed latch, outstanding-operation set, cooperative worker-drain records and pre-registered evidence descriptors.

## Cross-component boundaries

- [Compatibility profile](../compatibility-manifest-beam-loader-and-verifier/compatibility-profile-and-conformance-catalog.md) — shared ownership or observation boundary.
- [Resource adoption and reconciliation](../resource-accounting-and-overload-control/hierarchical-reservations-and-ledger-reconciliation.md) — shared ownership or observation boundary.
- [Runtime component inventory](../README.md) — all thirteen parent components.
- [Managed-runtime map](../../../10-maps/managed-actor-runtime.md) — selective research routes.
- [Open inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — decisions awaiting evidence.
- [Dated source manifest](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — exact session provenance.

## Maintaining this index

Inventory every direct child, link directories through their README, and keep
the parent, component inventory, map and session evidence connected. Add a new
service only for a distinct responsibility; do not split or merge to meet a
numerical quota. Do not turn research completion into checked implementation.
