---
title: "Semantic observation and view-generation publication"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - semantic-ui
  - state-synchronization
  - visual-computing
aliases: []
---

# Semantic observation and view-generation publication

This study decomposes [Durable semantic actors and disposable presentation](../durable-semantic-actors-and-disposable-presentation.md).

Research question: How can model truth publish a coherent semantic view
without making the publisher or its cached tree authoritative?

## Research basis and status

Functional reactive animation separates time-varying behavior from imperative
repaint identity. AccessKit implements frozen semantic nodes and atomic updates,
while Chromium caches accessibility state outside isolated renderers.
[1](../../../30-sources/elliott-hudak-1997-functional-reactive-animation.md)
[2](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md)
[3](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md)

Atom's observation and publication protocol is a proposal.

## Development

### Owned state and trust boundary

Model actors own domain state. A semantic publisher owns a view session,
publisher incarnation, base model frontier, semantic revision, projection
policy, and bounded subscriber cursors. Its tree is reconstructible evidence,
not the only copy of an edit or operation outcome.

### Admission, transitions, and completion

Publication begins with a complete model observation at a declared frontier,
builds a validated semantic snapshot, then atomically exposes a new view
generation. Incremental updates name their exact base and new revisions.
Subscriber overflow, publisher restart, or incompatible vocabulary causes an
explicit resnapshot instead of best-effort continuation.

### Failure and adversarial behavior

Partial multi-node updates, stale model reads, duplicate deltas, corrupt
relations, and slow consumers can create inconsistent meaning. Atomic groups
are bounded; checksums and frontier digests detect loss; publishers cannot
block model progress indefinitely; confidential projections omit structural
side channels as well as values.

### Alternatives and unresolved tradeoffs

Rebuilding every frame from model state is simple but expensive. Keeping one
mutable shared tree couples failure domains. Immutable snapshots plus checked
deltas support isolation; coalescing granularity and maximum resnapshot cost
need measurement.

## Verification obligations

- Crash during every multi-node publication and expose only the prior or next
  complete semantic revision.
- Delay, duplicate, reorder, and drop deltas; every consumer must resynchronize
  without issuing a duplicate domain command.
- Compare normalized snapshots before and after publisher replacement, allowing
  differences only for declared model progress or protocol migration.

## Connections

- [Internal-service index](README.md) — presentation state classification.
- [Atomic semantic streams](../semantics-first-accessible-ui-protocol/atomic-snapshot-delta-and-resynchronization.md) — protocol detail.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — source manifest.

## Sources

1. [Functional reactive animation](../../../30-sources/elliott-hudak-1997-functional-reactive-animation.md).
2. [AccessKit architecture](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md).
3. [Chromium UI process architecture](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md).
