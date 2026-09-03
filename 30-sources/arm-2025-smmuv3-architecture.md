---
title: "Arm System Memory Management Unit architecture specification, SMMUv3"
kind: source
created: "2026-09-02"
authors:
  - "Arm Limited"
published: "2025-04-30"
citation_key: "arm-2025-smmuv3-architecture"
container: "Arm architecture specification"
edition: "ARM IHI 0070 G.b"
isbn: null
doi: null
url: "https://documentation-service.arm.com/static/6813b2bbefb0f21122c144c2"
accessed: "2026-09-02"
tags:
  - arm64
  - dma
  - iommu
  - memory-protection
aliases:
  - "Arm SMMUv3 G.b"
---

# Arm System Memory Management Unit architecture specification, SMMUv3

## Reference

Arm Limited. *Arm System Memory Management Unit Architecture Specification,
SMMU Architecture Version 3*, ARM IHI 0070 G.b, 30 April 2025.
[Official specification](https://documentation-service.arm.com/static/6813b2bbefb0f21122c144c2).

## Research question or contribution

Which architectural mechanisms let software associate device streams with
translation/protection contexts, update those contexts safely, observe faults,
and determine completion of configuration, IOTLB, and device-ATC invalidation?

## Method

This is a normative architecture specification. The analysis focuses on stream
identity, stream/context tables, command and event queues, translation-cache
maintenance, PCIe ATS interaction, and `CMD_SYNC` completion semantics rather
than implementation-specific performance.

## Findings

- A StreamID selects a stream-table entry that determines whether traffic is
  permitted and which stage-1/stage-2 translation configuration applies. The
  hardware identity granularity bounds the isolation granularity software can
  claim.
- In-memory configuration and translation structures can be cached. Safe
  replacement requires valid-bit/update rules, visibility barriers, targeted
  configuration or TLB invalidations, and a completion operation.
- Consumption of an invalidation command does not mean that invalidation has
  completed. A following `CMD_SYNC` supplies the relevant completion point.
- `CMD_ATC_INV` extends revocation to a PCIe device's address-translation cache.
  A timeout can make `CMD_SYNC` fail with `CERROR_ATC_INV_SYNC`; in that case the
  synchronization guarantees have not been met and an unknown subset of ATC
  invalidations may remain outstanding.
- Completion affects table-walk and event visibility as well as cached entries;
  stale event records are therefore part of the reclamation protocol.
- Event, command, and page-request queues introduce bounded-memory, overflow,
  fault, and denial-of-service concerns that software must account for.

## Relevance

The Arm backend should implement `DmaDomain` updates as transactions ending in
successful `CMD_SYNC`, not as table writes or command-queue consumption. ATS is
an optional advanced profile; an ATC invalidation timeout keeps affected leases
quarantined and their frames unreclaimable. StreamID aliasing must be reflected
as one atomic requester/trust attachment set.

## Limits

The specification defines permitted behavior, not the correctness or latency
of a concrete SMMU, interconnect, firmware description, PCIe hierarchy, or
device. It cannot prove that all DMA paths traverse the SMMU, that a device
obeys its shared-memory protocol, or that reset drains device-internal work.

## Derived work

- [Protected I/O and DMA ownership](../20-notes/kernel-hardware-and-architecture-components/protected-io-and-dma-ownership.md)
