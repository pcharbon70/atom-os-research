---
title: "A least-privilege memory protection model for modern hardware"
kind: source
created: "2026-08-29"
authors:
  - "Reto Achermann"
  - "Nora Hossle"
  - "Lukas Humbel"
  - "Daniel Schwyn"
  - "David Cock"
  - "Timothy Roscoe"
published: 2019
citation_key: "achermann-et-al-2019-least-privilege"
container: "CoRR abs/1908.08707"
edition: null
isbn: null
doi: "10.48550/arXiv.1908.08707"
url: "https://arxiv.org/abs/1908.08707"
accessed: "2026-08-29"
tags:
  - capabilities
  - hardware-heterogeneity
  - iommu
  - memory-protection
  - operating-systems
aliases:
  - "Least-privilege memory protection model"
---

# A least-privilege memory protection model for modern hardware

## Reference

Reto Achermann et al. “A Least-Privilege Memory Protection Model for Modern
Hardware.” CoRR abs/1908.08707, 2019. DOI
[10.48550/arXiv.1908.08707](https://doi.org/10.48550/arXiv.1908.08707).

## Research question or contribution

How can an OS represent authorization when CPUs, IOMMUs, accelerators, secure
cores, and interconnects see different address spaces and independently
configurable translation paths?

## Method

The authors refine a formal model of address-space networks into an executable
capability specification, implement it in Barrelfish, and compare operations
with Linux virtual-memory management.

## Findings

- The familiar single global physical address-space model does not accurately
  describe many SoCs. Devices and heterogeneous cores can reach memory through
  different translation and protection nodes.
- Authority to access memory and authority to configure a translation are
  distinct. Both must be represented to enforce least privilege.
- The model expresses decentralized, partitioned capability authority and was
  implemented with performance comparable in the reported experiments to the
  Linux operations used for comparison.
- Correct CPU page tables alone do not imply system-wide isolation when other
  bus masters or translation units retain access.

## Relevance

The proposed kernel resource graph should model address spaces and
translations explicitly. A memory grant is not complete until CPU mappings,
DMA mappings, device ownership, caches, and in-flight operations agree; revoke
is correspondingly a transaction rather than one page-table write.

## Limits

This is a research model and prototype, not evidence for every SoC or a
complete production driver stack. The performance comparison does not prove
zero cost under all workloads, and the paper predates current IOMMU revisions.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
