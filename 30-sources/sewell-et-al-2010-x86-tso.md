---
title: "x86-TSO: A rigorous and usable programmer's model for x86 multiprocessors"
kind: source
created: "2026-08-30"
authors:
  - "Peter Sewell"
  - "Susmit Sarkar"
  - "Scott Owens"
  - "Francesco Zappa Nardelli"
  - "Magnus O. Myreen"
published: 2010
citation_key: "sewell-et-al-2010-x86-tso"
container: "Communications of the ACM 53(7)"
edition: null
isbn: null
doi: "10.1145/1785414.1785443"
url: "https://www.cl.cam.ac.uk/~pes20/weakmemory/cacm.pdf"
accessed: "2026-08-30"
tags:
  - concurrency
  - formal-methods
  - memory-models
  - multicore
  - x86-64
aliases:
  - "x86-TSO"
---

# x86-TSO: A rigorous and usable programmer's model for x86 multiprocessors

## Reference

Peter Sewell et al. “x86-TSO: A Rigorous and Usable Programmer's Model for x86
Multiprocessors.” *Communications of the ACM* 53(7), pages 89–97, July 2010.
DOI [10.1145/1785414.1785443](https://doi.org/10.1145/1785414.1785443).
[Author PDF](https://www.cl.cam.ac.uk/~pes20/weakmemory/cacm.pdf).

## Research question or contribution

Can x86 multiprocessor behavior be captured by a precise model that matches
hardware observations and supports practical reasoning about systems code?

## Method

The authors analyze vendor specifications and litmus tests, define equivalent
operational and axiomatic TSO models in HOL4, and use the model to reason about
a Linux spinlock and data-race freedom.

## Findings

- x86 ordinary memory is not sequentially consistent: store buffering permits
  outcomes that no simple interleaving of source-level loads and stores
  explains.
- TSO is nevertheless stronger than common Arm and RISC-V models and can hide
  missing portable synchronization in code tested only on x86.
- Precise models matter because contemporary prose specifications and
  programmer intuition were ambiguous or unsound for concurrent kernel code.
- The model explicitly excludes exceptions, page-table changes,
  self-modifying code, non-temporal operations, and several access forms. Device
  ordering, TLB maintenance, and instruction publication require other rules.

## Relevance

The common layer should specify source-language atomics and named CPU, I/O,
translation, and instruction-publication barriers separately. Shared protocols
should be validated against the weakest supported architecture rather than
assuming successful x86 tests demonstrate portability.

## Limits

The work captures a carefully stated subset and hardware generation, not the
complete current Intel or AMD architecture, compiler memory model, speculative
side channels, or mixed-size and device behavior.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
