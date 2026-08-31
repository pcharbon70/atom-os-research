---
title: "Simplifying ARM concurrency: Multicopy-atomic axiomatic and operational models for ARMv8"
kind: source
created: "2026-08-30"
authors:
  - "Christopher Pulte"
  - "Shaked Flur"
  - "Will Deacon"
  - "Jon French"
  - "Susmit Sarkar"
  - "Peter Sewell"
published: 2018
citation_key: "pulte-et-al-2018-simplifying-arm-concurrency"
container: "Proceedings of the ACM on Programming Languages 2, POPL, Article 19"
edition: null
isbn: null
doi: "10.1145/3158107"
url: "https://www.cl.cam.ac.uk/~pes20/armv8-mca/"
accessed: "2026-08-30"
tags:
  - aarch64
  - concurrency
  - formal-methods
  - memory-models
  - multicore
aliases:
  - "Multicopy-atomic ARMv8 model"
---

# Simplifying ARM concurrency: Multicopy-atomic axiomatic and operational models for ARMv8

## Reference

Christopher Pulte et al. “Simplifying ARM Concurrency: Multicopy-Atomic
Axiomatic and Operational Models for ARMv8.” *Proceedings of the ACM on
Programming Languages* 2, POPL, Article 19, 2018. DOI
[10.1145/3158107](https://doi.org/10.1145/3158107).
[Project page, paper, model, tests, and errata](https://www.cl.cam.ac.uk/~pes20/armv8-mca/).

## Research question or contribution

Can the Armv8 concurrency architecture be simplified to a multicopy-atomic
model while retaining useful hardware flexibility and providing equivalent
operational and axiomatic specifications?

## Method

Academic and Arm authors refine the architecture model, define operational and
axiomatic versions, prove their correspondence on paper, and exercise them
against litmus tests including Linux locking behavior.

## Findings

- Arm's ordinary-memory model is relaxed even after the move to
  multicopy-atomic writes; acquire, release, dependencies, exclusives, and
  barriers still have distinct semantics.
- The architecture specification itself evolved in response to formalization
  and hardware/software discussion, so kernel code must pin an edition and not
  rely on generic “Armv8” folklore.
- Executable models make architectural guarantees testable against small
  concurrent programs.
- The project publishes errata, reinforcing that model version and known
  limitations are part of reproducible evidence.

## Relevance

The common concurrency contract should be expressed in language-level
ordering terms and compiled by each port to the selected architecture profile.
Raw barrier mnemonics should remain inside the port. Architecture-model
versions and litmus suites should be pinned alongside implementation tests.

## Limits

This work focuses on ordinary-memory concurrency. Address translation,
instruction fetch, exceptions, I/O memory, and DMA require additional system
semantics; the equivalence proof itself is not fully mechanized.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
