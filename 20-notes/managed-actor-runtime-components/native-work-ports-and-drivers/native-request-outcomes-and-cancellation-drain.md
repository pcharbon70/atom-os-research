---
title: "Native request outcomes and cancellation drain"
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

# Native request outcomes and cancellation drain

This study decomposes [Native work, ports and drivers](../native-work-ports-and-drivers.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Ownership transfer and failure knowledge are distinct: losing a service route does not establish that an external operation never happened. [1](../../../30-sources/haecki-et-al-2019-cleanq.md), [2](../../../30-sources/chandra-toueg-1996-failure-detectors.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Protected service domains are the default native boundary. Regular and dirty NIFs remain inside the runtime memory-failure domain.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own request identity, caller/service generations, publication phase, terminal outcome and residual cleanup. Distinguish actor interest from operation execution and from resource disposition. A caller timeout is not a terminal effect record.

### Admission, transitions and completion

Reserve a terminal slot, encode and submit, then record the exact transport and service acceptance boundaries. Complete with protocol evidence, cancel before effect when proven, or retain Indeterminate after loss when nonexecution cannot be established. Stop routing late replies to a dead caller while continuing request cleanup.

### Failure and adversarial behavior

Loss immediately after endpoint publication can be indeterminate even without a service acknowledgement. Releasing the request on cancel acknowledgement can reuse a buffer still in use. Duplicate terminal replies must be idempotently reconciled, not decrement credits twice.

### Alternatives and unresolved tradeoffs

A stronger service-specific receipt/deduplication protocol can reduce uncertainty but needs retained result state and a defined effect boundary. It is not a generic property of ports, TCP or retries. Keep default retry policy outside the runtime.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Lose the service between publication and acknowledgement and reject a fabricated NotExecuted result.
- Timeout the caller, then deliver effect completion and cancellation acknowledgement in both orders.
- Repeat terminal messages and verify one result and one resource release.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [I/O ownership and terminal completion](../timers-events-and-asynchronous-io-integration/asynchronous-operation-records-and-buffer-completion.md) — a contract this service must compose with.
- [Failure projection without unsafe retry](../failure-translation-and-the-otp-boundary/service-loss-uncertainty-and-supervisor-handoff.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [CleanQ](../../../30-sources/haecki-et-al-2019-cleanq.md).
2. [Unreliable failure detectors](../../../30-sources/chandra-toueg-1996-failure-detectors.md).
