---
title: "Secure Virtual Architecture: A safe execution environment for commodity operating systems"
kind: source
created: "2026-09-02"
authors:
  - "John Criswell"
  - "Andrew Lenharth"
  - "Dinakar Dhurjati"
  - "Vikram Adve"
published: 2007
citation_key: "criswell-et-al-2007-secure-virtual-architecture"
container: "Proceedings of the 21st ACM Symposium on Operating Systems Principles"
edition: null
isbn: "978-1-59593-591-5"
doi: "10.1145/1294261.1294295"
url: "https://llvm.org/pubs/2007-SOSP-SVA.pdf"
accessed: "2026-09-02"
tags:
  - interfaces
  - operating-systems
  - privilege
  - type-safety
  - virtual-machines
aliases:
  - "Secure Virtual Architecture"
  - "SVA"
---

# Secure Virtual Architecture: A safe execution environment for commodity operating systems

## Reference

John Criswell, Andrew Lenharth, Dinakar Dhurjati, and Vikram Adve. “Secure
Virtual Architecture: A Safe Execution Environment for Commodity Operating
Systems.” *SOSP '07*, pages 351–366. DOI
[10.1145/1294261.1294295](https://doi.org/10.1145/1294261.1294295).
[Author-hosted paper](https://llvm.org/pubs/2007-SOSP-SVA.pdf).

## Research question or contribution

Can a typed low-level virtual architecture mediate privileged operations and
enforce useful safety properties while requiring limited changes to an
existing commodity kernel?

## Method

SVA defines a typed virtual instruction set and a set of OS operations that
encapsulate privileged hardware instructions. A checker keeps the complex
compiler outside the trusted base. The authors port Linux as though SVA were a
new architecture, examine source changes and overhead, and test known memory-
safety exploits.

## Findings

- Privileged operations can be concentrated behind a small virtual-
  architecture interface while most machine-independent kernel code remains
  unchanged.
- Typed low-level representations can enforce properties beyond a C function
  signature, including aspects of memory safety and control-flow integrity.
- The reported Linux port changed fewer than 300 lines of machine-independent
  kernel and driver code, demonstrating that an architecture boundary can be
  both semantically meaningful and narrow for that system.
- SVA prevented four of five evaluated Linux 2.4.22 memory-safety exploits;
  compiling one additional library would have covered the fifth.
- The virtual architecture and verifier remain trusted mechanisms, and a safe
  call surface cannot validate the higher-level correctness of an operation.

## Relevance

Atom OS should make all unsafe privileged instructions reachable only through
the architecture capsule and expose typed semantic operations above it. The
facade can use language types, sealed constructors, capability authority, and
generational tokens without turning BEAM into the kernel instruction set or
adopting SVA's compiler virtual machine.

## Limits

SVA targets a commodity Linux port and an older exploit set. Its goals and TCB
differ from this project's capability microkernel, and type safety alone does
not prove concurrency protocols, temporal bounds, DMA quiescence, or hardware
correctness.

## Derived work

- [Typed kernel-facing architecture facade](../20-notes/kernel-hardware-and-architecture-components/typed-kernel-facing-architecture-facade.md)
- [Unsafe architecture-primitives capsule](../20-notes/kernel-hardware-and-architecture-components/unsafe-architecture-primitives-capsule.md)
