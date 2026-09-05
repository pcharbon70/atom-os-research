---
title: "Hardware translation coherence for virtualized systems"
kind: source
created: "2026-09-04"
authors:
  - "Zi Yan"
  - "Ján Veselý"
  - "Guilherme Cox"
  - "Abhishek Bhattacharjee"
published: 2017
citation_key: "yan-et-al-2017-hatric"
container: "44th Annual International Symposium on Computer Architecture"
edition: null
isbn: "978-1-4503-4892-8"
doi: "10.1145/3079856.3080211"
url: "https://doi.org/10.1145/3079856.3080211"
accessed: "2026-09-04"
tags:
  - architecture
  - hardware
  - tlb
  - virtualization
  - virtual-memory
aliases:
  - "HATRIC"
---

# Hardware translation coherence for virtualized systems

## Reference

Zi Yan, Ján Veselý, Guilherme Cox, and Abhishek Bhattacharjee. “Hardware
Translation Coherence for Virtualized Systems.” *ISCA 2017*, pages 430–443.
DOI [10.1145/3079856.3080211](https://doi.org/10.1145/3079856.3080211).
[Author-hosted paper](https://guilhermecox.github.io/dw/ziyan-isca17.pdf).

## Research question or contribution

Can hardware track dependencies between cached translations and page-table
entries through the existing cache-coherence substrate, reducing expensive
software shootdowns in virtualized systems?

## Method

The authors design HATRIC, simulate it with KVM and Xen workloads, analyze area
and energy, and compare it with software and prior hardware translation-
coherence approaches. Translation structures retain a compact coherence tag
derived from the page-table-entry address.

## Findings

- Translation coherence is a distinct system problem even where ordinary data
  caches are coherent, and virtualization multiplies the affected translation
  structures.
- HATRIC invalidates dependent translation entries through cache-coherence
  traffic rather than broadcast software IPIs.
- The paper reports performance improvements up to 30%, energy savings around
  10%, and estimated per-CPU area cost around 0.2% in its modeled systems; one
  Xen configuration reports gains up to 33%.
- Coherence granularity and false invalidation remain design trade-offs.

## Relevance

HATRIC is evidence that a future backend may provide stronger hardware
translation-coherence assistance. Atom's portable contract should allow such
a backend to satisfy the same invalidation and completion effects without
exposing IPIs as the API or weakening the conservative software baseline.

## Limits

This is a simulated hardware proposal focused on virtualized workloads, not a
shipping mechanism or Atom prototype. Reported maxima are configuration-
specific. Hardware invalidation still requires a precisely specified
completion and reclamation contract; it does not replace authority validation,
mapping identity, DMA quiescence, or software-object lifetime management.

## Derived work

- [Invalidation planner](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/invalidation-planner.md)
- [Shootdown coordinator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/shootdown-coordinator.md)
