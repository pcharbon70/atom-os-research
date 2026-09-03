---
title: "RISC-V IOMMU architecture specification"
kind: source
created: "2026-09-02"
authors:
  - "RISC-V International"
published: "2026-02-22"
citation_key: "risc-v-international-2026-iommu"
container: "RISC-V Ratified Specifications Library"
edition: "Version 1.0.1, release 20260222"
isbn: null
doi: null
url: "https://docs.riscv.org/reference/iommu/v20260222/index.html"
accessed: "2026-09-02"
tags:
  - dma
  - iommu
  - memory-protection
  - risc-v
aliases:
  - "RISC-V IOMMU 1.0.1"
---

# RISC-V IOMMU architecture specification

## Reference

RISC-V International. *RISC-V IOMMU Architecture Specification*, version
1.0.1, ratified release 20260222, 22 February 2026.
[Official specification](https://docs.riscv.org/reference/iommu/v20260222/index.html).

## Research question or contribution

How does a RISC-V platform associate device and process identities with
translation contexts, synchronize cached I/O translations, invalidate PCIe
device ATCs, and report command/fault completion?

## Method

This is a normative architecture specification. The analysis uses the base
architecture, command-queue rules, data-structure update requirements, and
software guidelines for `IOTINVAL`, `ATS.INVAL`, and `IOFENCE.C`.

## Findings

- Device and optional process identifiers select memory-resident contexts for
  one- or two-stage translation. The specification admits implementation-
  dependent identity widths and discoverable feature combinations.
- The IOMMU can cache directory, context, page-table, and MSI-table data.
  Software must follow valid-entry atomicity rules and issue the matching
  invalidations; ordinary stores are not sufficient synchronization.
- Command-queue head advancement or an empty queue does not prove that fetched
  commands completed. Successful `IOFENCE.C` completion guarantees prior
  commands were completed and committed.
- `IOFENCE.C` uses `PR` and `PW` to request completion ordering for prior read
  and write transactions respectively. For memory reclamation, the
  specification calls for `PR` after device-read-only access and both `PR` and
  `PW` after device-write access. Those operands cover requests already
  processed by the IOMMU; software still needs device/interconnect-specific
  evidence that no new or upstream transaction remains.
- When PCIe ATS is enabled, software must invalidate both the IOMMU's IOATC and
  the device's DevATC, in the specified order. `ATS.INVAL` completes on device
  response or protocol timeout, and the following `IOFENCE.C` reports timeout.
- A safe reclamation sequence first disallows access in the page tables and
  then uses the appropriate invalidation and fence completion; failure keeps
  the old authority's effects unresolved.
- Command, fault, and page-request queues have explicit error and stall states.
  Recovery must account for which commands might need resubmission after the
  last successful fence.

## Relevance

The RISC-V backend maps naturally to a split-phase DMA transaction with a
completion epoch backed by `IOFENCE.C`. The portable API must preserve timeout
and partial-progress states. ATS and PRI should remain disabled in the initial
profile because they add device-side caches, flow-control limits, and recovery
obligations.

## Limits

The IOMMU is a separate platform component and is not guaranteed by the RISC-V
ISA alone. The specification does not prove that a concrete platform routes
every requester through it, assigns identifiers without aliasing, or supplies
the reset and bus-quiescence mechanisms needed for full device revocation.

## Derived work

- [Protected I/O and DMA ownership](../20-notes/kernel-hardware-and-architecture-components/protected-io-and-dma-ownership.md)
