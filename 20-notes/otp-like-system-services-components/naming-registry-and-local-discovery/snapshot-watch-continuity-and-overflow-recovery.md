---
title: "Snapshot/watch continuity and overflow recovery"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Snapshot/watch continuity and overflow recovery

This study decomposes [Naming, registry, and local discovery](../naming-registry-and-local-discovery.md).

Research question: How can bounded subscribers reconstruct state without silently missing changes?

## Research basis and status

etcd orders watch revisions within retained history, while delivery delay is
unbounded and compaction limits replay. [1](../../../30-sources/etcd-project-2026-api-guarantees.md) [2](../../../30-sources/welsh-et-al-2001-seda.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The watch service owns selector scope, authorized projection, snapshot revision,
next cursor, queue capacity and a separately readable continuity state. Watchers do
not own indefinite history retention; the registry owns compaction and resnapshot
admission.

### Admission, transitions and completion

Acquire a consistent snapshot at revision r and retain or establish watch continuity
from r+1 without a race. Deliver complete revisions according to the selected
profile. Advance the cursor only after the consumer's declared receipt boundary,
distinguishing transport receipt from actual cache application.

### Failure and adversarial behavior

When history is compacted or the queue overflows, close continuity and expose
ResnapshotRequired through status independent of the full queue. Never rely on a
final overflow message fitting into that queue. Reconnect across a shard generation
also requires explicit continuity proof.

### Alternatives and unresolved tradeoffs

Lossless durable replay costs storage and acknowledgement tracking; latest-state
consumers can instead resnapshot. Neither choice makes the cached binding current at
later invocation. Rate-limit resnapshot storms without pretending delayed consumers
have coherent state.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Mutate immediately between snapshot creation and watch installation; reconstruction must contain the change or explicitly require resnapshot.
- Fill the queue completely, trigger overflow and ensure status still reports lost continuity without enqueueing another event.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration/README.md) — coordinates readiness, publication and drain.
- [Distributed membership, discovery, and authoritative coordination](../distributed-membership-discovery-and-authoritative-coordination/README.md) — separates candidate discovery from authoritative ownership.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [etcd API guarantees](../../../30-sources/etcd-project-2026-api-guarantees.md).
2. [SEDA](../../../30-sources/welsh-et-al-2001-seda.md).
