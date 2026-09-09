---
title: "Clock era and timer destination contract"
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

# Clock era and timer destination contract

This study decomposes [Timers, events and asynchronous I/O integration](../timers-events-and-asynchronous-io-integration.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Timer data structures do not define language timer semantics; the selected OTP contract distinguishes PID and registered-name destinations. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/varghese-lauck-1987-timing-wheels.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. The runtime owns timer and actor semantics; the kernel supplies qualified time and deadline events, not one kernel timer per actor.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own conversion from timer arguments to a checked monotonic deadline, clock era and destination descriptor. PID timers bind an exact actor incarnation; name timers retain the name for resolution at expiry. Creator identity is accounting provenance, not universally the timer's lifetime owner.

### Admission, transitions and completion

Validate arithmetic and clock quality at arm time. Index PID timers by destination for exit and suspension handling. Under the parent OTP profile, suspension pauses PID-destination BIF timers; name-destination timers continue and resolve the current registration at expiry. Keep this distinction explicit in serialization and migration.

### Failure and adversarial behavior

A creator's exit must not cancel an unrelated surviving destination's timer. Name reuse may legitimately redirect a name timer, unlike a stale PID timer. If the clock era becomes invalid, record a typed failure or an explicitly profiled rebasing transition; do not pretend civil-clock adjustment is monotonic elapsed time.

### Alternatives and unresolved tradeoffs

Relative storage can make suspension natural but complicates migration; absolute deadlines simplify expiry comparisons but need remaining-duration capture. Either representation needs overflow and era checks. No wheel geometry resolves these semantic choices.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Exit the timer creator while a distinct PID destination remains alive.
- Suspend PID and name destinations and compare behavior with the pinned reference.
- Change name registration before expiry and reject any old-PID redirection in the PID case.

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
