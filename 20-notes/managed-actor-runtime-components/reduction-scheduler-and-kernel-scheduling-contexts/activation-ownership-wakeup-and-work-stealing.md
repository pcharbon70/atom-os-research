---
title: "Activation ownership, wakeup and work stealing"
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

# Activation ownership, wakeup and work stealing

This study decomposes [Reduction scheduler and kernel scheduling contexts](../reduction-scheduler-and-kernel-scheduling-contexts.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Actor scheduling research finds locality benefits and affinity-induced contention; progress protocols require a defined participant set. [1](../../../30-sources/barghi-karsten-2018-locality-aware-actor-scheduling.md), [2](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Runtime reductions select actors; kernel contexts enforce CPU authority. Neither is a hard real-time guarantee by itself.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own each actor's runnable/running/waiting claim, local queue membership and wakeup generation. A worker may execute an actor only after acquiring its unique activation ownership. Queue topology never changes PID identity or permits simultaneous mutators.

### Admission, transitions and completion

Publish work before issuing a wake. The waking producer and a blocking actor coordinate one transition to runnable. Stealing moves a claimable activation, not a currently executing actor. Migration hands over canonical state and accounting before another worker can run it.

### Failure and adversarial behavior

A stale runnable entry, duplicate wake or concurrent thief must not create two owners. A worker disappearing under context revocation leaves a queue-drain obligation. Locality hints can be stale without violating correctness, but queue ownership cannot.

### Alternatives and unresolved tradeoffs

Start with local queues and randomized victims as a comparison model. Hierarchical stealing is optional measured policy; retaining home affinity can create remote enqueue locks and long tails. Track migration, idle search and queue-delay distributions together.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Race wakeup with actor sleep and two simultaneous thieves.
- Revoke a worker while it owns runnable entries but no running actor.
- Compare locality policies under fan-in, short actors and uneven kernel budgets.

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

1. [Locality-aware actor scheduling](../../../30-sources/barghi-karsten-2018-locality-aware-actor-scheduling.md).
2. [Thread Progress](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md).
