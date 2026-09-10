---
title: "Release compatibility graph and transition admission"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Release compatibility graph and transition admission

This study decomposes [Release, update, rollback, and state migration](../release-update-rollback-and-state-migration.md).

Research question: Can old and new code, schemas, protocols and permissions safely coexist during rollout?

## Research basis and status

F1 constructs compatible intermediate schema states; immutable release selection
does not establish live compatibility. [1](../../../30-sources/rae-et-al-2013-online-schema-change-f1.md) [2](../../../30-sources/dolstra-et-al-2008-nixos.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The planner owns directed compatibility relations for readers, writers, queued
messages, credentials, runtime profile and peers. It records rollback conditions and
resource requirements for both generations. Layer 5 supplies semantic transforms and
domain invariants.

### Admission, transitions and completion

Validate every intermediate state, not only the source and destination releases.
Bind migration artifacts and compatibility checks to immutable digests. Reserve
shadow state, retained outcomes, old-generation drain and recovery capacity. Reject
a rollout if no safe transition or supported roll-forward route exists.

### Failure and adversarial behavior

Wire-decodable data may still have changed meaning. Older writers can corrupt newly
backfilled state, and policy rollback may restore forbidden authority. A prior
binary's availability on disk does not mean it can safely read the currently active
state.

### Alternatives and unresolved tradeoffs

Expand/contract reduces downtime but lengthens the mixed-version window. Offline
quiescent migration simplifies concurrency at availability cost. General in-place
hot update expands the state space further; retain a separate OTP conformance
profile rather than claiming native equivalence.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Generate mixed old/new readers and writers through each proposed stage and check semantic invariants.
- Remove the only backward-compatible schema edge; admission must disable automatic rollback rather than advertise it from retained binaries.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration/README.md) — coordinates readiness, publication and drain.
- [Durable state, transactions, and outcome recovery](../durable-state-transactions-and-outcome-recovery/README.md) — retains committed state and retry-result responsibility.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Online schema change in F1](../../../30-sources/rae-et-al-2013-online-schema-change-f1.md).
2. [NixOS](../../../30-sources/dolstra-et-al-2008-nixos.md).
