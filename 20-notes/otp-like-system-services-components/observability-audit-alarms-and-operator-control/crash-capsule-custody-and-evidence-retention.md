---
title: "Crash-capsule custody and evidence retention"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Crash-capsule custody and evidence retention

This study decomposes [Observability, audit, alarms, and operator control](../observability-audit-alarms-and-operator-control.md).

Research question: What evidence can survive a failed runtime without trusting its normal logger?

## Research basis and status

Sampled tracing is not guaranteed crash evidence; access to diagnostic state needs
separately scoped authority. [1](../../../30-sources/sigelman-et-al-2010-dapper.md) [2](../../../30-sources/miller-et-al-2003-capability-myths.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The evidence service owns pre-reserved domain-level capsule capacity, terminal
identity/generation, bounded fault metadata and retention policy. Lower layers
supply trustworthy terminal facts where available. Service-reported context remains
separately labeled and may be missing or false.

### Admission, transitions and completion

Reserve capture capacity before failure and select a minimal redacted record.
Transfer custody to a surviving evidence holder without depending on the failed
allocator, exporter or actor callback. Correlate later traces and audit by identity
while preserving their distinct reliability and trust classes.

### Failure and adversarial behavior

A million actors cannot each receive an unbounded dump reservation. Repeated crashes
can overwrite finite evidence only under declared priority/rotation policy.
Credential bytes and arbitrary heaps are excluded by default; comprehensive forensic
disclosure requires specific authority and cannot be assumed safe.

### Alternatives and unresolved tradeoffs

Per-domain shared pools scale better but may lose individual detail during storms.
Dedicated records for critical domains improve coverage at fixed cost. Capture
survival across runtime crash, machine reboot and power loss are different profiles
requiring separate evidence.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Crash the runtime with its allocator and logger unavailable; the reserved capsule path must not require either.
- Trigger more faults than retention capacity and verify explicit loss/rotation reporting without secret leakage or unbounded allocation.

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

1. [Dapper](../../../30-sources/sigelman-et-al-2010-dapper.md).
2. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
