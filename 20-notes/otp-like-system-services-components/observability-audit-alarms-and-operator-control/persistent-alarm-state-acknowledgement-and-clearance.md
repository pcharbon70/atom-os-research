---
title: "Persistent alarm state, acknowledgement, and clearance"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Persistent alarm state, acknowledgement, and clearance

This study decomposes [Observability, audit, alarms, and operator control](../observability-audit-alarms-and-operator-control.md).

Research question: How can operators acknowledge an incident without erasing an unresolved condition?

## Research basis and status

Crash-consistent state and OTP's limited alarm-handler abstraction motivate a
separate persistent alarm lifecycle. [1](../../../30-sources/chen-et-al-2015-fscq.md) [2](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The alarm controller owns condition identity, resource generation, evidence
references, severity, debounce state, acknowledgement and suppression expiry.
Notification delivery is a separate lossy or retried channel; sending an alert is
not the alarm state itself.

### Admission, transitions and completion

Persist the condition transition and deduplication key before reporting an
acknowledged state change. Acknowledge records operator awareness; clear requires
the type-specific predicate and hold-down. Suppression has an expiry and must not
delete the active condition or underlying evidence.

### Failure and adversarial behavior

Controller restart reloads current alarms and rechecks conditions rather than
resetting everything to healthy. A delayed clear from an old device generation
cannot clear its successor's fault. Contradictory observations remain visible as
perspectives instead of being replaced by the latest Boolean.

### Alternatives and unresolved tradeoffs

Durable alarms cost storage and must have cardinality quotas. Coalescing by resource
controls storms but can hide distinct causes unless evidence remains linked. Exact
auto-clear policy is domain-specific and cannot be supplied by a generic supervisor
or log parser.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Acknowledge an active fault, restart the controller and verify the condition remains active until its clear predicate passes.
- Expire suppression during notification outage; persistent alarm state must reactivate without depending on message delivery.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Configuration, workload identity, and secrets](../configuration-workload-identity-and-secrets/README.md) — supplies configuration adoption and credential-generation evidence.
- [Supervision and recovery policy](../supervision-and-recovery-policy/README.md) — owns restart admission, quarantine and escalation.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [FSCQ](../../../30-sources/chen-et-al-2015-fscq.md).
2. [OTP 29.0.6 system-services documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md).
