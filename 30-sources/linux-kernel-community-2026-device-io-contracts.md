---
title: "Bus-Independent Device Accesses"
kind: source
created: "2026-09-08"
authors:
  - "Matthew Wilcox"
  - "Alan Cox"
published: null
citation_key: "linux-kernel-community-2026-device-io-contracts"
container: "The Linux Kernel documentation"
edition: null
isbn: null
doi: null
url: "https://www.kernel.org/doc/html/latest/driver-api/device-io.html"
accessed: "2026-09-08"
tags:
  - architecture-support
  - kernel-architecture
aliases: []
---

# Bus-Independent Device Accesses

## Reference

Matthew Wilcox, Alan Cox. [Bus-Independent Device Accesses](https://www.kernel.org/doc/html/latest/driver-api/device-io.html). The Linux Kernel documentation; publication date not stated. Accessed 2026-09-08.

## Research question or contribution

How Linux drivers should access device memory while respecting mapping, access width and ordering requirements.

## Method

Official maintained API documentation. Read the MMIO access, ordering, endianness and posted-write discussion; this is an engineering contract, not a controlled performance experiment.

## Findings

MMIO accessors have semantics that ordinary memory-copy operations do not provide. Posted writes can require an appropriate readback to establish receipt; CPU-side ordering alone is a different guarantee.

## Relevance

Use separate register-access, ordering, receipt and operation-completion contracts in the proposed architecture.

## Limits

These are Linux API contracts and device/bus-dependent examples. They do not prove that any arbitrary register is safe to read back, or that receipt implies completion of the device's commanded operation.

## Derived work

- [Typed MMIO ordering and completion](../20-notes/kernel-hardware-and-architecture-components/ordering-coherence-and-code-publication/typed-mmio-ordering-and-completion.md) — architecture synthesis constrained by this source.
- [CPU-device transfer and queue publication](../20-notes/kernel-hardware-and-architecture-components/protected-io-and-dma-ownership/cpu-device-transfer-and-queue-publication.md) — architecture synthesis constrained by this source.
