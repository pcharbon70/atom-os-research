---
title: "Control-flow, root and operand verifier"
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

# Control-flow, root and operand verifier

This study decomposes [Compatibility manifest, BEAM loader and verifier](../compatibility-manifest-beam-loader-and-verifier.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

PCC makes assurance conditional on an explicit policy; the source audit shows that BEAM loading and runtime execution jointly enforce conventions. [1](../../../30-sources/necula-1997-proof-carrying-code.md), [2](../../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Compatibility is a versioned language/runtime claim. A validated container or signed module is not proof of hostile-code isolation.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own a verification worklist and abstract state for initialized X/Y slots, stack depth, catch/try regions, valid branch targets and live roots. Every opcode has a declared transfer function. This is a proposed verifier, not a claim that ordinary upstream BEAM is a malicious-module sandbox.

### Admission, transitions and completion

Check structural operands, propagate states through control-flow joins and reject inconsistent stacks or uninitialized live terms. Require valid root descriptions at allocation and call boundaries. Bound worklist steps and abstract-state size; emit an immutable verified image tied to byte and profile hashes, never unchecked host pointers.

### Failure and adversarial behavior

Missing instruction semantics or a false BIF effect declaration breaks the argument even if dataflow converges. A signed module can still be malformed. Sound rejection is preferable to accepting an unknown transfer function; verifier resource exhaustion is a load failure, not permission to skip checks.

### Alternatives and unresolved tradeoffs

A structural trusted-compiler profile is cheaper than a hostile-input verifier but must advertise the larger trust assumption. Future certificates could reduce repeated checking only after a machine model, policy and checker are independently validated.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Generate inconsistent join stacks and references to dead X registers at GC points.
- Mutate one opcode descriptor and confirm differential or verifier self-tests detect the mismatch.
- Force worklist exhaustion and verify no partially verified image becomes callable.

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

1. [Proof-carrying code](../../../30-sources/necula-1997-proof-carrying-code.md).
2. [Pinned OTP 29.0.5 source audit](../../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md).
