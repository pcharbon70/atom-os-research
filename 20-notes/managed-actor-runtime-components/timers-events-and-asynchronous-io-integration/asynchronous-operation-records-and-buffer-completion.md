---
title: "Asynchronous operation records and buffer completion"
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

# Asynchronous operation records and buffer completion

This study decomposes [Timers, events and asynchronous I/O integration](../timers-events-and-asynchronous-io-integration.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

CleanQ treats queues as ownership transfer; asynchronous resource accounting must continue after the initiating actor stops waiting. [1](../../../30-sources/haecki-et-al-2019-cleanq.md), [2](../../../30-sources/banga-et-al-1999-resource-containers.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. The runtime owns timer and actor semantics; the kernel supplies qualified time and deadline events, not one kernel timer per actor.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own request identity, caller/service incarnations, buffer leases, terminal result slot and readiness subscription. Readiness means an operation might progress; completion means the request reached a protocol-defined terminal state. Neither is inferred from the other.

### Admission, transitions and completion

Reserve request and result capacity before submission. On readiness, perform bounded work then re-arm using a check-before-sleep protocol. On completion, validate every generation, publish one actor observation if still eligible and release storage only after the lower ownership protocol returns it.

### Failure and adversarial behavior

Timeout or alias deactivation ends actor interest but may leave a service or device accessing the buffer. Cancellation acknowledgement is not hardware quiescence. Late results for dead actors still trigger old-operation cleanup, while no successor receives their payload.

### Alternatives and unresolved tradeoffs

Copying into service-owned memory simplifies lifetime but adds cost. Shared immutable buffers require explicit leases and protection; shared mutable access needs a stronger protocol. Select by operation class rather than declaring all I/O zero-copy.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Cancel after submission and delay the original completion while attempting buffer reuse.
- Drop readiness notifications and exercise poll/rearm recovery.
- Restart the service and deliver a completion carrying its old incarnation.

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

1. [CleanQ](../../../30-sources/haecki-et-al-2019-cleanq.md).
2. [Resource containers](../../../30-sources/banga-et-al-1999-resource-containers.md).
