---
title: "RadixVM: Scalable address spaces for multithreaded applications"
kind: source
created: "2026-09-04"
authors:
  - "Austin T. Clements"
  - "M. Frans Kaashoek"
  - "Nickolai Zeldovich"
published: 2013
citation_key: "clements-et-al-2013-radixvm"
container: "Proceedings of the 8th ACM European Conference on Computer Systems"
edition: null
isbn: "978-1-4503-1994-2"
doi: "10.1145/2465351.2465373"
url: "https://doi.org/10.1145/2465351.2465373"
accessed: "2026-09-04"
tags:
  - multicore
  - operating-systems
  - page-tables
  - scalability
  - tlb
  - virtual-memory
aliases:
  - "RadixVM"
---

# RadixVM: Scalable address spaces for multithreaded applications

## Reference

Austin T. Clements, M. Frans Kaashoek, and Nickolai Zeldovich. “RadixVM:
Scalable Address Spaces for Multithreaded Applications.” *EuroSys 2013*, pages
211–224. DOI
[10.1145/2465351.2465373](https://doi.org/10.1145/2465351.2465373).
[Authors' project page and open paper](https://pdos.csail.mit.edu/archive/multicore/radixvm/).

## Research question or contribution

Can a virtual-memory system make nonoverlapping operations in one shared
address space scale across many cores, including the metadata, page-table, and
TLB-shootdown paths that conventional kernels serialize?

## Method

RadixVM is implemented in a research kernel and evaluated on an 80-core x86
machine. The paper combines radix-tree VM metadata, refcache-based reference
management, per-core page tables, and precise tracking of which cores may need
shootdown; it measures microbenchmarks and applications while varying cores
and operation locality.

## Findings

- The evaluated system achieves near-perfect scaling for concurrent operations
  on nonoverlapping regions; removing one global address-space lock is not
  sufficient unless metadata, reference counts, page tables, and shootdowns
  are also addressed.
- Unmap first removes metadata and page-table reachability, determines the
  cores that can cache the translation, sends invalidations, waits for every
  response, and only then releases physical-memory references.
- Range-indexed metadata and precise per-range core tracking reduce unrelated
  contention and shootdown fanout.
- Per-core page tables improve mutation scalability but consume additional
  memory and may cause additional faults when mappings must be materialized on
  another core.

## Relevance

RadixVM grounds the distinction among a logical mapping ledger, encoded page
tables, target-set derivation, acknowledged invalidation, and reclamation. It
also motivates range-local concurrency as an optional later implementation,
after Atom proves a simpler single-writer baseline.

## Limits

The implementation is a research kernel evaluated on one cache-coherent x86
platform. Its replication and tracking mechanisms add state and failure modes,
and its performance does not transfer to AArch64 or RISC-V. Waiting for an IPI
acknowledgement is useful precedent but still needs ISA-specific proof about
walkers and reclamation.

## Derived work

- [Address-space object](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/address-space-object.md)
- [Mapping transaction](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/mapping-transaction.md)
- [Shootdown coordinator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/shootdown-coordinator.md)
- [Reclamation gate](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/reclamation-gate.md)
