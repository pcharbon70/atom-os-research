---
title: "Actor identity, lifecycle and process state: internal services"
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

# Actor identity, lifecycle and process state: internal services

## Purpose

Decompose the [parent component](../actor-identity-lifecycle-and-process-state.md) into independently
reviewable research contracts. These 4 studies separate state owners,
visibility decisions and residual lifetimes; they are not implementation phases.

## What belongs here

Keep service-level ownership, protocol alternatives, source findings, failure
cases and falsifiers here. Preserve the parent as the integrated component
model. Actor identity is a managed routing concept. The registry does not create kernel protection between actors sharing one runtime.

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

- [Actor registry generations and lookup pins](actor-registry-generations-and-lookup-pins.md) — covers registry slots, internal generation/epoch, publication state and bounded lookup pins.
- [Spawn transaction and atomic relations](spawn-transaction-and-atomic-relations.md) — covers an unpublished actor record, argument-copy arena, initial frame, account reservation and any requested parent relation.
- [Links, monitors, aliases and name registration](links-monitors-aliases-and-name-registration.md) — covers symmetric links, independent monitor references, alias activation state and registered-name bindings.
- [Exit cursor and process-state snapshots](exit-cursor-and-process-state-snapshots.md) — covers the actor's one selected exit outcome, a bounded cleanup cursor and versioned process-state summaries.

## Cross-component boundaries

- [Generation-bound signal publication](../signal-ingress-mailboxes-and-selective-receive/signal-envelope-admission-and-payload-transfer.md) — shared ownership or observation boundary.
- [Exit outcome and fan-out](../failure-translation-and-the-otp-boundary/termination-reason-lifetime-and-bounded-fanout.md) — shared ownership or observation boundary.
- [Runtime component inventory](../README.md) — all thirteen parent components.
- [Managed-runtime map](../../../10-maps/managed-actor-runtime.md) — selective research routes.
- [Open inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — decisions awaiting evidence.
- [Dated source manifest](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — exact session provenance.

## Maintaining this index

Inventory every direct child, link directories through their README, and keep
the parent, component inventory, map and session evidence connected. Add a new
service only for a distinct responsibility; do not split or merge to meet a
numerical quota. Do not turn research completion into checked implementation.
