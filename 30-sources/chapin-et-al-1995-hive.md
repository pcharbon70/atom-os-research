---
title: "Hive: Fault containment for shared-memory multiprocessors"
kind: source
created: "2026-08-31"
authors:
  - "John Chapin"
  - "Mendel Rosenblum"
  - "Scott Devine"
  - "Tirthankar Lahiri"
  - "Dan Teodosiu"
  - "Anoop Gupta"
published: 1995
citation_key: "chapin-et-al-1995-hive"
container: "Proceedings of the 15th ACM Symposium on Operating Systems Principles"
edition: null
isbn: "0-89791-715-4"
doi: "10.1145/224056.224059"
url: "https://www.scs.stanford.edu/nyu/04fa/sched/readings/hive.pdf"
accessed: "2026-08-31"
tags:
  - fault-containment
  - multicore
  - operating-systems
  - shared-memory
aliases:
  - "Hive"
---

# Hive: Fault containment for shared-memory multiprocessors

## Reference

John Chapin, Mendel Rosenblum, Scott Devine, Tirthankar Lahiri, Dan Teodosiu,
and Anoop Gupta. “Hive: Fault Containment for Shared-Memory Multiprocessors.”
*SOSP '95*, pages 12–25. DOI
[10.1145/224056.224059](https://doi.org/10.1145/224056.224059).
[Open PDF](https://www.scs.stanford.edu/nyu/04fa/sched/readings/hive.pdf).

## Research question or contribution

Can a large shared-memory multiprocessor be divided into operating-system cells
so a hardware or kernel fault affects only the applications using the failed
cell?

## Method

Hive partitions processors and memory into kernel cells, controls cross-cell
sharing, and models recovery under specified fail-stop and memory-corruption
assumptions in the SimOS environment.

## Findings

- Containment is operational: an application's failure probability should
  depend on the resources it uses rather than the size of the entire machine.
- Shared devices, memory, kernel state, and recovery services create correlated
  failure even when software components have separate address spaces.
- Recovery from memory-node failure requires hardware behavior to be stated:
  failed accesses must terminate, unaffected memory must remain sound, and the
  possible corruption set must be bounded.
- The reported injection campaign contained 49 fail-stop hardware faults and 20
  kernel-data corruptions to the affected cell under the simulation model.

## Relevance

Every claimed domain boundary must list shared dependencies: privileged kernel,
CPU/cache/memory, interrupt and IOMMU infrastructure, devices, runtime,
supervisor, state store, firmware, and recovery image. A BEAM actor inside one
runtime is not hardware- or memory-fault independent from its peers.

## Limits

The intended FLASH hardware was unavailable; simulation, small campaigns, and
partly oracle-assisted agreement bound the result. Reintegration was incomplete,
and the fault model does not cover arbitrary commodity hardware, malicious
devices, or all correlated faults.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
