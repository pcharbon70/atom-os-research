---
title: "Designing a global name service"
kind: source
created: "2026-09-04"
authors:
  - "Butler W. Lampson"
published: 1986
citation_key: "lampson-1986-global-name-service"
container: "Proceedings of the Fifth Annual ACM Symposium on Principles of Distributed Computing"
edition: "PODC '86, pages 1–10"
isbn: "0-89791-198-9"
doi: "10.1145/10590.10591"
url: "https://doi.org/10.1145/10590.10591"
accessed: "2026-09-04"
tags:
  - distributed-systems
  - naming
  - registries
  - service-discovery
aliases:
  - "Global name service paper"
---

# Designing a global name service

## Reference

Butler W. Lampson. “[Designing a Global Name
Service](https://www.cs.princeton.edu/courses/archive/spring13/cos598C/Lampson.pdf).”
*Proceedings of the Fifth Annual ACM Symposium on Principles of Distributed
Computing (PODC '86)*, pages 1–10, 1986. DOI
[10.1145/10590.10591](https://doi.org/10.1145/10590.10591).

## Research question or contribution

The paper designs a name service intended to survive worldwide scale, long
life, administrative change, partial failure, and the absence of one globally
trusted component. It treats lookup behavior under faults as part of the
interface specification and separates the client's stable naming view from
the administrative machinery of replicas, copies, placement, and update.

## Method

This is an architecture and semi-formal interface design derived from
Grapevine and Xerox Clearinghouse experience. It defines client and
administrative abstractions, name-space restructuring, replication, caching,
and authentication relationships, then sketches implementations. The paper
states that only a toy implementation existed, so it supplies unusually clear
semantics and design rationale but not a production evaluation of the proposed
whole.

## Findings

- The service maps hierarchical names to labeled values, but a directory also
  has a durable identifier independent of the path currently used to reach it.
  Links allow paths to retain meaning while the hierarchy is reorganized.
- Hierarchy is used not only for presentation but to distribute
  administration, accommodate growth, and contain failures or mistrust. The
  client abstraction hides copies and replica synchronization; the
  administrative interface makes them explicit.
- Precise nondeterministic behavior is preferable to pretending every lookup
  is fresh. Clients may obtain one of a constrained set of answers when
  replicas lag or fail, and the specification must say what staleness means.
- Lookup results may be cached until the earliest expiration encountered while
  traversing names and links. The design pays for scalable caching by delaying
  some changes or tolerating bounded inaccuracy instead of tracking every
  client for invalidation.
- Stable identity and human-meaningful path are separate. That distinction is
  important during rename, delegation, replica movement, and recovery.
- Naming contributes to resource location and authentication, but the service
  still has explicit protection and administrative mechanisms. A returned
  value is not automatically authority to use the named resource.

## Relevance

Atom OS should give a service a stable identifier and incarnation while
allowing one or more names to resolve to generation-bound candidates. The
local registry can therefore expose an atomic `snapshot + revision` read and a
watch starting strictly after that revision. A cache entry carries the
registry revision and expiry or invalidation cursor that justifies it; a caller
must never infer freshness merely because the name string is unchanged.

The paper also supports sharding registries by administrative or failure
scope. Atom OS can keep the common boot-local registry small and linearizable,
then layer eventual groups or federated discovery over it. Reorganization is a
new binding revision, not silent reuse of an old actor handle. Capability
derivation remains separate: resolution returns an attenuated handle only
through an authorized resolver path, or returns public descriptive metadata
that carries no invocation right.

## Limits

The proposed global service was not fully implemented or measured, and its
authentication examples and threat model predate modern cryptography and
capability-oriented operating systems. Expiration-based caching assumes useful
time bounds and can trade update latency for lookup availability. The design
does not supply a local lock-free registry algorithm, watcher backpressure,
actor-incarnation semantics, Byzantine replication, or exclusive-effect
fencing. Those remain Atom OS responsibilities.

## Derived work

- [Naming, registry, and local discovery](../20-notes/otp-like-system-services-components/naming-registry-and-local-discovery.md)
- [Distributed membership, discovery, and authoritative coordination](../20-notes/otp-like-system-services-components/distributed-membership-discovery-and-authoritative-coordination.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
