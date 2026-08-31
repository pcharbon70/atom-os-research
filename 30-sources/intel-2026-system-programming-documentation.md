---
title: "Intel 64 and IA-32 system programming documentation"
kind: source
created: "2026-08-30"
authors:
  - "Intel Corporation"
published: 2026
citation_key: "intel-2026-system-programming-documentation"
container: "Intel 64 and IA-32 Architectures Software Developer's Manual"
edition: "Combined Volumes, Order Number 325462-092US"
isbn: null
doi: null
url: "https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html"
accessed: "2026-08-30"
tags:
  - cpu-architecture
  - interrupts
  - memory-ordering
  - privilege
  - x86-64
aliases:
  - "Intel SDM system programming volumes"
---

# Intel 64 and IA-32 system programming documentation

## Reference

Intel Corporation. *Intel 64 and IA-32 Architectures Software Developer's
Manual*, Combined Volumes, Order Number 325462-092US, updated 2026-08-19.
[Official manual landing page](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html).

## Research question or contribution

Which x86-64 mechanisms must an architecture-support implementation account
for at privilege, entry, context, translation, interrupt, ordering, time, and
virtualization boundaries?

## Method

The system-programming and instruction-reference portions were used as the
normative architecture source. This note records categories of kernel-visible
mechanism and does not select a board, chipset, or device set.

## Findings

- Protected execution combines privilege levels, control registers, descriptor
  and interrupt tables, system-call entry instructions, task/thread-local
  state, and tightly specified interrupt and exception frames.
- Page-table formats, translation caches, process-context identifiers, and
  invalidation instructions expose both local operations and conditions under
  which broader invalidation or serialization is required.
- The architectural interrupt surface includes exceptions, local interrupt
  controller facilities, inter-processor interrupts, and message-signaled
  interrupts; controller policy remains separate from trap-frame semantics.
- The TSC and deadline-timer facilities can support high-resolution monotonic
  time and one-shot deadlines, subject to discovered invariance,
  synchronization, and virtualization properties.
- XSAVE-family facilities make floating-point, SIMD, protection, and other
  extended state a discoverable, growing execution-context set rather than a
  fixed register block.
- VMX and VT-d add optional second-level translation and device-remapping
  mechanisms. They are candidates for controlled delegation and DMA isolation,
  not requirements of the baseline kernel contract.

## Relevance

The manual demonstrates why a portable facade cannot be an instruction-name
wrapper. The common layer must describe effects such as validated user return,
translation invalidation completion, one-shot deadline programming, or saved
extended context; an x86-64 backend then realizes those effects with the
applicable tables, registers, and serialization rules.

## Limits

This is vendor architecture documentation, not an evaluation of kernel
designs. Some mechanisms are model-, feature-, and firmware-dependent.
Chipset initialization, ACPI parsing, board topology, and device programming
are deliberately outside this note.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
