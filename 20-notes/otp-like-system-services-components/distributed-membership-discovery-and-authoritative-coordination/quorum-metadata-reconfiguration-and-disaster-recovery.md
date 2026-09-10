---
title: "Quorum metadata, reconfiguration, and disaster recovery"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Quorum metadata, reconfiguration, and disaster recovery

This study decomposes [Distributed membership, discovery, and authoritative coordination](../distributed-membership-discovery-and-authoritative-coordination.md).

Research question: Which durable assumptions preserve one authoritative control history?

## Research basis and status

Raft orders crash-fault metadata under majority and stable-storage assumptions;
cached reads may be stale. [1](../../../30-sources/ongaro-ousterhout-2014-raft.md) [2](../../../30-sources/etcd-project-2026-api-guarantees.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The coordination cell owns voter configuration, term/vote/log state, committed
metadata, snapshots and authorization for proposals. Bulk application data and
observational gossip stay outside its log. The selected profile is crash-fault
tolerant, not Byzantine merely because channels authenticate peers.

### Admission, transitions and completion

Persist required protocol state before dependent replies. Use a linearizable barrier
for reads that grant authority. Reconfigure through an explicitly proved
overlapping-quorum protocol. Install snapshots only after validating identity,
configuration, committed frontier and integrity, with bounded transfer and proposal
queues.

### Failure and adversarial behavior

Lost quorum prevents new grants; gossip cannot shrink voters to restore
availability. Total stable-state loss can reset fencing unless an independent
high-water witness or safe recovery rule prevents rollback. A valid old snapshot is
not necessarily a current authority anchor.

### Alternatives and unresolved tradeoffs

Replication adds availability and ordering at storage and operational cost.
Single-node coordination has simpler recovery but a narrower failure profile.
Algorithm choice does not select a trustworthy implementation: snapshot, client
deduplication and disk-error paths require separate qualification.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Reconfigure during leader loss and verify no disjoint configurations commit conflicting ownership.
- Restore every replica from an old snapshot; the system must reject unsafe authority resurrection or explicitly declare disaster-recovery safety unavailable.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Naming, registry, and local discovery](../naming-registry-and-local-discovery/README.md) — publishes current bindings and watch revisions.
- [Device-service policy and management](../device-service-policy-and-management/README.md) — settles hardware outcomes and buffer custody.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Raft](../../../30-sources/ongaro-ousterhout-2014-raft.md).
2. [etcd API guarantees](../../../30-sources/etcd-project-2026-api-guarantees.md).
