---
title: "Timing analysis of a protected operating system kernel"
kind: source
created: "2026-08-31"
authors:
  - "Bernard Blackham"
  - "Yao Shi"
  - "Sudipta Chattopadhyay"
  - "Abhik Roychoudhury"
  - "Gernot Heiser"
published: 2011
citation_key: "blackham-et-al-2011-timing-analysis-protected-kernel"
container: "2011 IEEE 32nd Real-Time Systems Symposium"
edition: null
isbn: "978-1-4577-2000-0"
doi: "10.1109/RTSS.2011.38"
url: "https://trustworthy.systems/publications/nictaabstracts/Blackham_SCRH_11.abstract"
accessed: "2026-08-31"
tags:
  - formal-verification
  - operating-systems
  - real-time
  - temporal-isolation
  - worst-case-execution-time
aliases:
  - "seL4 WCET analysis"
---

# Timing analysis of a protected operating system kernel

## Reference

Bernard Blackham, Yao Shi, Sudipta Chattopadhyay, Abhik Roychoudhury, and
Gernot Heiser. “Timing Analysis of a Protected Operating System Kernel.”
*2011 IEEE 32nd Real-Time Systems Symposium*, pages 339–348. DOI
[10.1109/RTSS.2011.38](https://doi.org/10.1109/RTSS.2011.38).
[Author record and paper](https://trustworthy.systems/publications/nictaabstracts/Blackham_SCRH_11.abstract).

## Research question or contribution

Can static worst-case execution-time analysis provide a safe interrupt-response
bound for a protected, virtual-memory microkernel rather than only for a small
single-mode real-time executive?

## Method

The authors extract a control-flow graph from an ARM seL4 kernel binary, use
symbolic execution and a modified ARM version of Chronos to model paths, caches,
and a Cortex-A8 pipeline, and solve for worst-case paths with integer linear
programming. They analyze both an open configuration that permits all kernel
operations and a closed configuration restricted to a stated set of operations.
They then construct feasible worst-case scenarios and measure them on an 800 MHz
TI DM3730 Cortex-A8 BeagleBoard-xM with the L2 cache, speculative prefetching,
and branch prediction disabled to match the analysis model more closely.

## Findings

- The small, event-based kernel, absence of run-time function pointers and
  in-kernel allocation, few nested loops, and explicit preemption points made a
  full context-aware analysis of the approximately 10,000-instruction binary
  tractable.
- Timing analysis exposed pathological scheduler and object-lifecycle paths.
  The work led to removal of lazy scheduling and to additional preemption points
  in creation and deletion paths; verification of those changes was not
  complete at publication time.
- For the analyzed binary, hardware, and configuration, the computed
  interrupt-response bound was 492.1 microseconds for the restricted closed
  system and 1.74 milliseconds for the open system.
- Computed path bounds were between 5.36 and 10.15 times the corresponding
  observed times in Table III. The authors attribute the gap to conservative
  cache and pipeline models and remaining infeasible path fragments, rather
  than treating observed maxima as safe bounds.
- Functional correctness and termination facts helped the timing argument, but
  functional verification alone did not establish a temporal guarantee.

## Relevance

A claim that the minimal kernel has bounded latency must name the kernel
configuration, permitted operation set, target processor state, and analysis
assumptions. Capability revocation, teardown, and object deletion should be
incremental or explicitly preemptible so that one large authority subtree cannot
create an unbounded non-preemptible path. Scheduling-context budgets protect
domains from one another only if kernel execution and interrupt delivery have
analyzed bounds as well. An implementation in another language would require
its own binary-level timing analysis; neither seL4's functional proof nor these
2011 bounds transfer.

## Limits

The result concerns a historical seL4 binary on one single-core Cortex-A8
configuration with important hardware features disabled. Loop bounds and some
infeasible-path exclusions required manual input, the cache and pipeline models
were deliberately conservative, and the paper did not cover multicore
interference, modern speculative processors, MCS scheduling contexts, DMA, or a
BEAM runtime. The numerical bounds are evidence about the stated experiment,
not portable constants or proof that every small kernel is temporally bounded.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
