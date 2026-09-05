---
title: "Machine-independent virtual memory management for paged uniprocessor and multiprocessor architectures"
kind: source
created: "2026-09-04"
authors:
  - "Richard Rashid"
  - "Avadis Tevanian"
  - "Michael Young"
  - "David Golub"
  - "Robert Baron"
  - "David Black"
  - "William Bolosky"
  - "Jonathan Chew"
published: 1987
citation_key: "rashid-et-al-1987-machine-independent-virtual-memory"
container: "Second International Conference on Architectural Support for Programming Languages and Operating Systems"
edition: null
isbn: "0-8186-0805-6"
doi: "10.1145/36206.36181"
url: "https://doi.org/10.1145/36206.36181"
accessed: "2026-09-04"
tags:
  - architecture-support
  - operating-systems
  - portability
  - virtual-memory
aliases:
  - "Mach machine-independent VM"
---

# Machine-independent virtual memory management for paged uniprocessor and multiprocessor architectures

## Reference

Richard Rashid, Avadis Tevanian, Michael Young, David Golub, Robert Baron,
David Black, William Bolosky, and Jonathan Chew. “Machine-Independent Virtual
Memory Management for Paged Uniprocessor and Multiprocessor Architectures.”
*ASPLOS II*, pages 31–39, 1987. DOI
[10.1145/36206.36181](https://doi.org/10.1145/36206.36181).
[Open copy](https://rcs.uwaterloo.ca/~ali/readings/machvm.pdf).

## Research question or contribution

Can a virtual-memory subsystem expose machine-independent objects and policy
while confining hardware mapping details to a small machine-dependent module,
without reducing the services or measured performance of the system?

## Method

The paper describes Mach's task, memory-object, address-map, and `pmap`
abstractions and reports implementation experience across more than half a
dozen contemporary uniprocessor and multiprocessor systems. It compares how
different hardware mapping organizations fit the same higher-level model.

## Findings

- Mach keeps address-space management data in machine-independent structures
  and confines mappings needed by the hardware to one machine-dependent module
  and its header.
- The split was exercised on substantially different mapping architectures,
  rather than demonstrated on only one port.
- A task's address space is an ordered set of mappings to memory objects; the
  hardware representation is not the durable policy identity.
- The authors report that the separation did not sacrifice performance in
  their evaluated systems and sometimes improved it relative to the compared
  UNIX implementations.

## Relevance

This is foundational evidence for separating an Atom address-space object and
mapping ledger from an ISA-specific encoder. It supports a semantic interface
whose object identity, authority, and lifecycle survive a backend change, while
raw entry formats and low-level maintenance remain backend-owned.

## Limits

The hardware, workloads, security assumptions, and performance measurements
are from 1987. The paper predates current multilevel TLBs, weak virtual-memory
models, PCID/modern ASIDs, speculative execution, IOMMUs, and contemporary
many-core machines. Portability experience is not a proof that the proposed
Atom interface is complete or that modern backends have equal cost.

## Derived work

- [Address-space object](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/address-space-object.md)
- [Page-table and protection encoder](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/page-table-and-protection-encoder.md)
- [Address translation and protection transitions](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions.md)
