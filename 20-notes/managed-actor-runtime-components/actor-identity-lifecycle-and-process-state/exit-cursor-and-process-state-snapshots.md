---
title: "Exit cursor and process-state snapshots"
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

# Exit cursor and process-state snapshots

This study decomposes [Actor identity, lifecycle and process state](../actor-identity-lifecycle-and-process-state.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

OTP's visible-resource release ordering does not imply immediate byte reclamation; thread-progress mechanisms distinguish stable observation from live mutation. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Actor identity is a managed routing concept. The registry does not create kernel protection between actors sharing one runtime.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own the actor's one selected exit outcome, a bounded cleanup cursor and versioned process-state summaries. Mutable execution state remains worker-owned; inspection requests use owner-coordinated snapshots. Diagnostics cannot read an arbitrary mixture of pre-GC pointers and post-exit counters.

### Admission, transitions and completion

Stop language execution, seal the reason, release or transfer visible resources, then publish relation outcomes. Continue residual binary, native and reader-pin draining under retained accounts. Snapshot requests name the actor generation and either return a coherent declared view or a typed unavailable/exiting outcome.

### Failure and adversarial behavior

A large exit reason and many monitors can exhaust cleanup capacity. Reserve representation lifetime before dropping the heap; never substitute a digest on a compatible exit path. PID-destination timers are cleaned by destination, not by which actor created them. Dirty native work may outlive the death observation.

### Alternatives and unresolved tradeoffs

Fully stopping an actor for every inspection simplifies consistency but can perturb latency. Versioned summary snapshots are cheaper and less detailed. The API must say which fields are mutually consistent and which are samples.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Kill an actor owning a named table, timer and large reason; verify visible cleanup precedes DOWN.
- Inspect during copying GC and reject stale interior pointers.
- Delay a native completion past actor death and retain its charge until release.

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
2. [Thread Progress](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md).
