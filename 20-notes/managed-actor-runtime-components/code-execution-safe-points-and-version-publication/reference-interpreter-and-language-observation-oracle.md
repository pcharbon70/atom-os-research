---
title: "Reference interpreter and language-observation oracle"
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

# Reference interpreter and language-observation oracle

This study decomposes [Code execution, safe points and version publication](../code-execution-safe-points-and-version-publication.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

BeamAsm history shows why whole-runtime semantics constrain execution optimization; public compatibility is broader than removing dispatch overhead. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/gustavsson-2020-road-to-the-jit.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Language execution and code-version visibility belong to the runtime; executable-page publication consumes the lower kernel's complete W^X and instruction-fetch contract.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own a checked execution path over immutable validated instructions, including calls, tail calls, exceptions and BIF dispatch. It is a semantic comparison engine, not a privileged kernel loop and not a claim that interpreting alone isolates hostile bytecode.

### Admission, transitions and completion

Execute with explicit canonical registers, stack and reductions. Record language-visible observations at selected boundaries and compare optimized engines under the same profile and controlled schedule. Preserve the interpreter as a long-lived diagnostic oracle when native execution is introduced.

### Failure and adversarial behavior

A reference implementation can contain the same bug as a generated engine if both share unchecked helper logic. Differential agreement alone is insufficient; use independent expected outcomes for semantic edge cases. Unsupported instruction or helper behavior fails explicitly instead of falling through to a host operation.

### Alternatives and unresolved tradeoffs

One engine minimizes maintenance but loses a powerful independent comparison path. Two engines cost more testing and may share trusted services; document that shared fault set. Do not predict JIT benefit from sequential benchmarks alone.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Compare exception values, tail-call behavior and selective receives under identical schedules.
- Introduce a deliberately wrong optimized instruction to validate the differential harness.
- Run modules dominated by messaging and tables as well as arithmetic.

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

1. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
2. [The Road to the JIT](../../../30-sources/gustavsson-2020-road-to-the-jit.md).
