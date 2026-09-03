---
title: "Hazard pointers: Safe memory reclamation for lock-free objects"
kind: source
created: "2026-09-03"
authors:
  - "Maged M. Michael"
published: 2004
citation_key: "michael-2004-hazard-pointers"
container: "IEEE Transactions on Parallel and Distributed Systems"
edition: null
isbn: null
doi: "10.1109/TPDS.2004.8"
url: "https://research.ibm.com/publications/hazard-pointers-safe-memory-reclamation-for-lock-free-objects"
accessed: "2026-09-03"
tags:
  - concurrency
  - lock-free
  - memory-reclamation
  - quiescence
aliases:
  - "Hazard pointers paper"
---

# Hazard pointers: Safe memory reclamation for lock-free objects

## Reference

Maged M. Michael. “Hazard Pointers: Safe Memory Reclamation for Lock-Free
Objects.” *IEEE Transactions on Parallel and Distributed Systems* 15, no. 6
(2004): 491–504. DOI
[10.1109/TPDS.2004.8](https://doi.org/10.1109/TPDS.2004.8).
[IBM Research record](https://research.ibm.com/publications/hazard-pointers-safe-memory-reclamation-for-lock-free-objects)
and [open paper](https://www.eecg.utoronto.ca/~amza/ece1747h/papers/hazard_pointers.pdf).

## Research question or contribution

Can nodes removed from lock-free data structures be reclaimed for arbitrary
reuse without special scheduler support, multiword atomic instructions, or a
global quiescence wait? The paper introduces hazard pointers: each participant
publishes the addresses it may dereference, while reclaimers retain removed
nodes until no published hazard protects them.

## Method

The paper defines the method and progress properties, applies it to lock-free
objects and ABA avoidance, derives bounds on unreclaimed retired nodes, and
compares implementations on a multiprocessor system under several contention
and multiprogramming conditions.

## Findings

- The core protection and scan operations require only single-word reads and
  writes and are independent of special kernel scheduling support.
- A reclaimer can safely reuse a retired node once no participant's protected
  hazard set names it and the data-structure removal is already complete.
- Per-participant hazard slots provide an explicit bound on simultaneously
  protected nodes; batching retired-node scans amortizes work.
- The method remains available despite participant delay or failure, although
  a permanently published hazard can retain the particular protected node.
- Hazard pointers can also avoid the ABA problem when the reclamation and
  reuse discipline is followed.

## Relevance

Hazard-style bounded activation pins are a candidate for fast kernel-object
lookup paths whose maximum simultaneous protected references are known. They
make the pin holder and retained object explicit, complementing epoch or RCU
schemes. Atom OS could use fixed per-CPU or per-activation slots and charge the
retired set to the object's teardown account.

## Limits

The paper concerns software references in lock-free data structures. It does
not cover user execution, page-table walkers, TLBs, interrupts, device queues,
DMA, reset domains, or external side effects. Scanning work grows with the
number of participants and hazard slots, so a kernel implementation must bound
both. A crashed CPU that cannot clear protected kernel state is a platform
failure problem, not something hazard pointers solve. The evaluation does not
establish performance on current heterogeneous many-core hardware.

## Derived work

- [Teardown, revocation, and safe reclamation](../20-notes/minimal-privileged-kernel-components/teardown-revocation-and-safe-reclamation.md)
- [Typed object storage and explicit memory](../20-notes/minimal-privileged-kernel-components/typed-object-storage-and-explicit-memory.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
