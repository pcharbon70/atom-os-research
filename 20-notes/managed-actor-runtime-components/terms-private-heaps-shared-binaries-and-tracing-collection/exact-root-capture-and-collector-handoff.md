---
title: "Exact root capture and collector handoff"
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

# Exact root capture and collector handoff

This study decomposes [Terms, private heaps, shared binaries and tracing collection](../terms-private-heaps-shared-binaries-and-tracing-collection.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

ERTS exposes precise process collection conventions; yieldable helper documentation highlights native stack pointers that cannot safely survive suspension. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/erlang-otp-team-2026-yielding-c-code-contracts.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Automatic tracing collection and term interpretation remain unprivileged runtime responsibilities; kernel pages do not encode BEAM object ownership.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own a root-map version and actor-local collection handshake. Root classes include live registers, stack continuations, exception state, dictionaries, receive cursors, adopted fragments, temporary BIF values and native wrapper references. The execution engine provides canonical state; the collector interprets it under the same layout schema.

### Admission, transitions and completion

Request collection, stop this actor at a qualified safe point, materialize cached state and validate root-map/code-generation agreement. Pin explicit shared references before moving objects. Resume only with the committed new root set; arbitrary kernel preemption alone is not a collector safe point.

### Failure and adversarial behavior

A missing native temporary or stale receive cursor is a live pointer even when no language variable names it. Conservative scanning may retain data and misclassify words; it cannot silently replace precise moving-GC contracts. A root-schema mismatch stops the affected execution path instead of guessing.

### Alternatives and unresolved tradeoffs

Generated root maps reduce duplicated descriptions but put generator correctness in the trusted chain. A checked interpreter provides a simpler comparison path. Independently test emitted maps against instrumented object reachability and forced yields.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Force GC at every allocating instruction and helper transition.
- Keep the sole reference in each root class and verify survival.
- Introduce a code/root-map version mismatch and ensure no collection or resume proceeds.

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
2. [Automatic Yielding of C Code](../../../30-sources/erlang-otp-team-2026-yielding-c-code-contracts.md).
