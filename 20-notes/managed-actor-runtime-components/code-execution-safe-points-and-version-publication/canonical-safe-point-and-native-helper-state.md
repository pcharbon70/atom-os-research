---
title: "Canonical safe-point and native helper state"
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

# Canonical safe-point and native helper state

This study decomposes [Code execution, safe points and version publication](../code-execution-safe-points-and-version-publication.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

The source audit couples execution to GC and scheduling; yielding helpers expose why native local state cannot be left implicit across suspension. [1](../../../30-sources/erlang-otp-team-2026-yielding-c-code-contracts.md), [2](../../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Language execution and code-version visibility belong to the runtime; executable-page publication consumes the lower kernel's complete W^X and instruction-fetch contract.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own the canonical activation schema: code generation, continuation, live registers, stack roots, heap bounds, exception state, reductions and receive cursor. Code generators may cache state temporarily but must obey the schema at every allocating, yielding or inspecting boundary.

### Admission, transitions and completion

Materialize cached values and publish root metadata before entering a collector, scheduler, trace inspection or resumable helper. A native transition declares its return and unwind convention. Resume checks the continuation generation and reconstructs machine state from the authoritative managed representation.

### Failure and adversarial behavior

A stack pointer retained in a yielded helper may refer to a different stack on resumption. Untracked roots can be lost even if native execution returns normally. Kernel preemption preserves architecture state but does not automatically make arbitrary runtime internals safe for GC or inspection.

### Alternatives and unresolved tradeoffs

More frequent safe points simplify latency and recovery at a cost in code size and spills. Sparse safe points need validated bounds on every path between them, including exceptional and helper paths. Generated metadata must be checked against emitted code.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Force collection and inspection at every safe-point class.
- Yield and resume on another worker with temporary values kept only in native registers.
- Check exceptional unwinding through old code and nested helper continuations.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Verified instruction and root obligations](../compatibility-manifest-beam-loader-and-verifier/control-flow-root-and-operand-verifier.md) — a contract this service must compose with.
- [Retained literal ownership](../terms-private-heaps-shared-binaries-and-tracing-collection/shared-binary-literal-and-fragment-lifetimes.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [Automatic Yielding of C Code](../../../30-sources/erlang-otp-team-2026-yielding-c-code-contracts.md).
2. [Pinned OTP 29.0.5 source audit](../../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md).
