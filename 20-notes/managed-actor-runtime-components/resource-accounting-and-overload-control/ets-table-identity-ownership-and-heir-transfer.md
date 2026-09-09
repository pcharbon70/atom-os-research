---
title: "ETS table identity, ownership and heir transfer"
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

# ETS table identity, ownership and heir transfer

This study decomposes [Resource accounting and overload control](../resource-accounting-and-overload-control.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

ETS is explicit shared state with ownership rules; it is not a communal actor heap or an uncharged runtime utility. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/banga-et-al-1999-resource-containers.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Runtime ledgers attribute consumption beneath hard kernel domain limits; actor policy cannot mint memory, CPU or cleanup reserve.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own table identity/generation, type, access rights, current owner, configured heir and ledger account. Preserve separate no-heir, silent-heir and notifying-heir states. An actor's PID remains a generation-qualified lifetime reference.

### Admission, transitions and completion

Create privately and publish after reserving table metadata. On owner death, choose one live-heir transfer or destruction. Under the parent profile, the two-element heir option transfers silently and the three-element form sends ETS-TRANSFER. Explicit give_away sends its notification and does not rewrite the stored heir.

### Failure and adversarial behavior

Transfer cannot make both owners concurrently authoritative. A stale heir must not receive a reused table. Death notification ordering depends on completing visible table disposition, though physical node reclamation may remain deferred and charged.

### Alternatives and unresolved tradeoffs

One ownership lock makes transition linearization clear; per-table synchronization scales independent tables. Removing ownership entirely would simplify runtime cleanup only by changing compatibility and moving lifecycle obligations elsewhere.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Race owner death, heir death and give_away; obtain one compatible disposition.
- Verify silent versus notifying heir behavior and unchanged heir after give_away.
- Retain a stale table identifier across deletion/recreation and reject operations on the new generation.

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
2. [Resource containers](../../../30-sources/banga-et-al-1999-resource-containers.md).
