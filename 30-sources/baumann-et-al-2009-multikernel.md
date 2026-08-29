---
title: "The Multikernel: A new OS architecture for scalable multicore systems"
kind: source
created: "2026-08-29"
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
accessed: "2026-08-29"
tags:
  - actor-model
  - hardware-heterogeneity
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

The paper asks whether an operating system should treat a heterogeneous
multicore machine as a distributed system rather than hide it behind globally
shared kernel structures.

## Method

The authors define three principles—explicit inter-core communication,
hardware-neutral structure, and replicated rather than shared state—implement
them in Barrelfish, and compare messaging, shared-state updates, capability
operations, and application behavior on contemporary multicore hardware.

## Findings

- Hardware diversity includes core ISA and performance, cache and interconnect
  topology, memory ordering, NUMA placement, and non-coherent devices.
- Explicit messages expose communication, allow batching and pipelining, and
  extend naturally to cores or accelerators that cannot share ordinary memory.
- Replication can remove shared-state bottlenecks but introduces distributed
  consistency, agreement, naming, and failure problems inside one machine.
- The evaluated prototype showed competitive behavior on its tested systems;
  it did not prove that every shared structure or modern workload benefits.

## Relevance

An OTP-inspired OS should use explicit per-CPU ownership and asynchronous
cross-core protocols where this makes state and failure visible. It should not
turn the hardware layer itself into a fully replicated distributed kernel
before measuring the consistency and recovery costs. A hybrid—per-CPU fast
paths plus a small set of globally enforced capability invariants—is the
current synthesis.

## Limits

The evaluation is from 2009 hardware and Barrelfish's research implementation.
Current coherent interconnects, core counts, accelerators, and security threats
differ. Message passing can move rather than eliminate synchronization costs.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
