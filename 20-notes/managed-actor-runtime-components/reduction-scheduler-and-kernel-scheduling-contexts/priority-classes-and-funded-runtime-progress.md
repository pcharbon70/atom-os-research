---
title: "Priority classes and funded runtime progress"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - actor-model
  - beam
  - managed-runtime
  - system-architecture
aliases: []
---

# Priority classes and funded runtime progress

This study decomposes [Reduction scheduler and kernel scheduling contexts](../reduction-scheduler-and-kernel-scheduling-contexts.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

OTP priority and kernel budget are different mechanisms; overload studies show that feedback and finite queues do not automatically guarantee latency. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md), [3](../../../30-sources/welsh-et-al-2001-seda.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Runtime reductions select actors; kernel contexts enforce CPU authority. Neither is a hard real-time guarantee by itself.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own runtime work-class queues, priority selection state and capped control/GC/cleanup reserve. Actor-selected priority cannot relabel ordinary computation as mandatory system work. Supervisors select application policy above these mechanisms.

### Admission, transitions and completion

Admit work against its class before queueing, choose actors under the compatibility profile and dispatch system tasks in bounded slices. Reserve capacity for progressing terminal cleanup and evidence even when ordinary admission closes. Record starvation and reserve exhaustion as outcomes, not hidden scheduler exceptions.

### Failure and adversarial behavior

An infinite high-priority actor or a priority-message flood can starve lower-priority work under compatible semantics. Inventing fairness silently may break observations; claiming strict responsiveness without a restricted profile is equally misleading. A recovery reserve is finite and can force domain escalation.

### Alternatives and unresolved tradeoffs

Separate reserve queues simplify audit but add scheduling decisions. One queue with trusted class tags is possible if actors cannot forge them. Compare overhead and starvation under the same budget grants, not only throughput.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Flood ordinary queues and prove reserved cleanup remains schedulable within declared assumptions.
- Attempt to charge actor work to the recovery class.
- Exercise sustained high-priority load and report starvation honestly for the selected profile.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Safe-point handoff](../code-execution-safe-points-and-version-publication/canonical-safe-point-and-native-helper-state.md) — a contract this service must compose with.
- [Funded control and recovery](../resource-accounting-and-overload-control/pressure-states-and-protected-recovery-capacity.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
2. [Scheduling-context capabilities](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md).
3. [SEDA](../../../30-sources/welsh-et-al-2001-seda.md).
