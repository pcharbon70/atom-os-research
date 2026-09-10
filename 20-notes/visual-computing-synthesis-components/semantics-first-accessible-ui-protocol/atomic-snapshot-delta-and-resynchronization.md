---
title: "Atomic snapshot, delta, and resynchronization"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - accessibility
  - state-synchronization
  - semantic-ui
aliases: []
---

# Atomic snapshot, delta, and resynchronization

This study decomposes [Semantics-first accessible UI protocol](../semantics-first-accessible-ui-protocol.md).

Research question: How can every consumer detect loss, duplication,
reordering, stale bases, and incomplete semantic updates?

## Research basis and status

AccessKit implements atomic serializable tree updates and retained consumer
trees. Incremental-computation theory shows that a change is meaningful only
relative to an exact base. Chromium's cross-process accessibility cache
demonstrates a production retained projection.
[1](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md)
[2](../../../30-sources/cai-et-al-2014-theory-of-changes.md)
[3](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md)

No Atom wire format or interoperability test exists.

## Development

### Owned state and trust boundary

Each publisher owns stream ID, incarnation, current semantic revision, model
frontier digest, and bounded update history. Consumers own last accepted
revision and a validated materialized projection. Neither side assumes a
transport is exactly once or ordered without protocol evidence.

### Admission, transitions, and completion

Subscription atomically returns a complete bounded snapshot and the cursor for
subsequent changes. Every delta names base/new revisions, atomic group,
frontier digests, completeness, and checksum. A gap, duplicate with different
content, unknown base, overflow marker, or incarnation change forces a fresh
snapshot.

### Failure and adversarial behavior

Cycles, dangling relations, deletion-order errors, oversized atomic groups,
checksum collisions, and slow consumers threaten correctness or capacity.
Canonical encoding, structural validation, quotas, bounded history, and
explicit resnapshot make failure visible. Snapshot construction cannot hold
unbounded model locks.

### Alternatives and unresolved tradeoffs

Full snapshots simplify continuity but scale poorly for large virtual views.
Unversioned event streams are efficient but cannot prove current state.
Revisioned snapshots plus bounded deltas are preferred; canonical digest,
chunking, and transactional snapshot-frontier acquisition remain open.

## Verification obligations

- Drop, duplicate, corrupt, reorder, and splice deltas across publisher
  incarnations; no consumer may silently accept a false tree.
- Crash publisher and adapter at each atomic-group boundary and observe only a
  complete prior or next revision.
- Benchmark maximum admitted graphs, churn, slow consumers, history compaction,
  and resnapshot latency under fixed memory.

## Connections

- [Internal-service index](README.md) — semantic protocol decomposition.
- [View publication](../durable-semantic-actors-and-disposable-presentation/semantic-observation-and-view-generation-publication.md) — upstream model frontier.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — provenance.

## Sources

1. [AccessKit architecture](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md).
2. [A theory of changes](../../../30-sources/cai-et-al-2014-theory-of-changes.md).
3. [Chromium UI process architecture](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md).
