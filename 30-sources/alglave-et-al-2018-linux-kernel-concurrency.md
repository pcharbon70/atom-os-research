---
title: "Frightening small children and disconcerting grown-ups: Concurrency in the Linux kernel"
kind: source
created: "2026-09-02"
authors:
  - "Jade Alglave"
  - "Luc Maranget"
  - "Paul E. McKenney"
  - "Andrea Parri"
  - "Alan Stern"
published: 2018
citation_key: "alglave-et-al-2018-linux-kernel-concurrency"
container: "Proceedings of the 23rd ACM International Conference on Architectural Support for Programming Languages and Operating Systems"
edition: null
isbn: "978-1-4503-4911-6"
doi: "10.1145/3173162.3177156"
url: "https://discovery.ucl.ac.uk/id/eprint/10070727/"
accessed: "2026-09-02"
tags:
  - concurrency
  - formal-methods
  - linux
  - memory-models
  - operating-systems
aliases:
  - "The Linux kernel memory-model paper"
---

# Frightening small children and disconcerting grown-ups: Concurrency in the Linux kernel

## Reference

Jade Alglave et al. “Frightening Small Children and Disconcerting Grown-ups:
Concurrency in the Linux Kernel.” *ASPLOS '18*, pages 405–418, 2018. DOI
[10.1145/3173162.3177156](https://doi.org/10.1145/3173162.3177156).
[Author-accepted manuscript](https://discovery.ucl.ac.uk/id/eprint/10070727/).

## Research question or contribution

Can a portable kernel concurrency contract be expressed as a formal,
executable model and checked against both architecture behavior and real
kernel idioms?

## Method

The authors define an executable `cat` model for Linux-kernel concurrency,
test it with litmus programs and hardware, refine it with maintainers, and
formalize a fundamental RCU law and one implementation.

## Findings

- Portable systems code needs an explicit software memory model in addition
  to each ISA model; prose intuition and testing on one strong architecture
  are insufficient.
- Executable litmus tests let developers compare a protocol against the model
  and selected hardware outcomes.
- The evaluated model covers central ordinary-memory synchronization idioms
  but explicitly excludes compiler optimization, mixed-size structures,
  dynamic allocation, exceptions, interrupts, self-modifying code, and I/O.
- Formalizing RCU within the model demonstrates value for retirement and
  quiescence protocols, while the exclusions show why it cannot justify cache,
  device, translation, or executable-publication claims.

## Relevance

The kernel should publish a small, executable memory-model contract for its
atomics and locks, maintain litmus tests beside protocol code, and keep MMIO,
DMA, page-table, interrupt, and code-publication operations in separately
specified semantic APIs.

## Limits

This work models Linux rather than this kernel and deliberately excludes
several mechanisms central to the architecture layer. Copying Linux primitive
names would not transfer its model or proofs; the implementation language and
compiler mappings must also be pinned.

## Derived work

- [Ordering, coherence, and code publication](../20-notes/ordering-coherence-and-code-publication.md)
