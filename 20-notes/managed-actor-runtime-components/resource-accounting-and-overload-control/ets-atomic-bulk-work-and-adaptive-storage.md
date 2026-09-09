---
title: "ETS atomic bulk work and adaptive storage"
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

# ETS atomic bulk work and adaptive storage

This study decomposes [Resource accounting and overload control](../resource-accounting-and-overload-control.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Yielding ETS helpers can publish continuation state for assistance; scalable counters illustrate that shared metadata can dominate an otherwise fine-grained structure. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/erlang-otp-team-2026-yielding-c-code-contracts.md), [3](../../../30-sources/winblad-2021-decentralized-ets-counters.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Runtime ledgers attribute consumption beneath hard kernel domain limits; actor policy cannot mint memory, CPU or cleanup reserve.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own per-table operation descriptors, private preparation, mutation commit and retired storage. Table type, concurrency hints and traversal semantics come from the selected profile. Internal slicing must not weaken whole-operation atomicity.

### Admission, transitions and completion

Prepare list inserts or deletions in bounded work units, reserve destination and rollback capacity, then commit at the operation's defined visibility boundary. If other workers help a published operation, each claims disjoint work and observes one terminal result. Keep retained old structure alive for qualified traversals.

### Failure and adversarial behavior

Exposing partial list insert/insert_new or delete_all_objects effects merely to yield is not acceptable where the profile guarantees atomicity. Owner exit during a shared operation cannot free the continuation another worker is helping. Approximate size hints may select resizing but not replace exact resource admission.

### Alternatives and unresolved tradeoffs

Hashing, ordered trees and immutable snapshots suit different workloads. Adaptive locking can reduce contention but adds transitions that require their own invariants. A small coarse-lock reference model remains useful for history comparison; no universal data structure is selected here.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Pause each slice while concurrent readers check whole-operation atomicity.
- Kill the initiating actor during a helpable shared operation.
- Compare read/write/scan mixes and report contention, retained bytes and exact-size query cost together.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Shared-object retention](../terms-private-heaps-shared-binaries-and-tracing-collection/shared-binary-literal-and-fragment-lifetimes.md) — a contract this service must compose with.
- [Bounded shared-operation work](../reduction-scheduler-and-kernel-scheduling-contexts/reduction-costs-and-yieldable-work-continuations.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
2. [Automatic Yielding of C Code](../../../30-sources/erlang-otp-team-2026-yielding-c-code-contracts.md).
3. [Decentralized ETS counters](../../../30-sources/winblad-2021-decentralized-ets-counters.md).
