---
title: "Native emission, relocation and artifact validation"
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

# Native emission, relocation and artifact validation

This study decomposes [Code execution, safe points and version publication](../code-execution-safe-points-and-version-publication.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Load-time translation offers a simpler alternative to adaptive tracing; PCC cautions that code safety depends on the modeled policy and trusted checker. [1](../../../30-sources/gustavsson-2020-road-to-the-jit.md), [2](../../../30-sources/necula-1997-proof-carrying-code.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Language execution and code-version visibility belong to the runtime; executable-page publication consumes the lower kernel's complete W^X and instruction-fetch contract.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own writable nonexecutable staging pages, relocations, branch targets, code/root maps and the emitted artifact hash. The emitter gets no general kernel mapping authority. Approved runtime stubs are the only imported native call targets.

### Admission, transitions and completion

Lower verified instructions, build metadata with each template, resolve relocations and validate bounds and allowed target classes. Check all backedges and potentially long helper paths against the safe-point contract. Hand an immutable candidate manifest to page publication only after every writer is identified.

### Failure and adversarial behavior

An in-range branch can still bypass a required check; validating relocation ranges is not a semantic proof. Compiler bugs, template bugs and shared helper defects remain trusted-chain risks. Failed emission releases private staging but must not invalidate an already published module.

### Alternatives and unresolved tradeoffs

Simple per-instruction templates reduce optimizer complexity while retaining runtime metadata obligations. More aggressive optimization needs independent translation validation and measurements of compile latency, code size and diagnostic fidelity.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Corrupt relocation offsets, stub identities and root-map ranges.
- Compare emitted instructions and exception behavior with the interpreter on generated modules.
- Reject a loop whose transformed backedge bypasses its budget check.

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

1. [The Road to the JIT](../../../30-sources/gustavsson-2020-road-to-the-jit.md).
2. [Proof-carrying code](../../../30-sources/necula-1997-proof-carrying-code.md).
