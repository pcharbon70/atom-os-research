---
title: "A scalable implementation of virtual memory HAT layer for shared memory multiprocessor machines"
kind: source
created: "2026-09-04"
authors:
  - "Ramesh Balan"
  - "Kurt Gollhardt"
published: 1992
citation_key: "balan-gollhardt-1992-scalable-virtual-memory-hat-layer"
container: "USENIX Summer 1992 Technical Conference"
edition: null
isbn: null
doi: null
url: "https://www.usenix.org/conference/usenix-summer-1992-technical-conference/scalable-implementation-virtual-memory-hat-layer"
accessed: "2026-09-04"
tags:
  - architecture-support
  - multicore
  - operating-systems
  - scalability
  - tlb
  - virtual-memory
aliases:
  - "SVR4.2 HAT layer"
---

# A scalable implementation of virtual memory HAT layer for shared memory multiprocessor machines

## Reference

Ramesh Balan and Kurt Gollhardt. “A Scalable Implementation of Virtual Memory
HAT Layer for Shared Memory Multiprocessor Machines.” *USENIX Summer 1992
Technical Conference*, 1992.
[USENIX record and paper](https://www.usenix.org/conference/usenix-summer-1992-technical-conference/scalable-implementation-virtual-memory-hat-layer).

## Research question or contribution

How can the hardware-address-translation portion of a UNIX virtual-memory
system remain portable and scale across shared-memory multiprocessors?

## Method

The authors describe the SVR4.2 HAT interface, its division from the machine-
independent VM subsystem, its active-processor accounting and shootdown
protocols, and its locking design. Early measurements use a four-processor
20 MHz Intel 386 Sequent Symmetry system.

## Findings

- A small machine-dependent HAT interface can own TLB consistency while most
  VM state and policy remain machine independent.
- Per-address-space processor accounting lets mutation target processors that
  could hold the address space rather than indiscriminately flushing all CPUs.
- Fine-grained VM locking and lazy evaluation of whether a shootdown is needed
  were central to the implementation's scalability argument.
- The HAT layer still depends on architecture-specific page-table mutation and
  interprocessor-interrupt mechanisms; the paper assumes hardware data-cache
  coherence.

## Relevance

The HAT work supports keeping mapping policy above a narrow encoder,
invalidation-planner, and shootdown boundary. Its explicit load/unload hooks
also show that address-space activation and mutation must share a concurrency
protocol rather than maintain unrelated CPU masks.

## Limits

The design and preliminary measurements target early-1990s SVR4.2, i386, and
small cache-coherent SMP systems. The paper says the measurements are not final.
Its lazy policy and locking choices cannot be transferred without re-proving
them for modern walkers, weak virtual-memory semantics, CPU hotplug, and Atom's
quiescence contract.

## Derived work

- [Page-table and protection encoder](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/page-table-and-protection-encoder.md)
- [Mapping transaction](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/mapping-transaction.md)
- [Shootdown coordinator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/shootdown-coordinator.md)
