---
title: "Translation validation for a verified OS kernel"
kind: source
created: "2026-09-02"
authors:
  - "Thomas Arthur Leck Sewell"
  - "Magnus O. Myreen"
  - "Gerwin Klein"
published: 2013
citation_key: "sewell-et-al-2013-translation-validation"
container: "Proceedings of the 34th ACM SIGPLAN Conference on Programming Language Design and Implementation"
edition: null
isbn: "978-1-4503-2014-6"
doi: "10.1145/2499370.2462183"
url: "https://www.cl.cam.ac.uk/~mom22/pldi13.pdf"
accessed: "2026-09-02"
tags:
  - assembly
  - compilers
  - formal-verification
  - microkernels
aliases:
  - "seL4 translation validation"
---

# Translation validation for a verified OS kernel

## Reference

Thomas Arthur Leck Sewell, Magnus O. Myreen, and Gerwin Klein. “Translation
Validation for a Verified OS Kernel.” *PLDI '13*, pages 471–482, 2013. DOI
[10.1145/2499370.2462183](https://doi.org/10.1145/2499370.2462183).
[Open author PDF](https://www.cl.cam.ac.uk/~mom22/pldi13.pdf).

## Research question or contribution

Can source-level functional-correctness properties for seL4 be extended to the
optimized linked binary without trusting the compiler to preserve them?

## Method

The work validates refinement between formal C semantics and the generated ARM
binary for the functions in the existing seL4 verification, including linking
and selected compiler optimizations.

## Findings

- Translation validation connected the verified C implementation to its binary
  and removed the compiler from that part of the trusted computing base.
- The technique validates the concrete compiled artifact rather than proving a
  general compiler correct for every input program.
- At the reported boundary, assembly routines and volatile hardware accesses
  were explicitly omitted. They remain separate trusted or separately proved
  obligations.
- Binary verification depends on instruction semantics, binary analysis, and a
  stable correspondence with the source-level model.

## Relevance

Generated-code inspection is necessary but not equivalent to verification.
This work argues for treating assembly and hardware-register primitives as an
explicit residual boundary, emitting a reproducible disassembly artifact, and
eventually proving or validating that small boundary separately.

## Limits

The evaluated configuration is historical and architecture-specific. The
paper does not validate device behavior, caches, DMA, firmware, or modern
speculative effects, and its proof does not transfer to this project.

## Derived work

- [Unsafe architecture-primitives capsule](../20-notes/unsafe-architecture-primitives-capsule.md)
