---
title: "Causal resource accounts and fanout reservations"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Causal resource accounts and fanout reservations

This study decomposes [Admission, overload, and service-resource governance](../admission-overload-and-service-resource-governance.md).

Research question: How does asynchronous work remain charged to an authenticated owner?

## Research basis and status

Attenuated authority and explicit service stages motivate accountable delegation;
they do not prove multi-resource conservation. [1](../../../30-sources/miller-et-al-2003-capability-myths.md) [2](../../../30-sources/welsh-et-al-2001-seda.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The account service owns principal and service budgets, unique reservations, child
allocation lineage and protected control/recovery minima. Runtime reductions and
kernel memory enforcement are underlying mechanisms, not substitutes for
service-level causal attribution.

### Admission, transitions and completion

At admission bind operation identity to an authoritative account. Fanout subdivides
unique credits or atomically charges one shared ledger; copied numeric balances are
not spendable authority. Retained replies, timers, callbacks, downstream I/O and
deduplication records all retain an accountable owner.

### Failure and adversarial behavior

Detached work must obtain a new authorized account rather than disappearing into
system overhead. A replayed child reservation cannot be spent twice. When an owner
crashes, pending consumption remains charged until settlement or transfer; revoking
a handle does not make in-flight resources free.

### Alternatives and unresolved tradeoffs

Hierarchical static partitions simplify guarantees but may waste idle capacity.
Shared dynamic accounts improve utilization while adding contention and failure
recovery. Borrowing protected recovery resources requires a proved recall bound or
must remain forbidden.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Duplicate the same fanout reservation across concurrent actors; total admitted resource use must not exceed the parent grant.
- Crash the origin after downstream acceptance and verify all retained work still has a live custodian and charge.

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

1. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
2. [SEDA](../../../30-sources/welsh-et-al-2001-seda.md).
