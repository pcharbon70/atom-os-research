---
title: "Design of Tock kernel hardware interface layers"
kind: source
created: "2026-09-02"
authors:
  - "Brad Campbell"
  - "Philip Levis"
  - "Hudson Ayers"
published: null
citation_key: "tock-project-2026-hil-design"
container: "Tock Technical Reference Document 3"
edition: "Final best-current-practice document accessed 2026-09-02"
isbn: null
doi: null
url: "https://github.com/tock/tock/blob/master/doc/reference/trd3-hil-design.md"
accessed: "2026-09-02"
tags:
  - asynchronous-interfaces
  - embedded-systems
  - interfaces
  - ownership
  - type-safety
aliases:
  - "Tock HIL design"
---

# Design of Tock kernel hardware interface layers

## Reference

Brad Campbell, Philip Levis, and Hudson Ayers. [*Design of Kernel Hardware
Interface Layers (HILs)*](https://github.com/tock/tock/blob/master/doc/reference/trd3-hil-design.md),
Tock TRD 3, final best current practice, accessed 2026-09-02.

## Research question or contribution

Which interface rules let typed hardware services support asynchronous devices,
virtualization, buffer ownership, and multiple implementations without hiding
completion or error behavior?

## Method

The technical reference distills rules used by Tock's Rust HIL traits. It is a
maintainer design document rather than a controlled experiment; its examples
and rules were compared with this archive's explicit completion and ownership
requirements.

## Findings

- Hardware interfaces should generally be nonblocking and split-phase so they
  remain implementable over devices and multiplexers that cannot complete
  immediately.
- Submission success means a completion callback will occur. A failure other
  than `BUSY` means no callback will occur for that attempt; `BUSY` starts no
  new operation, but the callback for a previously accepted operation may
  still be pending. The caller therefore needs an operation generation to
  distinguish attempts.
- Completion returns both an explicit result and any transferred buffer, making
  error and resource ownership observable together.
- Synchronous callbacks are forbidden because they create reentrancy and stack
  assumptions that differ between hardware and virtual implementations.
- Fine-grained traits and separated control/data paths support virtualization
  and avoid forcing unrelated clients to receive excess authority.
- The document treats exceptional deviations as interface-wide obligations,
  not conveniences for one implementation.

## Relevance

These rules strongly support typed operation tokens, explicit acceptance,
returned ownership, and split control/data facets in the kernel-facing
architecture facade. Exactly-once terminal completion is this archive's
stronger synthesis, not a claim made by the Tock document. Atom OS should use
bounded event queues rather than callback stacks, but the acceptance and
ownership lessons transfer.

## Limits

Tock targets microcontrollers and uses cooperative in-kernel capsules. Its HILs
do not supply this project's capability authority, multicore completion,
generation fencing, crash isolation, or DMA revocation semantics. The mutable
upstream document can change after the access date.

## Derived work

- [Typed kernel-facing architecture facade](../20-notes/kernel-hardware-and-architecture-components/typed-kernel-facing-architecture-facade.md)
- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
