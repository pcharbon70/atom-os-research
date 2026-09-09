---
title: "Failure translation and the OTP boundary: internal services"
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

# Failure translation and the OTP boundary: internal services

## Purpose

Decompose the [parent component](../failure-translation-and-the-otp-boundary.md) into independently
reviewable research contracts. These 4 studies separate state owners,
visibility decisions and residual lifetimes; they are not implementation phases.

## What belongs here

Keep service-level ownership, protocol alternatives, source findings, failure
cases and falsifiers here. Preserve the parent as the integrated component
model. The runtime implements observations and actor termination; OTP-like services choose restart policy, and an outer service handles runtime corruption.

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

- [Typed failure provenance and compatible projection](typed-failure-provenance-and-compatible-projection.md) — covers a typed event with subject generation, origin, evidence class, operation phase and exact semantic reason.
- [Termination reason lifetime and bounded fan-out](termination-reason-lifetime-and-bounded-fanout.md) — covers recovery-held reason storage and fan-out cursors after actor execution stops.
- [Service loss, uncertainty and supervisor handoff](service-loss-uncertainty-and-supervisor-handoff.md) — covers the translation from service/gateway operation evidence into runtime events.
- [Outer runtime failure and new-epoch recovery](outer-runtime-failure-and-new-epoch-recovery.md) — covers the runtime-facing evidence and shutdown protocol, while the outer supervisor owns domain freeze, teardown and successor launch.

## Cross-component boundaries

- [Actor cleanup ownership](../actor-identity-lifecycle-and-process-state/exit-cursor-and-process-state-snapshots.md) — shared ownership or observation boundary.
- [Independent evidence custody](../observability-deterministic-testing-and-crash-evidence/watchdog-evidence-and-external-crash-custody.md) — shared ownership or observation boundary.
- [Runtime component inventory](../README.md) — all thirteen parent components.
- [Managed-runtime map](../../../10-maps/managed-actor-runtime.md) — selective research routes.
- [Open inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — decisions awaiting evidence.
- [Dated source manifest](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — exact session provenance.

## Maintaining this index

Inventory every direct child, link directories through their README, and keep
the parent, component inventory, map and session evidence connected. Add a new
service only for a distinct responsibility; do not split or merge to meet a
numerical quota. Do not turn research completion into checked implementation.
