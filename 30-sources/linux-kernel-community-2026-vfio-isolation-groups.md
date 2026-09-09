---
title: "VFIO - Virtual Function I/O"
kind: source
created: "2026-09-08"
authors:
  - "Linux kernel development community"
published: null
citation_key: "linux-kernel-community-2026-vfio-isolation-groups"
container: "The Linux Kernel documentation"
edition: null
isbn: null
doi: null
url: "https://docs.kernel.org/driver-api/vfio.html"
accessed: "2026-09-08"
tags:
  - architecture-support
  - kernel-architecture
aliases: []
---

# VFIO - Virtual Function I/O

## Reference

Linux kernel development community. [VFIO - Virtual Function I/O](https://docs.kernel.org/driver-api/vfio.html). The Linux Kernel documentation; publication date not stated. Accessed 2026-09-08.

## Research question or contribution

How device assignment reflects actual DMA isolation boundaries.

## Method

Official VFIO documentation; reviewed the IOMMU-group rationale and device, group and container relationships.

## Findings

Bridges, requester aliasing and peer-to-peer paths can make the isolation unit larger than one apparent device function. Software grouping reflects restrictions that handles alone cannot eliminate.

## Relevance

Represent requester, endpoint, interrupt and reset scopes separately and require evidence before granting independent authority.

## Limits

An IOMMU group is not automatically a reset domain. The documentation does not verify any particular laboratory machine or establish that every platform routes every DMA path through protection.

## Derived work

- [Requester and endpoint scope binding](../20-notes/kernel-hardware-and-architecture-components/protected-io-and-dma-ownership/requester-endpoint-scope-binding.md) — architecture synthesis constrained by this source.
- [Reset-domain and recovery authority](../20-notes/kernel-hardware-and-architecture-components/protected-io-and-dma-ownership/reset-domain-and-recovery-authority.md) — architecture synthesis constrained by this source.
