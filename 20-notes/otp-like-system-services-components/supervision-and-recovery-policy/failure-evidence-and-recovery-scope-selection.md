---
title: "Failure evidence and recovery-scope selection"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Failure evidence and recovery-scope selection

This study decomposes [Supervision and recovery policy](../supervision-and-recovery-policy.md).

Research question: When does an observation justify restarting an actor, runtime domain or device group?

## Research basis and status

Microreboot depends on disposable execution; Lifeguard demonstrates that the
observer itself may be slow. [1](../../../30-sources/candea-et-al-2004-microreboot.md) [2](../../../30-sources/dadgar-et-al-2018-lifeguard.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The classifier owns authenticated observations, source incarnation, causal grouping
and recovery eligibility policy. Kernel terminal facts, application health claims
and remote suspicion remain distinct evidence classes. It cannot infer absence of
external effects from any one of them.

### Admission, transitions and completion

Correlate evidence to the current child and its declared failure domain. Evaluate
whether overload should trigger shedding, a transient fault permits local restart,
or corruption requires domain replacement. Select the smallest scope whose state and
authority can actually be reconstructed; record the reason and contradictory
evidence.

### Failure and adversarial behavior

A stale health report must not restart a successor. Correlated observer overload can
fabricate apparent child storms; downgrade confidence and preserve independent
signals. Malicious service reports may influence diagnosis but cannot grant
replacement authority.

### Alternatives and unresolved tradeoffs

Immediate restart reduces detection delay but can destroy useful state and amplify
gray failure. Waiting for corroboration improves confidence at availability cost.
Thresholds must be workload-qualified, with explicit operator escalation when no
decisive observation is possible.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Pause only the observer while children remain healthy; evaluate false recovery decisions separately from actual failures.
- Deliver one old termination report after replacement and ensure it cannot consume the successor's restart budget.

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

1. [Microreboot](../../../30-sources/candea-et-al-2004-microreboot.md).
2. [Lifeguard](../../../30-sources/dadgar-et-al-2018-lifeguard.md).
