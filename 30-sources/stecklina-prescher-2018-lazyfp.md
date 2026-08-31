---
title: "LazyFP: Leaking FPU register state using microarchitectural side-channels"
kind: source
created: "2026-08-30"
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
accessed: "2026-08-30"
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

## Research question or contribution

Can speculative execution expose a previous protection domain's floating-point
and SIMD registers when an OS defers restoring extended state until first use?

## Method

The authors analyze lazy FPU switching and demonstrate reconstruction of
register contents through transient execution and cache side effects on
affected processors.

## Findings

- Lazy restore deliberately leaves previous-domain FPU and SIMD values in the
  architectural register file and relies on a fault before ordinary use.
- On affected processors, transient execution can pass that fault and encode
  the stale values in cache state, breaking the intended isolation.
- The optimization assumes many tasks avoid extended state. Modern compilers
  increasingly use SIMD for ordinary work, making that premise less reliable.
- Once a domain may use it, extended register state is security context, not an
  optional scheduler attachment.

## Relevance

The initial context component should eagerly save and restore all enabled
cross-domain state, use explicit per-CPU ownership, keep FPU/vector use out of
trap code, and refuse features whose state size or save protocol is unknown.
Lazy switching should require later target-specific evidence and a threat-model
review, not be the default optimization.

## Limits

The demonstrated leak depends on particular speculative behavior. Eager
switching does not solve every timing or microarchitectural channel, and newer
vector, matrix, debug, and accelerator state needs separate inventory.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
