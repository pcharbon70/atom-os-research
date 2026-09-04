---
title: "Zanzibar: Google's consistent, global authorization system"
kind: source
created: "2026-09-04"
authors:
  - "Ruoming Pang"
  - "Ramon Caceres"
  - "Mike Burrows"
  - "Zhifeng Chen"
  - "Pratik Dave"
  - "Nathan Germer"
  - "Alexander Golynski"
  - "Kevin Graney"
  - "Nina Kang"
  - "Lea Kissner"
  - "Jeffrey L. Korn"
  - "Abhishek Parmar"
  - "Christina D. Richards"
  - "Mengzhi Wang"
published: 2019
citation_key: "pang-et-al-2019-zanzibar"
container: "2019 USENIX Annual Technical Conference"
edition: null
isbn: "978-1-939133-03-8"
doi: null
url: "https://www.usenix.org/system/files/atc19-pang.pdf"
accessed: "2026-09-04"
tags:
  - authorization
  - consistency
  - distributed-systems
  - relationship-based-access-control
aliases:
  - "Zanzibar"
---

# Zanzibar: Google's consistent, global authorization system

## Reference

Ruoming Pang et al. “[Zanzibar: Google’s Consistent, Global Authorization
System](https://www.usenix.org/system/files/atc19-pang.pdf).” *2019 USENIX
Annual Technical Conference*, pages 33–46, July 2019.

## Research question or contribution

The paper describes a deployed service for storing relationship tuples and
evaluating shared authorization policy with low latency, high availability,
large scale, and causal consistency between content and ACL changes.

## Method

The authors document the data model, configuration language, consistency
tokens, distributed architecture, caching, hot-spot and client isolation, and
three years of Google production experience.

## Findings

- Relation tuples and set operations express owner, member, editor, viewer, and
  derived permissions across application objects.
- Opaque consistency tokens let clients require checks at least as fresh as a
  causally preceding ACL or content update, preventing stale authorization from
  violating user-visible ordering.
- The deployed service reports trillions of ACLs, millions of authorization
  requests per second, sub-10-ms 95th-percentile latency, and greater than
  99.999% availability over the reported period.
- Caches, snapshot reads, replication, and overload isolation are part of the
  authorization correctness and availability story, not transparent details.

## Relevance

Atom OS can borrow the relation model and explicit freshness tokens for
distributed sharing policy, but should mint short-lived, resource-specific
grants after a decision. The committing resource must validate the grant’s
object generation and minimum policy revision so that a check separated from
the effect does not reintroduce a time-of-check/time-of-use race.

## Limits

This is one company’s global service built on Google infrastructure and threat
assumptions. The reported scale is not an Atom OS requirement, and Zanzibar
does not provide human authentication, local kernel authority, credential
holder binding, device attestation, mandatory information flow, or a complete
solution to effects that race with revocation.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
