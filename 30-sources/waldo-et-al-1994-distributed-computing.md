---
title: "A Note on Distributed Computing"
kind: source
created: "2026-09-05"
authors:
  - "Jim Waldo"
  - "Geoff Wyant"
  - "Ann Wollrath"
  - "Sam Kendall"
published: 1994
citation_key: "waldo-et-al-1994-distributed-computing"
container: "Sun Microsystems Laboratories Technical Report TR-94-29"
edition: null
isbn: null
doi: null
url: "https://waldo.scholars.harvard.edu/publications/note-distributed-computing"
accessed: "2026-09-05"
tags:
  - distributed-systems
  - partial-failure
  - remote-interfaces
aliases:
  - "Waldo note on distributed computing"
---

# A Note on Distributed Computing

## Reference

Jim Waldo, Geoff Wyant, Ann Wollrath, and Sam Kendall. “[A Note on Distributed
Computing](https://waldo.scholars.harvard.edu/publications/note-distributed-computing).”
Sun Microsystems Laboratories Technical Report TR-94-29, 1994.

## Research question or contribution

The report argues against making remote and local object interactions
indistinguishable because latency, concurrency, memory access, and partial
failure change correct interface design.

## Method

It is a design position grounded in distributed-object experience and failure
analysis, not a benchmark or formal impossibility proof.

## Findings

- Remote calls can fail independently of caller and callee state and have
  orders-of-magnitude different latency.
- Interfaces that conceal distribution encourage designs unable to recover
  from partial failure or control network work.
- Distribution boundaries should be chosen deliberately rather than added
  transparently after local interfaces are fixed.

## Relevance

Actor ports that may cross a protected domain or node must expose deadlines,
admission, cancellation, retry identity, backpressure, fencing, reconciliation,
and `Indeterminate` outcomes. Adapter syntax cannot make a remote effect local.

## Limits

The report predates current transports and actor platforms. It supplies a
durable warning, not a complete outcome protocol or rule that every local and
remote interface must look unrelated.

## Derived work

- [External effects, ports, adapters, and reconciliation](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation.md)
- [Typed commands, queries, events, and protocol contracts](../20-notes/applications-and-domain-services-components/typed-commands-queries-events-and-protocol-contracts.md)
