---
title: "Private heap allocation and generational invariants"
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

# Private heap allocation and generational invariants

This study decomposes [Terms, private heaps, shared binaries and tracing collection](../terms-private-heaps-shared-binaries-and-tracing-collection.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Process-local collection reduces synchronization scope, but published memory-management work shows that heap organization and collector policy must be evaluated together. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Automatic tracing collection and term interpretation remain unprivileged runtime responsibilities; kernel pages do not encode BEAM object ownership.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own young/old areas, allocation tops, stack boundaries, remembered information and a generation-stamped allocator account. The mutator exclusively owns its private heap outside collector handoff. Other senders cannot allocate directly into that heap while it runs.

### Admission, transitions and completion

Check space and collector reserve before bump allocation. At a declared safe point, grow or collect through the memory service; publish new bounds only when roots and continuation state agree. Promotion either relies on a proved no-old-to-young invariant or records every violating edge, including runtime-maintained mutable containers.

### Failure and adversarial behavior

Ordinary term immutability does not prove that process dictionaries, match contexts or native wrappers never create relevant edges. Missing one barrier can silently reclaim live data. Fragmentation and reserved arenas remain charged even when live-word counters decrease.

### Alternatives and unresolved tradeoffs

Contiguous heap/stack storage simplifies collision checks but can increase copying; separate storage changes root walking and fragmentation. Promotion age and sizing heuristics are implementation choices. Measure full-collection frequency and retained pages rather than adopting upstream constants as requirements.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Force promotion while updating every mutable runtime root class.
- Exhaust the domain account with little live actor data and verify reserved pages are counted.
- Send concurrently with collection and confirm only the owner integrates incoming fragments.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Root materialization](../code-execution-safe-points-and-version-publication/canonical-safe-point-and-native-helper-state.md) — a contract this service must compose with.
- [Physical and retained accounting](../resource-accounting-and-overload-control/hierarchical-reservations-and-ledger-reconciliation.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
2. [Sagonas and Wilhelmsson: memory management](../../../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md).
