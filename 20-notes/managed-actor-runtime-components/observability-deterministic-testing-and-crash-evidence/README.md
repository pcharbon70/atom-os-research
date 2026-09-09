---
title: "Observability, deterministic testing and crash evidence: internal services"
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

# Observability, deterministic testing and crash evidence: internal services

## Purpose

Decompose the [parent component](../observability-deterministic-testing-and-crash-evidence.md) into independently
reviewable research contracts. These 4 studies separate state owners,
visibility decisions and residual lifetimes; they are not implementation phases.

## What belongs here

Keep service-level ownership, protocol alternatives, source findings, failure
cases and falsifiers here. Preserve the parent as the integrated component
model. Production traces, complete test schedules and crash evidence have different loss and trust contracts, even when they share an event schema.

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

- [Bounded trace streams, causality and privacy](bounded-trace-streams-causality-and-privacy.md) — covers stream schema, per-worker sequence, causal identifiers, filter generation and bounded ring capacity.
- [Deterministic choice log and external input capture](deterministic-choice-log-and-external-input-capture.md) — covers a replay manifest, enabled-choice set, ordered choices and recorded nondeterministic values.
- [Systematic exploration, differential oracles and shrinking](systematic-exploration-differential-oracles-and-shrinking.md) — covers executable invariants, bounded scenario models, differential observation rules and minimized failure artifacts.
- [Watchdog evidence and external crash custody](watchdog-evidence-and-external-crash-custody.md) — covers pre-registered bounded runtime descriptors, progress counters and optional crash sections.

## Cross-component boundaries

- [Failure evidence classification](../failure-translation-and-the-otp-boundary/typed-failure-provenance-and-compatible-projection.md) — shared ownership or observation boundary.
- [Observation and recovery limits](../resource-accounting-and-overload-control/pressure-states-and-protected-recovery-capacity.md) — shared ownership or observation boundary.
- [Runtime component inventory](../README.md) — all thirteen parent components.
- [Managed-runtime map](../../../10-maps/managed-actor-runtime.md) — selective research routes.
- [Open inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — decisions awaiting evidence.
- [Dated source manifest](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — exact session provenance.

## Maintaining this index

Inventory every direct child, link directories through their README, and keep
the parent, component inventory, map and session evidence connected. Add a new
service only for a distinct responsibility; do not split or merge to meet a
numerical quota. Do not turn research completion into checked implementation.
