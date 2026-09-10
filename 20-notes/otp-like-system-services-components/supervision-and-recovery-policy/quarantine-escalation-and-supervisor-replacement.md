---
title: "Quarantine, escalation, and supervisor replacement"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Quarantine, escalation, and supervisor replacement

This study decomposes [Supervision and recovery policy](../supervision-and-recovery-policy.md).

Research question: Who retains responsibility when local recovery cannot safely complete?

## Research basis and status

Revocation limits future authority, while recovery escalation requires a holder
outside the scope being destroyed. [1](../../../30-sources/miller-et-al-2003-capability-myths.md) [2](../../../30-sources/candea-et-al-2004-microreboot.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The quarantine custodian owns unresolved operation references, unsafe resources,
deadlines and escalation evidence. The outer holder owns the authority and reserve
to replace the supervisor itself. A quarantine entry is retained responsibility, not
a garbage-collection hint.

### Admission, transitions and completion

On exhausted budget or indeterminate teardown, close admission and transfer a
durable obligation record to the custodian. Escalation preserves the original
operation identities and reason chain. A replacement supervisor recovers outstanding
attempts before accepting new policy changes.

### Failure and adversarial behavior

Clearing an alarm or acknowledging quarantine must not release unsafe buffers.
Operator overrides require narrowly scoped authority and an audited new decision;
they cannot rewrite unknown effects as absent. If the outer holder is also lost, the
declared wider failure domain owns recovery.

### Alternatives and unresolved tradeoffs

Automatic escalation reduces manual intervention but can cascade into unnecessary
system-wide outage. Permanent quarantine protects integrity at finite capacity cost.
The design must name the terminal recovery boundary and reject new work when
retained obligations exhaust storage.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Kill the supervisor during group recovery and verify its replacement inherits unresolved attempts without duplicating effects.
- Acknowledge quarantine without a reclamation proof and ensure resources remain unavailable.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Admission, overload, and service-resource governance](../admission-overload-and-service-resource-governance/README.md) — budgets retained work, retries and recovery.
- [Durable state, transactions, and outcome recovery](../durable-state-transactions-and-outcome-recovery/README.md) — retains committed state and retry-result responsibility.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
2. [Microreboot](../../../30-sources/candea-et-al-2004-microreboot.md).
