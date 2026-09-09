---
title: "Sealed pages and executable-publication handoff"
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

# Sealed pages and executable-publication handoff

This study decomposes [Code execution, safe points and version publication](../code-execution-safe-points-and-version-publication.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Runtime index progress and native-page publication address different observers; a software grace period does not prove instruction-fetch coherence. [1](../../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md), [2](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Language execution and code-version visibility belong to the runtime; executable-page publication consumes the lower kernel's complete W^X and instruction-fetch contract.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own the candidate image's writer inventory, immutable page manifest and lower publication operation token. The kernel/facade owns mapping authority, affected execution contexts and architecture-specific remote completion. The runtime cannot substitute an atomic function-pointer store for that contract.

### Admission, transitions and completion

Close and drain every writer; establish data visibility and seal pages nonwritable before requesting executable publication. The lower operation holds affected execution as required, installs RX, completes instruction-fetch synchronization for its full target set and reports terminal publication. Only then may runtime indexes expose entry points.

### Failure and adversarial behavior

A hidden writable alias defeats W^X even when the visible mapping is RX. A timeout awaiting remote completion is not success. If publication fails after partial lower mutation, retain the operation token and storage until the lower teardown protocol proves safe disposition.

### Alternatives and unresolved tradeoffs

Persistent dual RW/RX aliases may be a hosted implementation technique but are excluded by this proposed baseline. Immutable new generations simplify audit at a peak-memory cost. Architecture details stay below this service, with exact completion evidence above.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Retain an unauthorized writer alias and require publication refusal.
- Delay one target's instruction-fetch acknowledgement; no actor may call the candidate.
- Fail lower publication mid-transition and verify pages are neither leaked nor prematurely recycled.

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

1. [Pinned OTP 29.0.5 source audit](../../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md).
2. [Thread Progress](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md).
