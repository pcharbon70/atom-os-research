---
title: "etcd API guarantees"
kind: source
created: "2026-09-04"
authors:
  - "etcd project"
published: null
citation_key: "etcd-project-2026-api-guarantees"
container: "etcd documentation"
edition: "v3.5 API guarantees page"
isbn: null
doi: null
url: "https://etcd.io/docs/v3.5/learning/api_guarantees/"
accessed: "2026-09-04"
tags:
  - consistency
  - discovery
  - distributed-systems
  - registries
  - watches
aliases:
  - "etcd watch and revision guarantees"
---

# etcd API guarantees

## Reference

etcd project. “[etcd API
guarantees](https://etcd.io/docs/v3.5/learning/api_guarantees/).” Version 3.5
documentation, accessed 2026-09-04.

## Research question or contribution

This official contract describes the ordering, consistency, durability, and
watch properties a replicated key-value API exposes. It is useful here because
local and distributed service discovery need precise meanings for revision,
snapshot, watch, compaction, and acknowledgement rather than an informal
promise that clients will “eventually hear about changes.”

## Method

The API-guarantees page was read as a public behavioral contract and checked
against the linked API concepts. No etcd cluster, fault injection, client
library, implementation audit, or benchmark was performed. The note therefore
records documented guarantees, not independently reproduced results.

## Findings

- Completed operations are linearizable by default, while serializable reads
  deliberately trade recency for availability and latency. A caller must
  choose which result it needs rather than treat every successful read as
  current authority.
- A store-wide revision orders committed changes. Transaction conditions and
  mutations share one revision, which lets a client bind a publication to the
  version it actually validated.
- A watch can begin after a selected revision and preserves event ordering for
  the watched history. That makes the cursor part of correctness, not merely a
  delivery optimization.
- Historical revisions are finite. Compaction can make an old cursor unusable,
  requiring the client to obtain a new snapshot and restart from a new
  revision. A bounded consumer must therefore expose resynchronization rather
  than promise an infinite lossless queue.
- An acknowledgement by the replicated service has stated persistence and
  visibility semantics, but those guarantees do not make a consumer's cached
  copy current after disconnection and do not authorize use of the value.

## Relevance

Atom OS local discovery should use one shard writer, a monotonic shard
revision, compare-and-publish, and a combined snapshot/cursor operation. A
watch is a bounded change stream. If its queue overflows, its cursor is too old,
or the consumer reconnects without continuity proof, the only correct recovery
is a fresh atomic snapshot plus a watch from the returned revision.

The consistency distinction also belongs in the type system. A cached or
serializable candidate can locate a possible endpoint; a linearizable binding
or still-valid lease is required when the lookup participates in exclusive
authority. In either case the returned name remains separate from the
capability needed to invoke the service.

## Limits

The documentation describes a particular replicated database and relies on
its Raft, storage, transport, authentication, and deployment assumptions. The
Atom OS local registry does not need to embed etcd, and a single-node shard can
provide a much smaller contract. The page does not establish resource bounds,
capability safety, workload identity, or application-level exactly-once
effects. Version 3.5 is retained because this is the stable, explicitly scoped
guarantee page read during the session; it should be repinned if those
guarantees change.

## Derived work

- [Naming, registry, and local discovery](../20-notes/otp-like-system-services-components/naming-registry-and-local-discovery.md)
- [Distributed membership, discovery, and authoritative coordination](../20-notes/otp-like-system-services-components/distributed-membership-discovery-and-authoritative-coordination.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
