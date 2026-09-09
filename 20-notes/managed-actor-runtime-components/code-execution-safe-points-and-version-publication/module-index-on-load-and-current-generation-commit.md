---
title: "Module index, on_load and current-generation commit"
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

# Module index, on_load and current-generation commit

This study decomposes [Code execution, safe points and version publication](../code-execution-safe-points-and-version-publication.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

OTP exposes current/old module behavior while internal thread-progress indexes are a different implementation mechanism. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Language execution and code-version visibility belong to the runtime; executable-page publication consumes the lower kernel's complete W^X and instruction-fetch contract.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own inactive module indexes, export/fun bindings, pending initialization actor and serialized per-module commit. A physically executable candidate is not yet the current language-visible version. First-load waiters are bounded, charged objects.

### Admission, transitions and completion

Build a complete inactive index referencing a successfully published native image or verified interpreted image. Drain staging readers before its atomic visibility switch. With on_load, give only the fresh initializer candidate access; existing callers keep the prior current version. Exact ok permits commit; another result retires the candidate.

### Failure and adversarial behavior

Initialization may issue external effects that unloading cannot undo. First-load callers must not wait in an unbounded queue. Parallel preparations for one module need explicit conflict resolution, not last-writer-wins over independently assembled export tables.

### Alternatives and unresolved tradeoffs

Serial finishing is simpler than concurrent multi-module publication but limits load throughput. Batch publication requires a declared atomicity scope and larger retained snapshots. Internal index count does not increase the two observable module versions.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Fail on_load after an external request and preserve both prior code and uncertain effect evidence.
- Race two loaders for the same module and reject mixed export generations.
- Pause a reader of the inactive index before attempting its reuse.

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
2. [Thread Progress](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md).
