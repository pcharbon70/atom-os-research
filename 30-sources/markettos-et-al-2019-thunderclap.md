---
title: "Thunderclap: Exploring vulnerabilities in operating system IOMMU protection via DMA from untrustworthy peripherals"
kind: source
created: "2026-08-30"
authors:
  - "A. Theodore Markettos"
  - "Colin Rothwell"
  - "Brett F. Gutstein"
  - "Allison Pearce"
  - "Peter G. Neumann"
  - "Simon W. Moore"
  - "Robert N. M. Watson"
published: 2019
citation_key: "markettos-et-al-2019-thunderclap"
container: "Network and Distributed System Security Symposium 2019"
edition: null
isbn: "1-891562-55-X"
doi: "10.14722/ndss.2019.23194"
url: "https://thunderclap.io/wp-content/uploads/2024/01/thunderclap-paper-ndss2019.pdf"
accessed: "2026-08-30"
tags:
  - dma
  - iommu
  - operating-systems
  - security
  - threat-modeling
aliases:
  - "Thunderclap"
---

# Thunderclap: Exploring vulnerabilities in operating system IOMMU protection via DMA from untrustworthy peripherals

## Reference

A. Theodore Markettos et al. “Thunderclap: Exploring Vulnerabilities in
Operating System IOMMU Protection via DMA from Untrustworthy Peripherals.”
*NDSS 2019*. DOI [10.14722/ndss.2019.23194](https://doi.org/10.14722/ndss.2019.23194).
[Project PDF](https://thunderclap.io/wp-content/uploads/2024/01/thunderclap-paper-ndss2019.pdf).

## Research question or contribution

Do operating systems that enable an IOMMU actually contain a functional but
malicious peripheral throughout realistic driver interactions and shared DMA
buffers?

## Method

The authors built a programmable malicious-peripheral platform, examined
macOS, FreeBSD, Linux, and Windows, and exercised excessive mappings, spatial
and temporal exposure, and trusted shared-memory protocols.

## Findings

- IOMMU presence or nominal enablement does not establish DMA isolation. The
  operating system must constrain each mapping and every transition in its
  lifetime.
- A device can exploit intentionally shared descriptor and payload memory
  without violating address translation. The DMA interface is a bidirectional,
  concurrent security protocol comparable in importance to a system-call
  interface.
- Broad mappings, sub-page sharing, delayed unmapping, allocator reuse, device
  reset, and early enablement create spatial or temporal exposure.
- Stronger isolation can increase mapping and invalidation costs; the security
  and performance policy must be explicit rather than silently bypassing the
  IOMMU.

## Relevance

The protected-I/O layer should begin DMA-denied, map only charged buffers for a
bounded operation, separate control from data, quiesce and invalidate before
reuse, scrub returned memory where required, and quarantine a device after
protocol or reset failure. IOMMU programming alone is not a completed
ownership transition.

## Limits

The tested OS releases and hardware are historical, and the platform does not
model every coherent interconnect or device. The paper does not imply that all
IOMMU implementations fail; it shows why OS lifecycle and shared-memory
semantics determine the protection actually achieved.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
