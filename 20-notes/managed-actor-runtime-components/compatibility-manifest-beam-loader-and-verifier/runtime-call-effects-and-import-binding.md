---
title: "Runtime-call effects and import binding"
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

# Runtime-call effects and import binding

This study decomposes [Compatibility manifest, BEAM loader and verifier](../compatibility-manifest-beam-loader-and-verifier.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Yielding C documentation demonstrates that helper calls need saved state and destruction paths; PCC explains why an unchecked helper lies outside a safety proof. [1](../../../30-sources/erlang-otp-team-2026-yielding-c-code-contracts.md), [2](../../../30-sources/necula-1997-proof-carrying-code.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Compatibility is a versioned language/runtime claim. A validated container or signed module is not proof of hostile-code isolation.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own generated call descriptors naming module/function/arity, allocation and GC effects, yielding/blocking class, required authority, exceptions and work accounting. These descriptors link the loader's imports to the execution engine's actual entry stubs. They are not independently maintained prose annotations.

### Admission, transitions and completion

Generate verifier effects, interpreter dispatch and native wrappers from one reviewed declaration set. Before publishing a binding, check signature, profile and helper identity. A may-yield helper returns a rooted continuation with a terminal destructor; a may-allocate helper enters through the canonical safe-point protocol.

### Failure and adversarial behavior

A helper falsely labeled nonallocating can invalidate roots; one falsely labeled bounded can monopolize a worker. Native C ABI compatibility establishes neither property. An unresolved helper or unexpected blocking dependency rejects the image rather than installing a permissive stub.

### Alternatives and unresolved tradeoffs

Conservative effects can add root materialization and scheduler overhead but reduce unsound special cases. More precise descriptors need evidence from the implementation and compiler output. Automatic C coroutine transformation is comparative evidence, not an assumed Zig facility or selected runtime language.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Inject allocation into a supposedly nonallocating helper under forced GC.
- Yield at every permitted helper boundary and kill the actor before resumption.
- Cross-check generated import tables, verifier effects and native symbols for exact agreement.

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

1. [Automatic Yielding of C Code](../../../30-sources/erlang-otp-team-2026-yielding-c-code-contracts.md).
2. [Proof-carrying code](../../../30-sources/necula-1997-proof-carrying-code.md).
