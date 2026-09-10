---
title: "Pressure observation, fair admission, and degradation"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Pressure observation, fair admission, and degradation

This study decomposes [Admission, overload, and service-resource governance](../admission-overload-and-service-resource-governance.md).

Research question: How can the system reject excess demand without confusing overload with service failure?

## Research basis and status

DAGOR uses local queue delay and propagated admission levels; SEDA's measured
control behavior did not establish hard latency guarantees. [1](../../../30-sources/zhou-et-al-2018-dagor.md) [2](../../../30-sources/welsh-et-al-2001-seda.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The admission controller owns server-observed pressure, per-principal shares,
authenticated service classes, thresholds and declared degraded modes. Applications
define semantic importance; callers cannot promote themselves by submitting a
priority integer.

### Admission, transitions and completion

Authenticate and check deadlines before expensive work. Reserve minimum retained and
downstream capacity, then admit, reject, bounded-wait or select an explicit smaller
contract. Apply hysteresis and rate-limited recovery using local queue age, service
time, retained bytes and dependency pressure rather than CPU alone.

### Failure and adversarial behavior

Stale downstream feedback can admit doomed fanout or reject healthy work. Missing
telemetry is not healthy evidence. Low-priority work can starve unless fairness and
minimum service rules are explicit. Restarting a merely overloaded service may
worsen its backlog and destroy warm state.

### Alternatives and unresolved tradeoffs

Static admission is auditable but less adaptive; feedback improves utilization while
adding oscillation and estimation risks. Degradation must expose its reduced
freshness, scope or fidelity in the result type. No source's numeric thresholds are
portable Atom OS defaults.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Apply step, burst and slow-dependency loads; report useful completion, false rejection, tail latency and fairness together.
- Forge emergency priority and remove metrics; neither condition may grant unbounded capacity or a false healthy state.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Supervision and recovery policy](../supervision-and-recovery-policy/README.md) — owns restart admission, quarantine and escalation.
- [Network endpoint and protocol services](../network-endpoint-and-protocol-services/README.md) — separates transport session state from application outcomes.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [DAGOR](../../../30-sources/zhou-et-al-2018-dagor.md).
2. [SEDA](../../../30-sources/welsh-et-al-2001-seda.md).
