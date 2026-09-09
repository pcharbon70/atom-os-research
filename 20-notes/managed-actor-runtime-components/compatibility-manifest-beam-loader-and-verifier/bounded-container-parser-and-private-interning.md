---
title: "Bounded container parser and private interning"
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

# Bounded container parser and private interning

This study decomposes [Compatibility manifest, BEAM loader and verifier](../compatibility-manifest-beam-loader-and-verifier.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Public BEAM compatibility and proof-carrying-code research distinguish parsing from the stronger policy that accepted code must satisfy. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/necula-1997-proof-carrying-code.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Compatibility is a versioned language/runtime claim. A validated container or signed module is not proof of hostile-code isolation.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own an immutable byte snapshot, checked chunk directory, bounded decode arena and provisional atom/import tables. Counts, decompressed bytes and parser work are charged to the load transaction. Permanent atom storage is not scratch space for rejected input.

### Admission, transitions and completion

Validate container lengths, alignment, duplicates and required chunks with checked arithmetic. Decode into index-based private structures; treat unused debug chunks as bounded opaque data. Check the complete image and reserve permanent metadata before committing new atoms and handing an immutable intermediate image to verification.

### Failure and adversarial behavior

An input producer mutating mapped bytes after validation is a TOCTOU attack; snapshot or revoke writers first. Compressed bombs, deep nesting and atom floods must fail within declared resource bounds. Rejection releases temporary data without leaving a growing global atom table.

### Alternatives and unresolved tradeoffs

Streaming can lower peak memory but complicates cross-chunk validation and rollback. A whole-image private arena costs more upfront and is easier to audit. Select limits from supported compiler outputs plus adversarial cases, not a convenient parser implementation.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Fuzz length overflow, duplicate chunks and decompression expansion.
- Repeat rejected unique-atom modules and verify permanent atom count stays unchanged.
- Mutate source bytes during loading; accepted image hashes and decoded instructions must remain consistent.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Execution and root contract](../code-execution-safe-points-and-version-publication/canonical-safe-point-and-native-helper-state.md) — a contract this service must compose with.
- [Load-transaction accounting](../resource-accounting-and-overload-control/hierarchical-reservations-and-ledger-reconciliation.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
2. [Proof-carrying code](../../../30-sources/necula-1997-proof-carrying-code.md).
