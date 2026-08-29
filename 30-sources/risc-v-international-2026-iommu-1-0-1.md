---
title: "RISC-V IOMMU Architecture Specification 1.0.1"
kind: source
created: "2026-08-29"
authors:
  - "RISC-V International"
published: 2026
citation_key: "risc-v-international-2026-iommu-1-0-1"
container: "RISC-V IOMMU Architecture Specification"
edition: "Version 1.0.1, revised 2026-02-22"
isbn: null
doi: null
url: "https://docs.riscv.org/reference/iommu/index.html"
accessed: "2026-08-29"
tags:
  - capabilities
  - dma
  - iommu
  - operating-systems
  - risc-v
aliases:
  - "RISC-V IOMMU 1.0.1"
---

# RISC-V IOMMU Architecture Specification 1.0.1

## Reference

RISC-V International. *RISC-V IOMMU Architecture Specification*, version
1.0.1, revised 22 February 2026. [Official HTML](https://docs.riscv.org/reference/iommu/index.html)
and [official PDF](https://docs.riscv.org/reference/hardware/iommu/_attachments/riscv-iommu.pdf).
Accessed 2026-08-29.

## Research question or contribution

What hardware mechanisms can confine device-initiated memory access and MSI
delivery, and what software lifecycle remains necessary around those
mechanisms?

## Method

The reading covered device contexts, process identifiers, single- and
two-stage translation, CPU-compatible page formats, command and fault queues,
translation invalidation, PCIe ATS/PRI, MSI address translation, bare/off
modes, and software update guidance.

## Findings

- The IOMMU selects a context per device and can perform one or two translation
  stages. This supports host isolation, shared virtual addressing, and virtual
  machine assignment without making those policies automatic.
- Translation caches and in-flight DMA make mapping changes asynchronous.
  Safe revoke requires quiescing submission, invalidating translations,
  waiting for completion, draining faults and interrupts, and only then
  recycling memory or device identity.
- `Bare` pass-through and `Off` are materially different security states. The
  kernel must choose a deny-by-default reset and assignment sequence.
- MSI translation couples the IOMMU to interrupt routing. Treating DMA and IRQ
  ownership as independent grants can leave an incomplete revocation boundary.

## Relevance

The specification supports an explicit DMA-domain component with
`map/publish/sync/unmap/revoke` transactions and generation-tagged ownership.
QEMU's RISC-V `virt` platform can expose a conforming reference device, making
this testable before physical hardware is selected.

## Limits

An IOMMU constrains addresses, not device protocol, bandwidth, interrupt rate,
firmware, or the safety of intentionally shared buffers. Hardware topology can
also group devices more coarsely than the software wants.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
