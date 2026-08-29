---
title: "x86-TSO: A rigorous and usable programmer's model for x86 multiprocessors"
kind: source
created: "2026-08-29"
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
url: "https://www.cl.cam.ac.uk/~mom22/cacm10.pdf"
accessed: "2026-08-29"
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
[Author PDF](https://www.cl.cam.ac.uk/~mom22/cacm10.pdf).

## Research question or contribution

Can x86 multiprocessor behavior be captured by a precise model that matches
hardware and supports practical reasoning about systems code?

## Method

The authors analyze vendor specifications and litmus tests, define an
operational TSO abstract machine in HOL4, and use it to reason about examples
including a Linux spinlock and data-race freedom.

## Findings

- x86 is not sequentially consistent: store buffering permits outcomes that no
  simple interleaving of source-level loads and stores explains.
- TSO is nevertheless stronger than common Arm and RISC-V models and can hide
  missing portable synchronization in code tested only on x86.
- Precise models matter because prose specifications and intuition were
  ambiguous or unsound for concurrent kernel code.
- Device memory and cache/TLB maintenance need their own architectural rules;
  ordinary-memory TSO is not a universal ordering model.

## Relevance

The architecture interface should name acquire, release, full, I/O, TLB, and
instruction-publication operations separately. The kernel's shared protocols
must be designed against the weakest selected target and exercised with litmus
tests, not inferred from successful x86 execution.

## Limits

The paper models the x86 generation and ordinary-memory behavior studied at
the time. It is not a complete current Intel/AMD system specification and does
not cover speculative side channels or every mixed-size operation.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
