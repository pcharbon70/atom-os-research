---
title: "Page, context and route grant adoption"
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

# Page, context and route grant adoption

This study decomposes [Runtime-domain bootstrap and kernel adapter](../runtime-domain-bootstrap-and-kernel-adapter.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Resource containers separate charge principals from threads; scheduling contexts make CPU authority distinct from a runtime worker. [1](../../../30-sources/banga-et-al-1999-resource-containers.md), [2](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. The adapter consumes kernel authority; it does not make BEAM terms into capabilities or put the managed runtime in privileged code.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own grant generations, adoption state and the association between runtime pools and kernel accounts. Allocator arenas, worker slots and route tables are separate objects with separate capacity limits. Neither the number of processors nor a successful allocation request proves that a corresponding usable runtime object exists.

### Admission, transitions and completion

Reserve runtime metadata first, request a bounded grant batch, then adopt only resources whose returned generation and rights match. Publish an arena or worker after initialization. Specify all-or-partial batch behavior explicitly. For a worker, create its queues and progress participant before exposing it to wakeup and stealing; withdrawing it uses the scheduler's drain protocol.

### Failure and adversarial behavior

An adoption failure after the kernel granted a resource leaves a real release obligation. Keep it in the ledger until release completes. Domain memory totals include reserved and not-yet-returned pages, not merely live actor bytes. A revoked context can pause execution before a runtime safe point, so cleanup cannot presume immediate cooperative return.

### Alternatives and unresolved tradeoffs

Batching amortizes crossings but increases stranded capacity and rollback complexity. Small grants simplify reconciliation but can inflate contention. Measure grant latency, fragmentation and recovery reserve separately before choosing batch sizes.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Inject partial grant success and metadata allocation failure after acceptance.
- Revoke a worker context during initialization; it must never become a steal target prematurely.
- Reconcile every adopted and retiring page with the kernel domain total.

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

1. [Resource containers](../../../30-sources/banga-et-al-1999-resource-containers.md).
2. [Scheduling-context capabilities](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md).
