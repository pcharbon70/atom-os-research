---
title: "LazyFP: Leaking FPU register state using microarchitectural side-channels"
kind: source
created: "2026-08-29"
authors:
  - "Julian Stecklina"
  - "Thomas Prescher"
published: 2018
citation_key: "stecklina-prescher-2018-lazyfp"
container: "CoRR abs/1806.07480"
edition: null
isbn: null
doi: "10.48550/arXiv.1806.07480"
url: "https://arxiv.org/abs/1806.07480"
accessed: "2026-08-29"
tags:
  - context-switching
  - fpu
  - security
  - side-channels
  - simd
aliases:
  - "LazyFP"
---

# LazyFP: Leaking FPU register state using microarchitectural side-channels

## Reference

Julian Stecklina and Thomas Prescher. “LazyFP: Leaking FPU Register State
Using Microarchitectural Side-Channels.” CoRR abs/1806.07480, 2018. DOI
[10.48550/arXiv.1806.07480](https://doi.org/10.48550/arXiv.1806.07480).
Intel's corresponding [security advisory](https://www.intel.com/content/www/us/en/security-center/advisory/intel-sa-00145.html)
was used to check the mitigation guidance.

## Research question or contribution

Can speculative execution expose a previous task's floating-point and SIMD
registers when an OS defers restoring extended state until first use?

## Method

The authors analyze lazy FPU switching and demonstrate recovery of register
state through transient execution and cache side effects on affected Intel
processors.

## Findings

- Lazy restore can leave another protection domain's FPU/SIMD values resident
  and transiently observable after a context switch.
- Intel recommended eager restore for relevant state on affected systems.
- The optimization's benefit depends on workloads not using extended state;
  compilers increasingly use SIMD even for ordinary memory operations, making
  that premise fragile.
- Extended register state is part of the security context, not an optional
  performance attachment once enabled for a domain.

## Relevance

The safe default is eager, ownership-tracked save/restore at kernel protection-
domain switches, with no floating-point or SIMD use in interrupt/trap code.
Managed actors inside one runtime domain need not each own architectural vector
state if the runtime reaches a safe point before actor scheduling.

## Limits

The demonstrated vulnerability is processor- and speculation-specific. Eager
switching does not remove all timing or microarchitectural channels, and future
vector, matrix, or accelerator states require separate inventory.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
