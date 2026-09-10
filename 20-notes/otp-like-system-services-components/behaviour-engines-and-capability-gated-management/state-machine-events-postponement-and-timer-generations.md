---
title: "State-machine events, postponement, and timer generations"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# State-machine events, postponement, and timer generations

This study decomposes [Behaviour engines and capability-gated management](../behaviour-engines-and-capability-gated-management.md).

Research question: How can state-machine features remain bounded without claiming invisible OTP compatibility?

## Research basis and status

OTP specifies postponed events and timeout actions; explicit queues expose resource
costs but do not automatically impose bounds. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md) [2](../../../30-sources/welsh-et-al-2001-seda.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The engine owns current state revision, event classification, postponed-event
storage, named timer generations and ordered action processing. Runtime timer
delivery is a lower-layer mechanism; semantic expiry and event reconsideration
remain engine responsibilities.

### Admission, transitions and completion

Validate the complete callback action list before applying engine mutations. Charge
retained events and deferred replies separately from the ordinary mailbox. Every
reschedule or cancellation changes the timer generation; queued expiry events are
checked against it. Specify when a state transition reconsiders postponed events.

### Failure and adversarial behavior

An event may remain valid yet never become actionable. Native policy therefore
bounds retention and repeated reconsideration, producing a named exhaustion result.
A timer-cancel acknowledgement cannot remove a message already delivered; generation
validation prevents stale effects.

### Alternatives and unresolved tradeoffs

A strict OTP adapter must preserve documented action ordering and postponement
within admitted resources. Native finite postponement is an explicit divergence, not
a proof that all OTP programs terminate. Choosing fair reconsideration versus strict
transition ordering requires differential traces.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Cancel, rearm and deliver the original expiry after a state change; only the current timer may act.
- Generate indefinitely postponed traffic and require a measured memory ceiling and declared native/compatibility outcome.

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
