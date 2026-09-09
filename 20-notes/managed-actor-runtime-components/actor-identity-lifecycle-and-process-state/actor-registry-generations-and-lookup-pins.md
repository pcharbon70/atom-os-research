---
title: "Actor registry generations and lookup pins"
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

# Actor registry generations and lookup pins

This study decomposes [Actor identity, lifecycle and process state](../actor-identity-lifecycle-and-process-state.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

OTP supplies PID semantics; hazard pointers show why removing an object and making its storage reusable are separate software events. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/michael-2004-hazard-pointers.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Actor identity is a managed routing concept. The registry does not create kernel protection between actors sharing one runtime.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own registry slots, internal generation/epoch, publication state and bounded lookup pins. The external PID representation and internal anti-stale key are related but not identical. An actor control block is not safe to dereference merely because a lookup found its slot.

### Admission, transitions and completion

Reserve a slot privately, publish a complete actor, acquire a reader pin before leaving lookup protection, then validate generation again. Exit removes new lookup visibility before retirement. Reuse requires both semantic death and drained old references; generation wrap must retire the slot or roll the domain epoch under explicit policy.

### Failure and adversarial behavior

A delayed sender holding an old pointer must not enqueue into a reused actor. Hazard-style pins bound specific retention but require a correct publication/recheck protocol and scan limits. Runtime memory corruption can forge any software pin; this is not a defense against a compromised collector.

### Alternatives and unresolved tradeoffs

Epoch reclamation makes frequent readers cheaper but a stalled participant can retain a large cohort. Explicit pins increase hot-path traffic but localize retention. Benchmark both under preemption and actor churn, not just lookup throughput.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Race lookup, exit and slot reuse with a paused producer.
- Exercise a deliberately tiny generation space to test wrap policy.
- Bound retired storage while one reader stalls indefinitely.

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
2. [Hazard pointers](../../../30-sources/michael-2004-hazard-pointers.md).
