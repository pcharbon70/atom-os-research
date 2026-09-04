---
title: "The Chubby lock service for loosely-coupled distributed systems"
kind: source
created: "2026-09-03"
authors:
  - "Mike Burrows"
published: 2006
citation_key: "burrows-2006-chubby"
container: "7th USENIX Symposium on Operating Systems Design and Implementation"
edition: "OSDI '06, 335–350"
isbn: null
doi: null
url: "https://research.google.com/archive/chubby-osdi06.pdf"
accessed: "2026-09-03"
tags:
  - coordination
  - distributed-systems
  - leases
  - naming
aliases:
  - "Chubby"
---

# The Chubby lock service for loosely-coupled distributed systems

## Reference

Mike Burrows. “[The Chubby Lock Service for Loosely-Coupled Distributed
Systems](https://research.google.com/archive/chubby-osdi06.pdf).” *OSDI '06*,
pages 335–350. [USENIX record](https://www.usenix.org/conference/osdi-06/presentation/chubby-lock-service-loosely-coupled-distributed-systems).

## Research question or contribution

What semantics and engineering mechanisms make a replicated, coarse-grained
lock and small-metadata service useful to many loosely coupled client systems?

## Method

The paper reports the design, deployment, workload, failure handling, and
operational lessons of production Chubby cells. It compares intended use with
actual use by tens of thousands of clients and documents choices around Paxos
replication, sessions, leases, caching, notifications, names, ACLs, and load
adaptation.

## Findings

- A small reliable coordination service can centralize coarse-grained leader
  election, rendezvous, configuration pointers, and low-volume metadata while
  leaving high-volume application data elsewhere.
- Lock possession alone cannot protect an external resource after delay or
  partition. Chubby sequencers carry a lock generation, and the resource must
  reject stale generations; this is a fencing protocol.
- Session leases have an explicit jeopardy interval. During uncertainty the
  client invalidates caches and quiesces operations rather than pretending the
  session is certainly valid or expired.
- Handles identify a particular object instance, not only a reusable path, and
  generation numbers expose content, lock, and ACL changes.
- Consistent client caching and change notifications allowed read-heavy naming
  traffic to scale, while the implementation retained a deliberately
  low-volume write and lock-acquisition role.
- Actual uses expanded beyond locking to naming, configuration, access-control
  data, and service discovery, which increased the operational importance of
  the service.

## Relevance

The Atom OS service layer should use generation-fenced leases for leader or
device ownership, versioned watches with resynchronization, and separate
high-volume data paths. A consensus-backed metadata service can anchor a small
distributed namespace, but applications should not confuse a name or a lock
with authority: protected resources must validate the relevant capability and
fencing generation.

## Limits

Chubby reflects Google's 2006 datacenter environment and crash-fault model. It
is not a general database, secret manager, high-rate lock server, Byzantine
protocol, or proof that one shared global namespace is desirable. Its paper
describes an engineered service rather than publishing every consensus or
storage implementation detail.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [2026-09-03 OTP-like system-services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
