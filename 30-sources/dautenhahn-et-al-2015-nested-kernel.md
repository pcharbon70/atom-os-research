---
title: "Nested Kernel: An operating system architecture for intra-kernel privilege separation"
kind: source
created: "2026-09-04"
authors:
  - "Nathan Dautenhahn"
  - "Theodoros Kasampalis"
  - "Will Dietz"
  - "John Criswell"
  - "Vikram Adve"
published: 2015
citation_key: "dautenhahn-et-al-2015-nested-kernel"
container: "20th International Conference on Architectural Support for Programming Languages and Operating Systems"
edition: null
isbn: "978-1-4503-2835-7"
doi: "10.1145/2694344.2694386"
url: "https://doi.org/10.1145/2694344.2694386"
accessed: "2026-09-04"
tags:
  - intra-kernel-isolation
  - memory-protection
  - operating-systems
  - reference-monitor
  - virtual-memory
aliases:
  - "Nested Kernel"
  - "PerspicuOS"
---

# Nested Kernel: An operating system architecture for intra-kernel privilege separation

## Reference

Nathan Dautenhahn, Theodoros Kasampalis, Will Dietz, John Criswell, and Vikram
Adve. “Nested Kernel: An Operating System Architecture for Intra-Kernel
Privilege Separation.” *ASPLOS 2015*, pages 191–206. DOI
[10.1145/2694344.2694386](https://doi.org/10.1145/2694344.2694386).
[Author-hosted paper](https://nathandautenhahn.com/downloads/publications/asplos200-dautenhahn.pdf).

## Research question or contribution

Can a small protected core mediate every physical-MMU update even when the rest
of a monolithic kernel still executes at the highest hardware privilege level?

## Method

The authors build PerspicuOS from FreeBSD 9.0 on x86-64. The nested kernel
write-protects page-table pages through every outer-kernel mapping, controls
the MMU mechanisms that can disable protection, exposes a virtual-MMU update
interface, implements several intra-kernel policies, and evaluates overhead.

## Findings

- Complete mediation of MMU state requires protecting both page-table storage
  and control-register paths that could disable its protection.
- Declaring and typing page-table pages before use lets the protected core
  reject arbitrary memory as a translation structure.
- A narrow virtual-MMU interface can leave higher VM policy outside the small
  protected component while retaining authority over final activation.
- The prototype reports less than 1% average overhead for Apache and 2.7% for
  kernel compilation in its evaluated configuration.

## Relevance

This is direct evidence for making the page-table encoder a completely
mediated boundary and for preventing ordinary mappings of translation-
structure pages. Atom can achieve a smaller TCB through its microkernel
structure rather than the paper's same-ring nesting, but must still enumerate
boot, fault, recovery, and diagnostic mutation paths.

## Limits

The prototype is FreeBSD/x86-64-specific, primarily uniprocessor in scope, and
does not fully cover DMA, SMI, or every execute-protection case. Its measured
overheads do not establish the cost of Atom's capability and multicore
transaction protocols.

## Derived work

- [Page-table and protection encoder](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/page-table-and-protection-encoder.md)
- [Mapping validator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/mapping-validator.md)
