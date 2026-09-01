---
title: "The Multikernel: A new OS architecture for scalable multicore systems"
kind: source
created: "2026-08-30"
authors:
  - "Andrew Baumann"
  - "Paul Barham"
  - "Pierre-Evariste Dagand"
  - "Tim Harris"
  - "Rebecca Isaacs"
  - "Simon Peter"
  - "Timothy Roscoe"
  - "Adrian Schüpbach"
  - "Akhilesh Singhania"
published: 2009
citation_key: "baumann-et-al-2009-multikernel"
container: "Proceedings of the 22nd ACM Symposium on Operating Systems Principles"
edition: null
isbn: "978-1-60558-752-3"
doi: "10.1145/1629575.1629579"
url: "https://barrelfish.org/publications/barrelfish_sosp09.pdf"
accessed: "2026-08-30"
tags:
  - hardware-heterogeneity
  - message-passing
  - multicore
  - operating-systems
  - scalability
aliases:
  - "The Multikernel"
---

# The Multikernel: A new OS architecture for scalable multicore systems

## Reference

Andrew Baumann et al. “The Multikernel: A New OS Architecture for Scalable
Multicore Systems.” *SOSP '09*, 2009. DOI
[10.1145/1629575.1629579](https://doi.org/10.1145/1629575.1629579).
[Author-hosted PDF](https://barrelfish.org/publications/barrelfish_sosp09.pdf).

## Research question or contribution

Should an operating system treat a diverse multicore machine as a distributed
system rather than organize its core around globally shared, lock-protected
state?

## Method

The authors propose explicit inter-core communication, hardware-neutral OS
structure, and replicated rather than shared state; implement those principles
in Barrelfish; and evaluate messaging, capability operations, shared updates,
and applications on contemporary multicore systems.

## Findings

- Cache hierarchy, interconnect, memory ordering, core behavior, and even ISA
  can vary within or across machines, making assumptions embedded in shared
  data structures fragile.
- Explicit messages make communication and ownership transfers visible and can
  support batching, pipelining, non-coherent memory, and heterogeneous cores.
- Per-core replication reduces some shared-state bottlenecks but introduces
  distributed consistency, agreement, naming, and failure problems inside the
  machine.
- The prototype showed competitive results on its tested hardware; the work
  does not establish that messages dominate shared memory for every object,
  core count, or modern coherent system.

## Relevance

The architecture layer should prefer CPU-local ownership and explicit
cross-CPU requests for TLB invalidation, CPU lifecycle, interrupt migration,
and other infrequent global transitions. It should not require a complete
multikernel. Small read-mostly snapshots or carefully synchronized global
invariants may be simpler. The decision belongs to each component's access and
failure pattern.

## Limits

The hardware and Barrelfish implementation are historical. Message passing can
move synchronization costs into protocols, and replication can complicate
revocation and recovery. Measurements must be repeated for chosen targets.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
