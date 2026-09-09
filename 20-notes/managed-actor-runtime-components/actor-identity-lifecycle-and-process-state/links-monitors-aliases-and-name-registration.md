---
title: "Links, monitors, aliases and name registration"
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

# Links, monitors, aliases and name registration

This study decomposes [Actor identity, lifecycle and process state](../actor-identity-lifecycle-and-process-state.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Signals carry relation semantics; mailbox insertion and name lookup are separate observations from merely constructing an actor reference. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/hogberg-2021-message-passing.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Actor identity is a managed routing concept. The registry does not create kernel protection between actors sharing one runtime.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own symmetric links, independent monitor references, alias activation state and registered-name bindings. Each relation binds actor generations. These objects may share storage helpers, but their cancellation, multiplicity and observation rules remain distinct.

### Admission, transitions and completion

Serialize relation installation with target death and publish one terminal monitor observation for each active monitor. Treat aliases as revocable message destinations; the signal owner rechecks activity at mailbox insertion. Registered names resolve to a live binding for the operation that uses them, not a permanent identity for all future sends.

### Failure and adversarial behavior

Deactivating an alias removes future insertion permission, not an already queued reply and not an external operation's effect. Reusing a name does not recreate old links or monitors. A copied PID or reference grants only the language operations allowed by the selected profile, never raw adapter authority.

### Alternatives and unresolved tradeoffs

A unified relation table can simplify accounting but must retain typed state transitions. Separate tables avoid overloaded flags but require a cross-table exit protocol. Choose by measured contention and proof clarity, not by assuming all references have monitor semantics.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Race alias deactivation after signal publication but before mailbox insertion.
- Create repeated monitors and verify separate references and terminal observations.
- Unregister and re-register a name during sends without redirecting old generation-bound relations.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Generation-bound signal publication](../signal-ingress-mailboxes-and-selective-receive/signal-envelope-admission-and-payload-transfer.md) — a contract this service must compose with.
- [Exit outcome and fan-out](../failure-translation-and-the-otp-boundary/termination-reason-lifetime-and-bounded-fanout.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
2. [A few notes on message passing](../../../30-sources/hogberg-2021-message-passing.md).
