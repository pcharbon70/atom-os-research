---
title: "A least-privilege memory protection model for modern hardware"
kind: source
created: "2026-08-30"
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
accessed: "2026-08-30"
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

How can an OS represent authority when CPUs, IOMMUs, accelerators, and other
translation nodes see different address spaces and can independently configure
paths through them?

## Method

The authors refine a formal address-space-network model into an executable
capability specification, implement it in Barrelfish, and compare selected
operations with Linux virtual-memory management.

## Findings

- A single global physical-address-space abstraction does not accurately model
  many modern systems. Different initiators can reach memory through different
  translation and protection paths.
- Authority to access memory and authority to configure a translation are
  distinct and both must be represented for least privilege.
- The implementation expresses decentralized, partitioned capability authority
  and reports comparable performance for the evaluated operations.
- Correct CPU page tables do not establish system-wide isolation if an IOMMU,
  device, or other translation node retains a path to the memory.

## Relevance

The translation component should represent CPU and DMA address spaces as typed
objects connected by authorized mappings, not pass raw physical addresses as
ambient authority. Revocation must close every relevant translation path and
wait for cached or in-flight use before declaring memory reusable.

## Limits

This is a research model and prototype, not evidence for every architecture or
a complete production driver stack. The comparison covers selected operations
and predates current architecture revisions.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
