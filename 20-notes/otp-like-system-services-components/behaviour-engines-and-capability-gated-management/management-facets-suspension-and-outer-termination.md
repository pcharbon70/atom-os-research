---
title: "Management facets, suspension, and outer termination"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Management facets, suspension, and outer termination

This study decomposes [Behaviour engines and capability-gated management](../behaviour-engines-and-capability-gated-management.md).

Research question: How can management remain useful without becoming unrestricted inspection or relying on cooperation for containment?

## Research basis and status

sys suspension still services system messages; its termination request is not
synchronous proof of death. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md) [2](../../../30-sources/miller-et-al-2003-capability-myths.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The management gateway owns target-scoped operation facets, visibility projections,
suspension tokens and a finite control lane. The target owns cooperative snapshots.
A separate lifecycle holder owns forceful fencing and protected-domain teardown.

### Admission, transitions and completion

Authorize target incarnation, operation, fields, byte limit and lifetime before
dispatch. Suspend closes ordinary dispatch but does not imply drained work. Resume
must present the current suspension token. Termination returns request acceptance
separately from runtime terminal evidence and lower-layer resource settlement.

### Failure and adversarial behavior

A callback that never yields may prevent the engine from servicing even reserved
messages. The outer holder therefore remains independent of that queue and execution
domain. Snapshot recursion, secret fields and repeated deadline extension must be
rejected or bounded.

### Alternatives and unresolved tradeoffs

Library-local management has low overhead but trusts the target's interpreter.
External management can enforce access checks yet cannot safely fabricate arbitrary
application state. Prefer metadata-only inspection by default and explicitly
privilege richer snapshots.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Saturate normal and control queues independently; forceful replacement must not require a reply from the target.
- Reuse a suspension token after restart and attempt a secret-bearing snapshot through Inspect-only authority; both must fail.

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
2. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
