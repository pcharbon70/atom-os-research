---
title: "CertiKOS: An extensible architecture for building certified concurrent OS kernels"
kind: source
created: "2026-08-30"
authors:
  - "Ronghui Gu"
  - "Zhong Shao"
  - "Hao Chen"
  - "Xiongnan Wu"
  - "Jieung Kim"
  - "Vilhelm Sjöberg"
  - "David Costanzo"
published: 2016
citation_key: "gu-et-al-2016-certikos"
container: "12th USENIX Symposium on Operating Systems Design and Implementation"
edition: null
isbn: "978-1-931971-33-1"
doi: null
url: "https://www.usenix.org/conference/osdi16/technical-sessions/presentation/gu"
accessed: "2026-08-30"
tags:
  - abstraction-layers
  - concurrency
  - formal-verification
  - operating-systems
  - specifications
aliases:
  - "CertiKOS"
---

# CertiKOS: An extensible architecture for building certified concurrent OS kernels

## Reference

Ronghui Gu et al. “CertiKOS: An Extensible Architecture for Building Certified
Concurrent OS Kernels.” *OSDI '16*, pages 653–669, 2016.
[USENIX paper and metadata](https://www.usenix.org/conference/osdi16/technical-sessions/presentation/gu).

## Research question or contribution

Can a practical concurrent kernel be decomposed into certified abstraction
layers whose behavior remains correct under valid CPU, thread, user, and I/O
interleavings?

## Method

The authors specify observable events at successive abstraction levels, prove
contextual refinement for kernel functions, construct per-CPU and per-thread
logical machines, and verify a 6,500-line C and x86-assembly kernel with
fine-grained locking.

## Findings

- A useful layer is defined by its observable state and events, not merely by
  grouping source files. Each implementation layer must refine the contract
  above under the interference allowed below.
- Per-CPU private state can be reasoned about separately from synchronized
  shared objects when rely conditions and composition rules are explicit.
- Concurrency includes user transitions, I/O interrupts, and multicore
  execution; treating only one category leaves important interference outside
  the model.
- The authors identify important proof boundaries: their machine model did not
  model TLB behavior, so TLB-shootdown code was outside the verified claim;
  boot and device initialization were also assumptions. This is a concrete
  warning against overclaiming from a verified subset.

## Relevance

Each proposed hardware-support component should publish an observable contract
and interference model. CPU-local primitives, cross-CPU transitions, and
device-driven events need different specifications. Verification and testing
claims must enumerate omitted hardware behavior, especially translation
caches, boot state, DMA, and interrupt nesting.

## Limits

CertiKOS targets a modeled x86 subset and relies on a trusted tool and hardware
base. Its proof architecture is evidence for decomposition and claim hygiene,
not a proof of this project's proposed interfaces.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
