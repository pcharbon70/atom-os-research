---
title: "Optimizing the TLB shootdown algorithm with page access tracking"
kind: source
created: "2026-09-02"
authors:
  - "Nadav Amit"
published: 2017
citation_key: "amit-2017-optimizing-tlb-shootdown"
container: "2017 USENIX Annual Technical Conference"
edition: null
isbn: "978-1-931971-38-6"
doi: null
url: "https://www.usenix.org/conference/atc17/technical-sessions/presentation/amit"
accessed: "2026-09-02"
tags:
  - multicore
  - operating-systems
  - performance
  - tlb
  - virtual-memory
aliases:
  - "Page-access-tracked TLB shootdown"
---

# Optimizing the TLB shootdown algorithm with page access tracking

## Reference

Nadav Amit. “Optimizing the TLB Shootdown Algorithm with Page Access
Tracking.” *2017 USENIX Annual Technical Conference*, pages 27–39, 2017.
[USENIX paper and artifacts](https://www.usenix.org/conference/atc17/technical-sessions/presentation/amit).

## Research question or contribution

Can an operating system avoid unnecessary remote translation invalidations by
using hardware-maintained page-access state to identify mappings that cannot
be cached by other processors?

## Method

The work modifies Linux on x86, adds page-access-tracking techniques to its TLB
shootdown subsystem, analyzes the conditions under which remote invalidation
can be omitted, and evaluates application and microbenchmark behavior.

## Findings

- TLB shootdowns are synchronous cross-CPU protocols whose cost grows with the
  number of possible users of an address space; batching alone does not remove
  unnecessary targets.
- The evaluated techniques use x86 page-access information to recognize cases
  in which a translation was local or was never installed, and therefore avoid
  a remote shootdown without weakening the required postcondition.
- The implementation reduced invalidations by up to 98% on average and
  improved selected workloads by up to 78% in the reported configuration.
- Tracking is not free. The paper reports overheads up to 9% when mappings are
  never removed, making the optimization workload- and mechanism-dependent.

## Relevance

The baseline translation protocol should first be correct with a conservative
active-CPU set and acknowledged remote invalidation. Targeted or avoided
shootdowns can then be introduced behind the same completion contract, with a
proof that the tracking evidence is sufficient on the selected architecture.

## Limits

The mechanism and evaluation are x86- and Linux-specific. Accessed-bit
semantics, page-table walkers, virtualization, and available invalidation
instructions differ on Arm and RISC-V. Reported maxima are not portable
performance promises, and the technique does not establish safe frame reuse
after an unresponsive target CPU.

## Derived work

- [Address translation and protection transitions](../20-notes/address-translation-and-protection-transitions.md)
