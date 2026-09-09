---
title: "Admission close and domain quiescence"
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

# Admission close and domain quiescence

This study decomposes [Runtime-domain bootstrap and kernel adapter](../runtime-domain-bootstrap-and-kernel-adapter.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Crash-only recovery locates restart control outside failed state; thread-progress evidence covers participating software readers, not arbitrary domain or device quiescence. [1](../../../30-sources/candea-fox-2003-crash-only-software.md), [2](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. The adapter consumes kernel authority; it does not make BEAM terms into capabilities or put the managed runtime in privileged code.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own a monotonic admissions-closed latch, outstanding-operation set, cooperative worker-drain records and pre-registered evidence descriptors. The external supervisor owns forced freeze and domain replacement. Runtime bookkeeping is useful evidence, not authoritative proof after native memory corruption.

### Admission, transitions and completion

Close new ordinary work, request operation disposition, release actor activation ownership, and report cooperative thread progress. Seal available runtime evidence before dismantling its mappings. The external teardown path must also work when no runtime acknowledgement arrives. Publish successor routes only under a new runtime epoch after old authority has been withdrawn.

### Failure and adversarial behavior

Cancellation acknowledgements do not release in-flight I/O buffers or prove that effects stopped. A stalled unmanaged native participant may prevent local reclamation; escalation records that fact instead of advancing an epoch synthetically. Evidence failure must not deadlock the independent kernel teardown path.

### Alternatives and unresolved tradeoffs

Graceful draining preserves diagnostics and may reduce application disruption, but waiting forever defeats containment. A bounded cooperative interval followed by outer policy is preferable to a runtime-owned unlimited shutdown. Its duration and residual-device treatment remain deployment decisions.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Freeze while a worker holds a collector or code-publication continuation.
- Suppress all cooperative replies and confirm the external teardown contract remains usable.
- Deliver old-epoch completions after replacement; release old resources without routing them to new actors.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Compatibility profile](../compatibility-manifest-beam-loader-and-verifier/compatibility-profile-and-conformance-catalog.md) — a contract this service must compose with.
- [Resource adoption and reconciliation](../resource-accounting-and-overload-control/hierarchical-reservations-and-ledger-reconciliation.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [Crash-only software](../../../30-sources/candea-fox-2003-crash-only-software.md).
2. [Thread Progress](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md).
