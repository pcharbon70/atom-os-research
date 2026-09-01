---
title: "For a microkernel, a big lock is fine"
kind: source
created: "2026-08-31"
authors:
  - "Sean Peters"
  - "Adrian Danis"
  - "Kevin Elphinstone"
  - "Gernot Heiser"
published: 2015
citation_key: "peters-et-al-2015-big-lock-microkernel"
container: "Proceedings of the 6th Asia-Pacific Workshop on Systems"
edition: null
isbn: "978-1-4503-3554-6"
doi: "10.1145/2797022.2797042"
url: "https://trustworthy.systems/publications/nictaabstracts/Peters_DEH_15.abstract"
accessed: "2026-08-31"
tags:
  - microkernels
  - multicore
  - operating-systems
  - scalability
  - synchronization
aliases:
  - "Big-lock microkernel study"
---

# For a microkernel, a big lock is fine

## Reference

Sean Peters, Adrian Danis, Kevin Elphinstone, and Gernot Heiser. “For a
Microkernel, a Big Lock Is Fine.” *Proceedings of the 6th Asia-Pacific Workshop
on Systems*, Article 3, pages 3:1–3:7, 2015. DOI
[10.1145/2797022.2797042](https://doi.org/10.1145/2797022.2797042).
[Author record and paper](https://trustworthy.systems/publications/nictaabstracts/Peters_DEH_15.abstract).

## Research question or contribution

For a small microkernel running on a moderate number of closely coupled cores,
does fine-grained locking repay its acquisition, complexity, and assurance
costs, or can a single kernel lock remain competitive?

## Method

The authors build multicore seL4 prototypes using a CLH big kernel lock, a big
reader lock plus fine-grained locks, and Intel restricted transactional memory;
an unsafe no-lock build supplies a theoretical baseline. They measure hot-cache
IPC on a four-core Arm Cortex-A9 i.MX6Q and on a four-core/eight-hardware-thread
Intel i7-4770. On x86 they also run user-level Ethernet and lwIP with one Redis
instance per hardware thread under YCSB workload A, comparing throughput and
CPU utilization.

## Findings

- In the single-core IPC measurement, the big lock added 65 cycles, about 10%,
  on x86 and 124 cycles, about 20%, on Arm. The evaluated fine-grained design
  added about 30% and 60%, respectively, because a typical call acquired four
  locks and Arm required additional memory barriers.
- In the intentionally pathological multicore ping-pong test, which performed
  almost no user work, big-lock throughput plateaued after three cores.
  Fine-grained locking scaled because the benchmark used disjoint objects.
- In the x86 Redis macrobenchmark, all seL4 locking variants had similar
  throughput through eight hardware threads. The workload was network-bound
  with substantial idle time; normalized efficiency showed only a small
  big-lock reduction rather than a contention cliff.
- Fine-grained locking exposed substantially more concurrent state. The authors
  report that, even after months of work, they were not confident their
  prototype was fully correct; the existing seL4 proofs covered the single-core
  kernel, not these multicore variants.
- The paper's conclusion is conditional: a big lock can remain attractive when
  kernel critical sections and shared-cache latency are short, user execution
  between kernel entries is comparatively long, and a cluster has a moderate
  core count.

## Relevance

An initial minimal kernel can use one lock per tightly coupled core cluster to
preserve simple invariants, while using explicit cross-cluster messages and
replicated state when scaling requires it. The lock must not cover user-level
drivers or BEAM runtime work, and long lifecycle operations must remain
preemptible. The architecture contract still needs cross-core entry,
quiescence, TLB-completion, and interrupt-routing mechanisms. Contention and
hold time should be measured under BEAM scheduler, IPC, fault, and teardown
loads before replacing the simple design with finer-grained synchronization.

## Limits

This was a prototype on two 2015 shared-cache machines: four physical cores on
each, with x86 results extended to eight-way parallelism through simultaneous
multithreading. The only macrobenchmark ran on x86 and was limited by network
throughput; no Arm macrobenchmark, NUMA system, high-core-count cluster, or BEAM
workload was evaluated. The prototypes were not the verified single-core seL4
kernel, and the paper neither proves the big lock correct nor establishes that
it scales on modern many-core systems. It supports a measured starting choice,
not a universal locking rule.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
