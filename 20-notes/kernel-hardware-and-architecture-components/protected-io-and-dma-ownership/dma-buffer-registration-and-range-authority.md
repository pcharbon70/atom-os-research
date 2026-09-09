---
title: "DMA buffer registration and range authority"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - protected-io-and-dma-ownership
aliases: []
---

# DMA buffer registration and range authority

A DMA address is a scoped translation result, not ownership of memory. Registration must preserve frame authority, bounds, permissions and lifetime independently from whether device access is currently enabled.

## Scope and research question

How can a buffer be prepared for I/O without exposing neighboring data or creating a mapping that outlives its frame authority?

This report refines [component 8: Protected I/O and DMA ownership](../protected-io-and-dma-ownership.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Frame authority owns physical storage; DmaAddressSpace owns translation context; DmaMapping owns an IOVA interval and its maintenance obligations. BufferRegistration binds exact byte bounds, backing frames, authority epoch, direction, quota and profile. Outward mapping to protection granules records collateral bytes explicitly. DmaMapping lifetime and device-access lifetime are distinct.

### Protocol and publication points

Validate frame authority and checked ranges → reserve IOVA and accounting capacity → initialize protected descriptors → create dormant mapping state → return a generation-bound registration. Under EnforcedExclusive, dormant means the device cannot access the CPU-owned buffer, even if translation metadata has been allocated. Final deregistration requires revocation and all software view lifetimes to close.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Sharing a protection granule can expose unrelated bytes. Zeroing padding may reduce disclosure but does not make mutable neighboring ownership safe. Integer overflow, scatter/gather overlap, stale frame epochs and IOVA reuse can redirect access. A copied Zig handle does not prolong or transfer authority; protected state must validate it.

### Alternatives and tradeoffs

Dedicated I/O granules simplify isolation at a memory and copy cost. Shared-granule mappings require a deliberately weaker or jointly owned profile. Bounce buffers reduce exposure but add copy, lifetime and completion obligations rather than eliminating them.

### Cross-architecture realization

Physical and I/O virtual address widths, mapping granules and permission capabilities depend on the remapper and execution environment. CPU page size alone cannot define the DMA isolation granule.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Register sub-granule and overlapping ranges and account for every additionally exposed byte.
- Release and reuse a backing frame while an old mapping handle survives; the stale epoch must not authorize access.
- Exhaust IOVA and metadata quotas at each acquisition point; rejection must preserve the caller's frame authority.

A full range-conservation proof, quota policy and treatment of device-specific addressability limits remain unverified.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [CPU-device transfer and queue publication](cpu-device-transfer-and-queue-publication.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Thunderclap](../../../30-sources/markettos-et-al-2019-thunderclap.md) — DMA spatial and temporal exposure despite translation protection.
- [CleanQ](../../../30-sources/haecki-et-al-2019-cleanq.md) — Transfer-set conservation under cooperative ownership assumptions.
- [Intel VT-d architecture](../../../30-sources/intel-2024-vt-d-architecture.md) — I/O translation and invalidation completion are separate mechanisms.
- [Arm SMMUv3 architecture](../../../30-sources/arm-2025-smmuv3-architecture.md) — IOMMU command and translation-cache synchronization scope.
- [RISC-V IOMMU architecture](../../../30-sources/risc-v-international-2026-iommu-architecture.md) — A distinct device-translation and command-completion profile.
- [Zig language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
