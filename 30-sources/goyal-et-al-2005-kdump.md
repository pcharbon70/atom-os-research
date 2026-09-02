---
title: "Kdump: A kexec-based kernel crash dumping mechanism"
kind: source
created: "2026-09-02"
authors:
  - "Vivek Goyal"
  - "Eric W. Biederman"
  - "Hariprasad Nellitheertha"
published: 2005
citation_key: "goyal-et-al-2005-kdump"
container: "Proceedings of the Ottawa Linux Symposium 2005"
edition: null
isbn: null
doi: null
url: "https://www.kernel.org/doc/ols/2005/ols2005v1-pages-177-188.pdf"
accessed: "2026-09-02"
tags:
  - crash-dumps
  - diagnostics
  - fault-containment
  - operating-systems
aliases:
  - "Kdump paper"
---

# Kdump: A kexec-based kernel crash dumping mechanism

## Reference

Vivek Goyal, Eric W. Biederman, and Hariprasad Nellitheertha. “Kdump, A
Kexec-based Kernel Crash Dumping Mechanism.” *Proceedings of the Ottawa Linux
Symposium 2005*, volume 1, pages 169–180.
[Full paper](https://www.kernel.org/doc/ols/2005/ols2005v1-pages-177-188.pdf).

## Research question or contribution

Can crash capture rely on a separately prepared execution environment rather
than continuing to use the failed kernel's allocator, drivers, and complex
subsystems?

## Method

The paper describes the kexec/kdump design and implementation: reserve memory
while the first kernel is healthy, preserve processor and physical-memory
metadata, enter a small capture kernel after a crash, and export the old memory
through standard ELF core structures.

## Findings

- The capture kernel and metadata are loaded into reserved memory before the
  failure, reducing dependence on allocation and ordinary kernel state during
  the crash path.
- Processor notes, valid physical-memory ranges, and any relocated backup
  regions are described in prebuilt ELF headers. Standard representation lets
  analysis tools evolve independently of the crashing kernel.
- The capture environment can differ in version from the failed kernel, which
  separates evidence preservation from interpretation.
- Architecture-specific fixed memory, startup state, and device behavior still
  matter. A second kernel can overwrite evidence or be corrupted by outstanding
  DMA unless reservation and handoff rules cover those effects.
- The design improves the independence of bulk capture but does not make entry
  into the crash environment certain after arbitrary hardware or firmware
  failure.

## Relevance

Atom OS should prepare a small crash sink and its memory, entry state, and
metadata layout during healthy boot. The immediate fatal path should only seal
bounded CPU-local records and transfer to that prepared environment. Bulk
memory collection, compression, storage, and symbolization belong outside the
damaged kernel instance.

## Limits

The implementation and evaluation are historical and Linux-specific. Kdump
assumes enough CPU, memory, and platform state survives to enter another
kernel. It is not a containment proof, and it does not solve confidentiality,
malicious-device DMA, recursive faults, or corrupted firmware.

## Derived work

- [Architecture faults and diagnostics](../20-notes/architecture-faults-and-diagnostics.md)
- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
