---
title: "CleanQ: A lightweight, uniform, formally specified interface for intra-machine data transfer"
kind: source
created: "2026-08-29"
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
accessed: "2026-08-29"
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
interfaces for multiple transfer mechanisms, and compares operation and
end-to-end costs with Virtio and DPDK paths.

## Findings

- Descriptor rings are ownership protocols over buffers, not merely circular
  arrays. Enqueue transfers an explicitly described region and dequeue returns
  it under precise obligations.
- A uniform contract can hide weak memory and non-coherent implementation
  details from clients while leaving them explicit in each queue backend.
- The paper reports tens-of-cycles operation overhead and comparable tested
  end-to-end performance, challenging the assumption that a formal interface
  must be heavyweight.
- Queue creation, authorization, quotas, reset, and device control remain
  outside CleanQ's data-plane contract.

## Relevance

DMA buffers and actor/service queues should use a common ownership state
machine where possible: `owned`, `offered`, `in-flight`, `returned`,
`quarantined`. Cache synchronization and barriers belong in the backend, but
the API must expose when ownership has actually changed.

## Limits

This is a research implementation and formal model, not direct verification of
this project's future Zig code or arbitrary hardware. It does not solve
malicious-device access beyond the authorized buffers.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
