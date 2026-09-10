---
title: "Audit intent/outcome integrity and witness progress"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Audit intent/outcome integrity and witness progress

This study decomposes [Observability, audit, alarms, and operator control](../observability-audit-alarms-and-operator-control.md).

Research question: Which tampering and omission can a security audit trail actually detect?

## Research basis and status

Forward-integrity logging protects covered history under erasure assumptions;
crash-safe persistence is a separate requirement. [1](../../../30-sources/schneier-kelsey-1999-secure-audit-logs.md) [2](../../../30-sources/chen-et-al-2015-fscq.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The audit service owns framed records, sequence and epoch,
authorization/intent/outcome linkage, key evolution and witnessed frontier.
Producers own reported observations; a trusted mediator must cover mandatory
authority changes if completeness is claimed.

### Admission, transitions and completion

Reserve audit capacity and durably record intent before the protected effect. Record
independent outcome evidence afterward, retaining uncertainty when the outcome is
unavailable. Checkpoint authenticated progress to a separate witness. Recovery
validates chain, durable prefix and externally known high-water state.

### Failure and adversarial behavior

Chaining cannot prove a compromised producer told the truth or emitted an event. A
locally valid old chain can hide rollback without an external anchor. If audit is
mandatory and unavailable, fail closed or use a predeclared separately reserved
evidence path; ordinary telemetry dropping is not acceptable.

### Alternatives and unresolved tradeoffs

Frequent witnessing reduces the unanchored interval but adds availability
dependencies. Protected key handles may improve confinement, yet forward-integrity
claims still require actual old-key erasure and rollback analysis. Modern
cryptographic choices remain unselected, not inherited from a 1999 construction.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Truncate or restore a valid old log and compare against the witness; report the gap instead of accepting current completeness.
- Crash after audit intent and after the effect; the recovered history must preserve pending/known outcome distinctions.

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

1. [Secure audit logs](../../../30-sources/schneier-kelsey-1999-secure-audit-logs.md).
2. [FSCQ](../../../30-sources/chen-et-al-2015-fscq.md).
