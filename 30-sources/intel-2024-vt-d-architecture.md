---
title: "Intel Virtualization Technology for Directed I/O architecture specification"
kind: source
created: "2026-09-02"
authors:
  - "Intel Corporation"
published: "2024-08"
citation_key: "intel-2024-vt-d-5-0"
container: "Intel architecture specification"
edition: "Revision 5.0, Order Number D51397-017"
isbn: null
doi: null
url: "https://www.intel.com/content/www/us/en/content-details/919688/intel-virtualization-technology-for-directed-i-o-architecture-specification.html"
accessed: "2026-09-02"
tags:
  - dma
  - interrupts
  - iommu
  - virtualization
  - x86-64
aliases:
  - "Intel VT-d 5.0"
---

# Intel Virtualization Technology for Directed I/O architecture specification

## Reference

Intel Corporation. *Intel Virtualization Technology for Directed I/O
Architecture Specification*, revision 5.0, Order Number D51397-017, August
2024. [Official specification](https://www.intel.com/content/www/us/en/content-details/919688/intel-virtualization-technology-for-directed-i-o-architecture-specification.html).

## Research question or contribution

Which x86 platform mechanisms constrain device DMA and remap device-generated
interrupts, and what ordered invalidation/completion protocol must software
follow when contexts or translations change?

## Method

This is a normative architecture specification. The analysis focuses on
requester identity, DMA-remapping tables, interrupt remapping, PASID/ATS-capable
devices, queued invalidation, and invalidation-wait semantics.

## Findings

- Remapping hardware selects contexts from device source identity and can
  enforce translated access permissions. Interrupt-remapping tables provide a
  separate control plane for device-generated interrupts.
- Context, PASID, IOTLB, interrupt-entry, and device-TLB caches require
  appropriately scoped invalidation when their backing structures or ownership
  change.
- The queued-invalidation interface orders dependent invalidations. A wait
  descriptor reports completion only after the relevant earlier descriptors
  complete; its fence option constrains later descriptors as well.
- Device-TLB invalidation follows IOTLB and interrupt-cache invalidations ahead
  of it in the queue. A device-TLB timeout prevents completion of pending wait
  descriptors.
- ATS/PASID and translated requests add device-side cached state and more
  invalidation scopes. They are not transparent performance switches.
- Hardware feature discovery and platform scope remain necessary: a CPU family
  name does not prove that every requester and interrupt path is remapped.

## Relevance

The x86-64 backend should expose a completed invalidation epoch only after the
ordered queued-invalidation and wait sequence succeeds for every relevant
cache. Interrupt remapping is part of a delegatable device endpoint, not an
automatic consequence of DMA remapping. The initial profile should keep ATS
and PASID disabled until timeout and reset behavior is verified.

## Limits

VT-d is a platform architecture, not proof that firmware describes remapping
units correctly, PCIe routing preserves requester identity, devices obey ATS,
or every DMA path is covered. The specification does not validate a driver's
descriptor protocol or show that function reset has drained external effects.

## Derived work

- [Protected I/O and DMA ownership](../20-notes/protected-io-and-dma-ownership.md)
