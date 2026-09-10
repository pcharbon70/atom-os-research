---
title: "Event-router subscriber isolation and delivery classes"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Event-router subscriber isolation and delivery classes

This study decomposes [Behaviour engines and capability-gated management](../behaviour-engines-and-capability-gated-management.md).

Research question: What does event publication mean when subscribers have different failure and loss contracts?

## Research basis and status

OTP gen_event shares a manager process; independently queued subscribers are a
different native abstraction. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md) [2](../../../30-sources/welsh-et-al-2001-seda.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The router owns subscription generations, projections, per-subscriber credits and
admission receipts. Subscribers own processing and durable acknowledgements. A
subscription is both a disclosure decision and a finite retention commitment, not an
unrestricted callback registration.

### Admission, transitions and completion

Classify each event as lossy, latest-value, sticky condition or acknowledged
history. Project fields before crossing subscriber authority boundaries. Publication
reports which declared admission condition was met; it does not claim subscriber
execution or atomic broadcast. Removal closes a generation before reclaiming queued
references.

### Failure and adversarial behavior

A stalled subscriber cannot consume all router capacity. Reliable classes reject,
backpressure or require durable replay; they cannot silently inherit telemetry
dropping. Subscriber restart invalidates its old credits and acknowledgements.
Callback execution inside one manager remains shared-fate compatibility behavior.

### Alternatives and unresolved tradeoffs

Per-subscriber actors improve isolation but add scheduling and fanout cost. Group
queues reduce overhead while coupling latency and secrecy. Choose placement from
failure and disclosure needs, and preserve the explicit absence of a portable
gen_event handler-order guarantee.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Stall one subscriber while others progress; account all retained bytes and overflow results.
- Replay an old subscriber acknowledgement after replacement and verify it cannot release a current delivery obligation.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Supervision and recovery policy](../supervision-and-recovery-policy/README.md) — owns restart admission, quarantine and escalation.
- [Observability, audit, alarms, and operator control](../observability-audit-alarms-and-operator-control/README.md) — separates diagnostic, audit and operator-control obligations.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [OTP 29.0.6 system-services documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md).
2. [SEDA](../../../30-sources/welsh-et-al-2001-seda.md).
