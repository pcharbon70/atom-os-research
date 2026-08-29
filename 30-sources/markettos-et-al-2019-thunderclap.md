---
title: "Thunderclap: Exploring vulnerabilities in operating system IOMMU protection via DMA from untrustworthy peripherals"
kind: source
created: "2026-08-29"
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
isbn: null
doi: "10.14722/ndss.2019.23194"
url: "https://thunderclap.io/wp-content/uploads/2024/01/thunderclap-paper-ndss2019.pdf"
accessed: "2026-08-29"
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

The authors built an FPGA-based malicious peripheral platform, exercised
macOS, FreeBSD, Linux, and Windows, and developed attacks through excessive or
incorrect mappings and trusted shared-memory protocols.

## Findings

- Presence or nominal use of an IOMMU does not establish DMA isolation. Broad
  identity mappings, delayed enablement, permissive shared buffers, and driver
  protocol assumptions can restore a useful attack surface.
- A device can exploit intentionally shared communication memory without
  violating the IOMMU's address checks.
- Boot-time DMA, hot-plug, device reset, and transition windows are part of the
  security lifecycle, not exceptional setup details.
- The work led to mitigations, but its central lesson is architectural: the
  IOMMU must be integrated with least-privilege buffer and device ownership.

## Relevance

The project should start DMA-denied, map only descriptor and payload regions
needed for a bounded operation, separate control from data, scrub returned
buffers, and make assignment/revocation a state machine with audit evidence.

## Limits

The tested OS versions and interfaces are historical. The work does not imply
that all IOMMU designs are broken, nor does an FPGA peripheral model every
device or coherent interconnect.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
