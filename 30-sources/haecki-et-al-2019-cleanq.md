---
title: "CleanQ: A lightweight, uniform, formally specified interface for intra-machine data transfer"
kind: source
created: "2026-08-30"
authors:
  - "Roni Haecki"
  - "Lukas Humbel"
  - "Reto Achermann"
  - "David Cock"
  - "Daniel Schwyn"
  - "Timothy Roscoe"
published: 2019
citation_key: "haecki-et-al-2019-cleanq"
container: "CoRR abs/1911.08773"
edition: null
isbn: null
doi: "10.48550/arXiv.1911.08773"
url: "https://arxiv.org/abs/1911.08773"
accessed: "2026-08-30"
tags:
  - dma
  - formal-methods
  - io
  - operating-systems
  - ownership
  - queues
aliases:
  - "CleanQ"
---

# CleanQ: A lightweight, uniform, formally specified interface for intra-machine data transfer

## Reference

Roni Haecki et al. “CleanQ: A Lightweight, Uniform, Formally Specified
Interface for Intra-Machine Data Transfer.” CoRR abs/1911.08773, 2019. DOI
[10.48550/arXiv.1911.08773](https://doi.org/10.48550/arXiv.1911.08773).

## Research question or contribution

Can descriptor-ring interfaces for devices, processes, and virtual machines be
reduced to a precise ownership-transfer contract without losing performance?

## Method

The work defines and verifies queue semantics, implements composable C
interfaces for several transfer mechanisms, and compares operation and
end-to-end costs with Virtio and DPDK paths.

## Findings

- Descriptor rings are ownership protocols over memory regions, not merely
  circular arrays. Enqueue and dequeue change which endpoint may access each
  region and under what obligation.
- A uniform contract can hide weak-memory and non-coherent implementation
  details from clients while requiring each backend to implement them
  correctly.
- The paper reports operation overhead in the tens of cycles and comparable
  tested end-to-end performance, showing that a precise interface need not be
  heavyweight.
- Queue creation, authentication, quota, reset, and device control are outside
  the data-transfer contract and must be supplied by surrounding components.

## Relevance

DMA and cross-domain queues should share an explicit ownership vocabulary such
as `owned`, `offered`, `in-flight`, `returned`, and `quarantined`. Cache
maintenance and barriers belong in the backend, while the facade must state
when ownership has actually transferred and when memory may be reused.

## Limits

CleanQ is a research implementation and formal model, not verification of
arbitrary devices or this future kernel. It does not contain malicious devices
that can misuse intentionally shared buffers or lie through their protocol.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
