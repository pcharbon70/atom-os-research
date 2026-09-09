---
title: "Compatibility profile and conformance catalog"
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

# Compatibility profile and conformance catalog

This study decomposes [Compatibility manifest, BEAM loader and verifier](../compatibility-manifest-beam-loader-and-verifier.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

The archive distinguishes its OTP 29.0.6 public-contract baseline from its OTP 29.0.5 source audit; internal constants are not compatibility requirements. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Compatibility is a versioned language/runtime claim. A validated container or signed module is not proof of hostile-code isolation.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own the profile hash, accepted compiler/container/instruction versions, BIF/library surface and a catalog of observable cases. Separate supported, rejected and extension behavior for timers, signals, ETS, code loading, native calls and distribution. A single BEAM version number cannot express this matrix.

### Admission, transitions and completion

Resolve all required imports and feature flags against one immutable profile before code admission. Bind test programs, reference-runtime identity, expected observations and resource policy to that hash. Differential tests compare language values and permitted histories, not allocator addresses, reduction weights or physical queue layout.

### Failure and adversarial behavior

A restricted profile must not advertise full OTP compatibility. A module that loads successfully can still depend on an absent exception, alias or BIF behavior. Moving documentation and patch releases cannot silently update a previously accepted profile. Unknown features remain explicit rejection or unresolved qualification.

### Alternatives and unresolved tradeoffs

One narrow profile reduces verification scope but excludes software; a broader profile increases shared-state and native trust obligations. Preserve a capability to grow the catalog monotonically while versioning changed behavior. No profile acceptance is asserted by writing this catalog.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Load a valid container requiring an unsupported BIF and reject before publication.
- Compile equivalent tests with each claimed compiler release and record semantic differences.
- Compare timer, purge and exit outcomes against the exact reference version, not only instruction execution.

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
2. [Pinned OTP 29.0.5 source audit](../../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md).
