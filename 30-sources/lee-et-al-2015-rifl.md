---
title: "Implementing linearizability at large scale and low latency"
kind: source
created: "2026-09-03"
authors:
  - "Collin Lee"
  - "Seo Jin Park"
  - "Ankita Kejriwal"
  - "Satoshi Matsushita"
  - "John Ousterhout"
published: "2015-10-04"
citation_key: "lee-et-al-2015-rifl"
container: "Proceedings of the 25th ACM Symposium on Operating Systems Principles"
edition: "SOSP '15, 71–86"
isbn: "978-1-4503-3834-9"
doi: "10.1145/2815400.2815416"
url: "https://doi.org/10.1145/2815400.2815416"
accessed: "2026-09-03"
tags:
  - distributed-systems
  - linearizability
  - remote-procedure-call
  - retry-semantics
aliases:
  - "RIFL"
  - "Reusable Infrastructure for Linearizability"
---

# Implementing linearizability at large scale and low latency

## Reference

Collin Lee, Seo Jin Park, Ankita Kejriwal, Satoshi Matsushita, and John
Ousterhout. “[Implementing Linearizability at Large Scale and Low
Latency](https://doi.org/10.1145/2815400.2815416).” *Proceedings of the 25th
ACM Symposium on Operating Systems Principles (SOSP '15)*, pages 71–86, 2015.
The authors' [open paper](https://web.stanford.edu/~ouster/cgi-bin/papers/rifl.pdf)
was read.

## Research question or contribution

Can reusable infrastructure turn an automatically retried, at-least-once RPC
mechanism into a linearizable operation without adding prohibitive latency or
losing its duplicate-suppression state when objects move after reconfiguration?

The proposed RIFL mechanism addresses four connected problems: globally unique
RPC identification, durable completion records, rendezvous between a retry and
the relevant record after migration, and bounded reclamation of those records.

## Method

The paper specifies three cooperating modules. A client-side `RequestTracker`
allocates sequence numbers and tracks acknowledgements; a `LeaseManager` gives
each client a leased identifier and checks whether that identifier remains
valid; and a server-side `ResultTracker` distinguishes new, completed,
in-progress, and stale requests. The design associates every completion record
with an unambiguously chosen object so the record follows that object through
migration and crash recovery.

The authors implemented the mechanism in RAMCloud. They used it to make writes,
conditional writes, and atomic increments linearizable and to construct a
multi-object transaction mechanism. Evaluation combined operation
microbenchmarks and TPC-C comparisons on Linux servers connected by a
kernel-bypass InfiniBand fabric. This is implementation and performance
evidence for that system, not a formal proof of the whole design.

## Findings

- Automatic retry and idempotent-looking mutations are not sufficient for
  linearizability. If a server performs an operation and fails before its reply
  is observed, an unrecognized retry can execute again and produce a history
  inconsistent with one instantaneous execution.
- RIFL identifies a logical RPC with a 64-bit leased client identifier and a
  64-bit client sequence number. A retry must retain the same identifier.
- The server durably records both completion and returned result atomically
  with the operation's mutations and with comparable durability. A recognized
  retry returns that saved result instead of re-executing the mutation.
- Duplicate suppression must survive placement changes. RIFL stores a
  completion record with a distinguished underlying object and requires the
  record to migrate with that object before retries are routed to its new
  owner.
- Client acknowledgements advance a `firstIncomplete` sequence number, allowing
  older result state to be reclaimed. The implementation bounds the number of
  non-reclaimable RPCs per client, making concurrency and retained server state
  an explicit trade-off.
- Leases make reclamation after client loss detectable rather than silently
  unsafe. Servers reject requests whose client lease has expired; a late client
  can therefore receive a stale or ambiguous outcome instead of reusing an
  identifier whose completion record may have been deleted. Lease expiration
  is confirmed with a centralized lease service backed by stable metadata and
  a durable cluster clock.
- In the reported RAMCloud configuration, RIFL added 530 ns to a 13.5 µs
  durable write, less than four percent. Simple distributed transactions
  committed in about 20 µs. These measurements establish feasibility for the
  tested RAMCloud implementation and hardware, not a general latency bound.
- The paper's exactly-once claim is deliberately scoped. It assumes a reliable
  client, automatic RPC retry, and reliably stored server metadata. A client
  that crashes and loses its request state can still leave the operation's
  outcome unknown, and the ultimate human caller may need an application-level
  way to observe whether an effect occurred.

## Relevance

RIFL supplies a useful boundary for the OTP-like services layer. Ordinary actor
delivery should not be relabeled exactly once merely because a gateway retries
or suppresses duplicates. A stronger durable-call profile is defensible only
when the service can preserve one request identifier across retries and
reconfiguration, commit the effect and result record atomically, route retries
to that record, retain it until acknowledgement or safe lease expiry, and
return an explicit stale or indeterminate outcome when those conditions fail.

This profile is most plausible for narrow authoritative mutations such as
registry updates, release decisions, and durable orchestration records. It does
not make arbitrary external device, network, or human-visible effects exactly
once unless the actual effect sink participates in the same atomic protocol or
offers equivalent durable deduplication.

RIFL's numeric client identifier is uniqueness machinery, not proof of the
caller's identity. An Atom OS adaptation would need to bind request identity
and retained results to an authenticated service incarnation and the capability
authorizing the operation. Even then, authenticated identity answers who
presented a credential; it does not itself authorize the requested action.

## Limits

The failure model is centered on crash, retry, and data migration, not
Byzantine clients, compromised servers, credential theft, or malicious replay.
The mechanism assumes reliable durable storage and atomic coupling between the
operation and completion record; it does not create those properties. It also
assumes the underlying system supplies request-response RPC, automatic retry,
object ownership and migration, and a recoverable centralized lease service.

The cluster-clock protocol is only partly described in the conference paper.
Long disruptions trade lease safety against retained metadata and availability,
and client loss remains an end-to-end ambiguity. The RAMCloud measurements use
2015-era datacenter hardware and a specialized in-memory store, so they provide
no direct evidence about embedded footprint, flash endurance, actor-mailbox
traffic, or Atom OS scheduling interference.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [2026-09-03 OTP-like system services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
