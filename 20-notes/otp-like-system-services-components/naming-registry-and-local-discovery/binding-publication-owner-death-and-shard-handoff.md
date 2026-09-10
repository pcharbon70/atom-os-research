---
title: "Binding publication, owner death, and shard handoff"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Binding publication, owner death, and shard handoff

This study decomposes [Naming, registry, and local discovery](../naming-registry-and-local-discovery.md).

Research question: How can replacement and owner cleanup avoid deleting a successor's binding?

## Research basis and status

Revision conditions and incarnation-sensitive handles support replacement without
treating reusable paths as object identity. [1](../../../30-sources/etcd-project-2026-api-guarantees.md) [2](../../../30-sources/burrows-2006-chubby.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The shard writer owns immutable binding tables and a monotonically ordered
publication revision within its shard generation. Reservation owners and service
actors are separate identities. The lifecycle controller supplies readiness evidence
but does not overwrite the shard directly.

### Admission, transitions and completion

Publish only against the expected old binding and revision. Conditional withdrawal
names the exact owner and binding generation. Owner-death reconciliation uses those
same conditions. A shard handoff freezes or fences the old writer, transfers
authoritative state and installs a fresh shard generation before accepting writes.

### Failure and adversarial behavior

An old monitor notification arriving after replacement cannot remove the current
binding. A lost publication reply requires operation-status reconciliation.
Persisted bindings must be revalidated against live owner generations after registry
recovery; stale checkpoints cannot resurrect dead endpoints.

### Alternatives and unresolved tradeoffs

A single local writer keeps mutation reasoning small. Sharding scales independent
namespaces but provides no cross-shard atomicity. If lifecycle requires one coherent
multi-shard graph, publish a shared immutable root above shards or explicitly
introduce a transaction protocol.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Race owner death, replacement and delayed withdrawal; exactly the intended old binding may disappear.
- Crash during shard transfer and attempt writes through both writers; at most the authorized current generation may commit.

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
2. [Chubby](../../../30-sources/burrows-2006-chubby.md).
