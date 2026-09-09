---
title: "Shared binary, literal and fragment lifetimes"
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

# Shared binary, literal and fragment lifetimes

This study decomposes [Terms, private heaps, shared binaries and tracing collection](../terms-private-heaps-shared-binaries-and-tracing-collection.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Explicit sharing needs stronger lifetime rules than private heaps; persistent-term engineering shows how cheap reads can shift cost into later reclamation. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/clebsch-et-al-2017-orca.md), [3](../../../30-sources/larsson-2019-persistent-term.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Automatic tracing collection and term interpretation remain unprivileged runtime responsibilities; kernel pages do not encode BEAM object ownership.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own reference/lease records for immutable large binaries, literal areas and incoming heap fragments. Physical ownership has exactly one primary charge; retained-parent telemetry may name many actors without multiplying physical totals. A tiny subbinary can keep a large allocation live.

### Admission, transitions and completion

Sending retains allowed shared objects and transfers a private fragment into ingress ownership. Receiver adoption moves—not duplicates—the fragment charge. Collection and exit release references exactly once. Literal retirement follows logical code purge and later copying/draining; no actor can mutate shared backing memory.

### Failure and adversarial behavior

Refcount wrap, double fragment adoption and abandoned sender rollback can produce leaks or use-after-free. Persistent-term replacement may require runtime-wide reader work even though ordinary actor GC is local. This does not authorize a shared mutable actor heap or permit one actor to free another's retained binary.

### Alternatives and unresolved tradeoffs

Copying small slices can reduce parent retention but costs CPU and may alter internal sharing economics. Keep the choice semantically invisible and account both copies during transition. Batched reference updates need bounded flush and actor-death handling.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Retain one byte of a large binary after sender exit and reconcile physical versus retained totals.
- Race fragment publication, alias rejection and receiver collection; observe one release owner.
- Purge code while literals remain in mailboxes and native wrappers, then verify safe later reclamation.

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
2. [Orca: collector and type-system co-design](../../../30-sources/clebsch-et-al-2017-orca.md).
3. [Clever use of persistent_term](../../../30-sources/larsson-2019-persistent-term.md).
