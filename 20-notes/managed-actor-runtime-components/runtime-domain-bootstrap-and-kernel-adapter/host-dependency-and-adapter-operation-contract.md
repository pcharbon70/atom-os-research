---
title: "Host dependency and adapter operation contract"
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

# Host dependency and adapter operation contract

This study decomposes [Runtime-domain bootstrap and kernel adapter](../runtime-domain-bootstrap-and-kernel-adapter.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Hosted ERTS and CleanQ expose different layers: the former needs many OS services; the latter specifies ownership transfer rather than a complete host environment. [1](../../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md), [2](../../../30-sources/haecki-et-al-2019-cleanq.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. The adapter consumes kernel authority; it does not make BEAM terms into capabilities or put the managed runtime in privileged code.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own a dependency inventory grouped by clocks, memory, threading, files, entropy, networking and dynamic code. Each entry names a semantic adapter operation, unsupported feature or isolated compatibility service. Raw selectors remain inside the adapter; an actor-visible integer or opaque term never directly indexes a kernel capability.

### Admission, transitions and completion

Operations declare acceptance, completion, cancellation and memory ownership separately. An operation record is allocated before submission and survives coalesced wakeups. A notification causes polling of authoritative state; it is not a completion receipt. Generated bindings share schema and error definitions with the runtime call descriptors.

### Failure and adversarial behavior

A successful C link or freestanding build does not implement missing POSIX semantics. Returning success from stubbed locks, clocks or mapping operations is unsafe. Unknown required imports reject the image/profile; optional unsupported functions have declared language-visible behavior. Retry only when the operation identity and its actual idempotence contract permit it.

### Alternatives and unresolved tradeoffs

Recreating a POSIX personality can reduce source-porting work but expands implementation and compatibility obligations. A native semantic adapter is narrower but requires runtime changes. Keep both as research alternatives; this decomposition does not select an upstream ERTS port.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Census imported symbols and indirect service calls against the manifest.
- Drop every wakeup while polling operation state; no completed request may remain permanently undiscoverable.
- Attempt a forged actor-side selector and confirm no authority lookup occurs.

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
2. [CleanQ](../../../30-sources/haecki-et-al-2019-cleanq.md).
