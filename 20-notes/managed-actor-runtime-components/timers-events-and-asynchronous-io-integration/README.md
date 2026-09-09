---
title: "Timers, events and asynchronous I/O integration: internal services"
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

# Timers, events and asynchronous I/O integration: internal services

## Purpose

Decompose the [parent component](../timers-events-and-asynchronous-io-integration.md) into independently
reviewable research contracts. These 4 studies separate state owners,
visibility decisions and residual lifetimes; they are not implementation phases.

## What belongs here

Keep service-level ownership, protocol alternatives, source findings, failure
cases and falsifiers here. Preserve the parent as the integrated component
model. The runtime owns timer and actor semantics; the kernel supplies qualified time and deadline events, not one kernel timer per actor.

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

- [Clock era and timer destination contract](clock-era-and-timer-destination-contract.md) — covers conversion from timer arguments to a checked monotonic deadline, clock era and destination descriptor.
- [Hierarchical timer queues and bounded cascade](hierarchical-timer-queues-and-bounded-cascade.md) — covers wheel geometry, near-deadline structure, shard generation, occupancy hints and a resumable cascade cursor.
- [Expiry, cancel, suspend and deadline-rearm arbitration](expiry-cancel-suspend-and-deadline-rearm-arbitration.md) — covers each timer's armed/suspended/due/published/cancelled state and the token for the shard's earliest kernel deadline.
- [Asynchronous operation records and buffer completion](asynchronous-operation-records-and-buffer-completion.md) — covers request identity, caller/service incarnations, buffer leases, terminal result slot and readiness subscription.

## Cross-component boundaries

- [Timeout consumption and receive races](../signal-ingress-mailboxes-and-selective-receive/selective-receive-cursors-markers-and-timeouts.md) — shared ownership or observation boundary.
- [External request disposition](../native-work-ports-and-drivers/native-request-outcomes-and-cancellation-drain.md) — shared ownership or observation boundary.
- [Runtime component inventory](../README.md) — all thirteen parent components.
- [Managed-runtime map](../../../10-maps/managed-actor-runtime.md) — selective research routes.
- [Open inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — decisions awaiting evidence.
- [Dated source manifest](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — exact session provenance.

## Maintaining this index

Inventory every direct child, link directories through their README, and keep
the parent, component inventory, map and session evidence connected. Add a new
service only for a distinct responsibility; do not split or merge to meet a
numerical quota. Do not turn research completion into checked implementation.
