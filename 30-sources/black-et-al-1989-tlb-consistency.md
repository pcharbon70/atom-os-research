---
title: "Translation lookaside buffer consistency: A software approach"
kind: source
created: "2026-09-04"
authors:
  - "David L. Black"
  - "Richard F. Rashid"
  - "David B. Golub"
  - "Charles R. Hill"
  - "Robert V. Baron"
published: 1989
citation_key: "black-et-al-1989-tlb-consistency"
container: "Third International Conference on Architectural Support for Programming Languages and Operating Systems"
edition: null
isbn: "978-0-89791-300-3"
doi: "10.1145/70082.68193"
url: "https://doi.org/10.1145/70082.68193"
accessed: "2026-09-04"
tags:
  - multicore
  - operating-systems
  - tlb
  - virtual-memory
aliases:
  - "Mach TLB consistency"
---

# Translation lookaside buffer consistency: A software approach

## Reference

David L. Black, Richard F. Rashid, David B. Golub, Charles R. Hill, and Robert
V. Baron. “Translation Lookaside Buffer Consistency: A Software Approach.”
*ASPLOS III*, pages 113–122, 1989. DOI
[10.1145/70082.68193](https://doi.org/10.1145/70082.68193).
[Open copy](https://www.cs.rice.edu/~alc/comp521/Papers/p113-black.pdf).

## Research question or contribution

How can an operating system maintain TLB consistency on multiprocessors whose
hardware does not make translation caches coherent?

## Method

The paper develops Mach's initiator and responder algorithms, considers
hardware variations in page-table and TLB organization, and tests the protocol
by repeatedly reducing mappings to read-only while processors concurrently
modify protected counters. It also reports contemporary performance data.

## Findings

- Data-cache coherence does not imply translation-cache coherence. The OS must
  separately track which processors can use a physical map and coordinate
  invalidation after relevant mapping changes.
- Removing access or reducing permission requires remote processors to stop
  using the old translation before the restrictive effect is complete.
- A permission increase can sometimes tolerate a temporarily stale restrictive
  translation, while reductions cannot tolerate a stale permissive one.
- Hardware that reloads or writes translation state creates additional races;
  the exact page-table update and invalidation algorithm is architecture
  dependent.
- Target sets and acknowledgement are first-class protocol state, not merely
  an optimization around a page-table store.
- Mach bounds each processor's pending address-invalidation list; when that
  list overflows, the responder conservatively upgrades the batch to a full-TLB
  invalidation instead of dropping an address or allocating in the interrupt
  path.

## Relevance

This work supplies the historical foundation for separating an invalidation
plan from a shootdown coordinator and for classifying mapping changes by the
danger of stale translations. Its stress test also inspires Atom's requirement
to race permission reduction against actual access, not only inspect tables.

## Limits

The paper evaluates late-1980s Mach and hardware. Modern processors have deeper
walk caches, context tags, weak ordering, speculation, virtualization, and
different invalidation instructions. Its algorithm is precedent, not a modern
proof or performance forecast, and it does not cover DMA translation.

## Derived work

- [Invalidation planner](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/invalidation-planner.md)
- [Shootdown coordinator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/shootdown-coordinator.md)
- [Mapping transaction](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/mapping-transaction.md)
