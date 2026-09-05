---
title: "Managing Update Conflicts in Bayou, a Weakly Connected Replicated Storage System"
kind: source
created: "2026-09-05"
authors:
  - "Douglas B. Terry"
  - "Marvin M. Theimer"
  - "Karin Petersen"
  - "Alan J. Demers"
  - "Mike J. Spreitzer"
  - "Carl H. Hauser"
published: 1995
citation_key: "terry-et-al-1995-bayou-conflicts"
container: "Proceedings of SOSP 1995"
edition: null
isbn: null
doi: "10.1145/224057.224070"
url: "https://doi.org/10.1145/224057.224070"
accessed: "2026-09-05"
tags:
  - conflict-resolution
  - disconnected-operation
  - replicated-data
aliases:
  - "Bayou conflict management"
---

# Managing Update Conflicts in Bayou, a Weakly Connected Replicated Storage System

## Reference

Douglas B. Terry, Marvin M. Theimer, Karin Petersen, Alan J. Demers, Mike J.
Spreitzer, and Carl H. Hauser. “[Managing Update Conflicts in Bayou, a Weakly
Connected Replicated Storage System](https://doi.org/10.1145/224057.224070).”
*Proceedings of the 15th ACM Symposium on Operating Systems Principles*, 1995,
pages 172–182.

## Research question or contribution

Bayou investigates application-specific conflict detection and resolution for
data replicated among weakly connected mobile servers.

## Method

The paper presents dependency checks, merge procedures, tentative and
committed writes, epidemic propagation, and experience with prototype
applications.

## Findings

- Storage cannot infer every semantic conflict from concurrent bytes;
  applications may need dependency predicates and merge logic.
- Tentative state gives availability but differs observably from globally
  ordered committed state.
- Deterministic resolution and eventual ordering can yield convergence while
  preserving application-specific policies.

## Relevance

Layer 5 must classify collaborative operations and own conflict meaning. Users
and programs must be told whether they observe tentative, committed, stale, or
conflicted state; Layer 4 replication alone cannot invent intent.

## Limits

Bayou's architecture and devices are historical. Application merge code can
be wrong, malicious, or inappropriate for security, money, scarce resources,
or irreversible effects. Eventual convergence is not domain correctness.

## Derived work

- [Offline collaboration, replication, and conflict semantics](../20-notes/applications-and-domain-services-components/offline-collaboration-replication-and-conflict-semantics.md)
