---
title: "Spawn transaction and atomic relations"
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

# Spawn transaction and atomic relations

This study decomposes [Actor identity, lifecycle and process state](../actor-identity-lifecycle-and-process-state.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Compatible spawn/link/monitor operations have observable atomicity obligations; Concuerror demonstrates the importance of scheduling immediately around spawn. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/christakis-et-al-2013-concuerror.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Actor identity is a managed routing concept. The registry does not create kernel protection between actors sharing one runtime.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own an unpublished actor record, argument-copy arena, initial frame, account reservation and any requested parent relation. Registry, scheduler and relation managers participate without exposing independent partial success. Spawn is not just allocating a stack.

### Admission, transitions and completion

Reserve all required metadata, copy arguments into the child's private ownership and construct a valid first continuation. Install required link/monitor state consistently with concurrent parent exit. Publish the PID and exactly one runnable activation only after the chosen spawn operation can satisfy its contract.

### Failure and adversarial behavior

Failure before publication rolls back every reservation. Failure afterward is actor termination, not disappearance of a returned PID. Parent exit between relation installation and publication needs a modeled outcome; a retry must not accidentally create twins because a reply was lost.

### Alternatives and unresolved tradeoffs

One lifecycle lock offers a clear baseline but can bottleneck spawn storms. Distributed commit-style ownership claims may scale better while increasing failure windows. Preserve the same observable history when optimizing the internal protocol.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Inject OOM after every allocation and check for orphan relation records.
- Race linked spawn against parent exit and child immediate exit.
- Replay simultaneous spawn wakeups and verify the child never runs on two workers.

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
2. [Concuerror](../../../30-sources/christakis-et-al-2013-concuerror.md).
