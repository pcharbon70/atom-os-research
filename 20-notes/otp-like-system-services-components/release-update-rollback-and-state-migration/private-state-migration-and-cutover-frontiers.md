---
title: "Private state migration and cutover frontiers"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Private state migration and cutover frontiers

This study decomposes [Release, update, rollback, and state migration](../release-update-rollback-and-state-migration.md).

Research question: How does migration finish against a coherent state when the old generation is still changing?

## Research basis and status

Compatible schema stages and crash-aware publication support controlled migration,
but do not prove arbitrary semantic transforms. [1](../../../30-sources/rae-et-al-2013-online-schema-change-f1.md) [2](../../../30-sources/chen-et-al-2015-fscq.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The migration service owns immutable input frontier, transform digest, private
destination root, progress ledger and validation results. It receives constrained
read/write capabilities. Applications own domain meaning; storage owns commit and
replay behavior.

### Admission, transitions and completion

For offline migration, close old write admission and establish a settled frontier.
For online migration, declare the change-capture or compatible dual-write protocol
and prove the final catch-up barrier. Resume chunked work by stable input and
transform identity, then validate closure and invariants before cutover.

### Failure and adversarial behavior

Repeating a chunk after crash must not duplicate external effects. A copied root
with a missing accepted-write suffix is not complete. Outstanding operation-result
records and old-format messages need migration or retained ownership, not just data
conversion.

### Alternatives and unresolved tradeoffs

Copying into private state costs storage but preserves a clear fallback. In-place
rewriting reduces peak space while greatly complicating crash recovery and rollback.
A reversible data transform does not reverse user-visible effects or invalidated
credentials.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Crash at chunk checkpoint boundaries and verify deterministic resumed output against the same source frontier.
- Allow one old writer to lag past catch-up; cutover must block or fence it without losing an already accepted mutation.

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
2. [FSCQ](../../../30-sources/chen-et-al-2015-fscq.md).
