---
title: "Signal ingress, mailboxes and selective receive: internal services"
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

# Signal ingress, mailboxes and selective receive: internal services

## Purpose

Decompose the [parent component](../signal-ingress-mailboxes-and-selective-receive.md) into independently
reviewable research contracts. These 4 studies separate state owners,
visibility decisions and residual lifetimes; they are not implementation phases.

## What belongs here

Keep service-level ownership, protocol alternatives, source findings, failure
cases and falsifiers here. Preserve the parent as the integrated component
model. Physical enqueue order, ordered signal delivery and selective mailbox placement are three separate contracts.

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

- [Signal envelope admission and payload transfer](signal-envelope-admission-and-payload-transfer.md) — covers a prepared envelope containing source/destination incarnations, signal kind, order-domain identity, payload storage, correlation and charge.
- [Striped ingress order and node reclamation](striped-ingress-order-and-node-reclamation.md) — covers stripe generations, sender-to-stripe assignment, drain cursors and producer pins.
- [Signal dispatch, priority and alias admission](signal-dispatch-priority-and-alias-admission.md) — covers the receiver-side signal dispatcher, priority/ordinary mailbox partitions and bounded control-work cursor.
- [Selective receive cursors, markers and timeouts](selective-receive-cursors-markers-and-timeouts.md) — covers the current receive expression, partition-aware scan cursor, saved unmatched position, timeout identity and validated fresh-reference marker.

## Cross-component boundaries

- [Relation state ownership](../actor-identity-lifecycle-and-process-state/links-monitors-aliases-and-name-registration.md) — shared ownership or observation boundary.
- [Payload lifetime and adoption](../terms-private-heaps-shared-binaries-and-tracing-collection/shared-binary-literal-and-fragment-lifetimes.md) — shared ownership or observation boundary.
- [Runtime component inventory](../README.md) — all thirteen parent components.
- [Managed-runtime map](../../../10-maps/managed-actor-runtime.md) — selective research routes.
- [Open inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — decisions awaiting evidence.
- [Dated source manifest](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — exact session provenance.

## Maintaining this index

Inventory every direct child, link directories through their README, and keep
the parent, component inventory, map and session evidence connected. Add a new
service only for a distinct responsibility; do not split or merge to meet a
numerical quota. Do not turn research completion into checked implementation.
