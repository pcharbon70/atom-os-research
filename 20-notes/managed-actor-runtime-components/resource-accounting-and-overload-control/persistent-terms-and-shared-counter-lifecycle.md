---
title: "Persistent terms and shared counter lifecycle"
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

# Persistent terms and shared counter lifecycle

This study decomposes [Resource accounting and overload control](../resource-accounting-and-overload-control.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

The two first-party articles expose a common tradeoff: inexpensive shared reads or updates can defer substantial work to replacement or observation. [1](../../../30-sources/larsson-2019-persistent-term.md), [2](../../../30-sources/winblad-2021-decentralized-ets-counters.md), [3](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Runtime ledgers attribute consumption beneath hard kernel domain limits; actor policy cannot mint memory, CPU or cleanup reserve.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own global immutable term bindings, counter-array generations and pending reader-drain/reclamation work. These resources are node/runtime-global, not owned solely by the last actor that accessed them. Their presence must be explicit in the compatibility manifest.

### Admission, transitions and completion

Publish a complete new binding or counter representation while retaining prior reader-visible storage. Reclaim only after the appropriate progress protocol and any term-copy work finish. For counters, preserve accumulated values across snapshot/representation replacement; separate approximate telemetry from admission authority.

### Failure and adversarial behavior

Replacing a persistent term can create cross-runtime collector work despite process-local ordinary GC. Repeated replacement can accumulate generations and starve reclamation. A stalled native reader cannot be wished away by a software epoch increment. Full replacement and observation work remains charged.

### Alternatives and unresolved tradeoffs

ETS copy-in/out offers different update/read costs; persistent terms suit stable read-mostly data rather than arbitrary frequently mutated configuration. Shared counters can use centralized or striped representation according to observation frequency. Keep the choice measurable and reversible under a safe transition.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Repeatedly replace a large persistent term while actors retain old references.
- Take counter snapshots during concurrent updates and representation changes; lose or duplicate no increments.
- Stall a progress participant and enforce a bounded pending-generation admission policy.

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

1. [Clever use of persistent_term](../../../30-sources/larsson-2019-persistent-term.md).
2. [Decentralized ETS counters](../../../30-sources/winblad-2021-decentralized-ets-counters.md).
3. [Thread Progress](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md).
