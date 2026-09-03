---
title: "Scalable and effective page-table and TLB management on NUMA systems"
kind: source
created: "2026-09-02"
authors:
  - "Bin Gao"
  - "Qingxuan Kang"
  - "Hao-Wei Tee"
  - "Kyle Timothy Ng Chu"
  - "Alireza Sanaee"
  - "Djordje Jevdjic"
published: 2024
citation_key: "gao-et-al-2024-scalable-page-table-tlb"
container: "2024 USENIX Annual Technical Conference"
edition: null
isbn: "978-1-939133-41-0"
doi: null
url: "https://www.usenix.org/conference/atc24/presentation/gao-bin-scalable"
accessed: "2026-09-02"
tags:
  - multicore
  - numa
  - operating-systems
  - performance
  - tlb
  - virtual-memory
aliases:
  - "Hydra page-table management"
---

# Scalable and effective page-table and TLB management on NUMA systems

## Reference

Bin Gao et al. “Scalable and Effective Page-Table and TLB Management on NUMA
Systems.” *2024 USENIX Annual Technical Conference*, pages 445–461, 2024.
[USENIX paper and metadata](https://www.usenix.org/conference/atc24/presentation/gao-bin-scalable).

## Research question or contribution

Can partial, demand-driven page-table replication retain local NUMA page walks
without paying the mutation and shootdown cost of eagerly replicating every
page-table page?

## Method

The authors measure mapping operations on four- and eight-socket x86-64
systems, implement Hydra in Linux, replicate page-table subtrees on demand,
track their sharers, and evaluate microbenchmarks and applications.

## Findings

- The paper reports up to 40-fold overhead for selected `munmap` and
  `mprotect` cases as the affected process spans a large NUMA system.
- Full page-table replication improves walk locality but adds coherence work
  to each mapping change.
- Hydra's partial replication records precise sharers, which also narrows some
  TLB shootdowns. The reported Webserver and Memcached experiments improved by
  12% and 36%, respectively, over the evaluated baseline.
- Translation locality, mutation frequency, replication, and invalidation
  targeting are one coupled performance problem; optimizing only walks can
  make protection transitions worse.

## Relevance

The address-space object should expose a stable mutation and completion
contract while keeping its page-table placement strategy private. The first
kernel should use one non-replicated page-table hierarchy per address space;
partial NUMA replication is a later optimization that must preserve mapping
identity, target-set soundness, and reclamation epochs.

## Limits

Hydra is a Linux/x86-64 research implementation evaluated on large NUMA
servers. It adds replica metadata and algorithms inappropriate for a minimal
first port, and its results do not transfer directly to Arm, RISC-V, small
systems, MPU-only targets, or this project's capability object model.

## Derived work

- [Address translation and protection transitions](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions.md)
