---
title: "Expiry, cancel, suspend and deadline-rearm arbitration"
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

# Expiry, cancel, suspend and deadline-rearm arbitration

This study decomposes [Timers, events and asynchronous I/O integration](../timers-events-and-asynchronous-io-integration.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

OTP cancellation observations are weaker than a universal no-message guarantee; a timer structure alone supplies no cancellation linearization rule. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/varghese-lauck-1987-timing-wheels.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. The runtime owns timer and actor semantics; the kernel supplies qualified time and deadline events, not one kernel timer per actor.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own each timer's armed/suspended/due/published/cancelled state and the token for the shard's earliest kernel deadline. Timer reference generation, actor generation and clock era remain separate checks. A wakeup token identifies an arm attempt, not proof of expiry.

### Admission, transitions and completion

Serialize cancel, target suspension/exit and expiry around one terminal publication decision. Preserve remaining duration when the profile pauses a PID timer. Re-arm the lower deadline after inspecting the current earliest timer; use a generation to reject obsolete callbacks and poll sticky completion state after coalescing.

### Failure and adversarial behavior

Cancel losing to publication does not retract a mailbox message. An extra old wake is harmless if it triggers re-evaluation rather than an unconditional send. Record deadline, due recognition, signal publication and actor consumption separately so lateness can be attributed.

### Alternatives and unresolved tradeoffs

A single shard lock provides a tractable reference model; lock-free terminal claims can reduce contention but still need payload lifetime and rearm serialization. Compatibility may expose only a Boolean or remaining time while diagnostics retain the actual internal race outcome.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Race cancel with expiry before and after signal publication.
- Suspend a PID destination while its deadline wake is queued.
- Deliver stale and duplicate kernel wakeups; publish at most one timeout for each timer generation.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Timeout consumption and receive races](../signal-ingress-mailboxes-and-selective-receive/selective-receive-cursors-markers-and-timeouts.md) — a contract this service must compose with.
- [External request disposition](../native-work-ports-and-drivers/native-request-outcomes-and-cancellation-drain.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
2. [Hashed and hierarchical timing wheels](../../../30-sources/varghese-lauck-1987-timing-wheels.md).
