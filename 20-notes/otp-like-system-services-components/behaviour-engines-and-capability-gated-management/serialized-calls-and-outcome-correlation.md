---
title: "Serialized calls and outcome correlation"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Serialized calls and outcome correlation

This study decomposes [Behaviour engines and capability-gated management](../behaviour-engines-and-capability-gated-management.md).

Research question: Which operation state survives a caller timeout or late reply?

## Research basis and status

OTP call timeouts stop waiting rather than cancel execution; RIFL makes stronger
retry semantics conditional on retained results. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md) [2](../../../30-sources/lee-et-al-2015-rifl.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The engine owns caller references, accepted request digests, callback state and
bounded reply slots. Durable business outcomes belong to the outcome service or
application, not the volatile call table. Service identity, actor incarnation and
logical operation identity are separate.

### Admission, transitions and completion

Reserve a reply slot before admission. Serialize callback entry while permitting
explicit asynchronous continuations whose state version is rechecked. Expiring a
caller alias closes delivery to that caller generation, not the accepted effect. A
retry retains its logical operation identity while receiving a new transport
correlation reference.

### Failure and adversarial behavior

A callback crash after an effect but before reply produces uncertainty. Never replay
solely because the old caller stopped waiting. Different request bodies using the
same logical identity must fail. A cast's successful submission cannot stand for
acknowledged execution.

### Alternatives and unresolved tradeoffs

Keeping every callback synchronous is simple but lets long work block management.
Splitting work permits responsiveness but requires explicit continuation validity.
Native acceptance states are an opt-in API, not a silent change to documented OTP
tuples.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Deliver a delayed reply after caller-slot reuse and ensure the new call cannot complete from it.
- Crash after effect completion before reply; require retained outcome lookup or Indeterminate, not unconditional retry.

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
2. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
