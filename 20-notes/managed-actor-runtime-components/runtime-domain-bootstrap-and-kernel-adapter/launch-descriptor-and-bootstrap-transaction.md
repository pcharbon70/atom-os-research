---
title: "Launch descriptor and bootstrap transaction"
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

# Launch descriptor and bootstrap transaction

This study decomposes [Runtime-domain bootstrap and kernel adapter](../runtime-domain-bootstrap-and-kernel-adapter.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

The pinned source audit exposes a substantial hosted dependency surface; crash-only design makes restart depend on explicit external state, not a second ad hoc initializer. [1](../../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md), [2](../../../30-sources/candea-fox-2003-crash-only-software.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. The adapter consumes kernel authority; it does not make BEAM terms into capabilities or put the managed runtime in privileged code.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

An immutable launch snapshot owns descriptor version, runtime epoch, image/profile hashes, initial resource grants and route identities. A private acquisition ledger records each accepted mapping, context and endpoint. This is runtime-side defensive validation; the kernel must independently validate operations even if the runtime is malicious.

### Admission, transitions and completion

Validate bounds and overlapping ranges before dereferencing nested records. Construct allocator, collector reserve, actor registry and scheduler state privately; connect declared services before publishing the first actor. Every partial acquisition has its own release token. A bootstrap failure closes admission and drains this ledger; a published first actor changes the transaction into an ordinary runtime lifecycle.

### Failure and adversarial behavior

A revoked route during startup cannot be replaced by an ambient name lookup. Repeated launch messages must return the original transaction state, not allocate another domain. An initializer that has performed external I/O cannot claim those effects were rolled back when its local objects are released.

### Alternatives and unresolved tradeoffs

A static descriptor makes authority inspectable but limits dynamic service discovery. A richer bootstrap broker remains possible above this boundary, provided it returns explicitly authorized, incarnation-bound grants. Resolve which dependencies are mandatory before treating any image as self-contained.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Reject a descriptor with overlapping mapping ranges without consuming grants.
- Interrupt each acquisition and retry; verify one live grant or one terminal release per ledger entry.
- Fail immediately before and after first-actor publication and distinguish rollback from actor exit.

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

1. [Pinned OTP 29.0.5 source audit](../../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md).
2. [Crash-only software](../../../30-sources/candea-fox-2003-crash-only-software.md).
