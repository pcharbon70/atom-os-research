---
title: "IOMMU maintenance and completion"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - protected-io-and-dma-ownership
aliases: []
---

# IOMMU maintenance and completion

IOMMU work needs typed maintenance plans and scoped completion evidence. Consuming a queue entry, invalidating one cache and draining prior device traffic are not interchangeable outcomes.

## Scope and research question

How can a common service expose the guarantees needed for safe mapping changes without claiming that all remappers implement one universal fence?

This report refines [component 8: Protected I/O and DMA ownership](../protected-io-and-dma-ownership.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

MaintenancePlan identifies remapper instance, configuration generation, affected requester/address ranges, cache classes, command sequence and required observations. Track configuration caches, IOTLB state, device address-translation caches and interrupt-remapping state separately. Completion records bind the operation and affected scope; they do not grant frame ownership by themselves.

### Protocol and publication points

Validate change and profile → publish table writes with required visibility → enqueue ordered maintenance → observe the prescribed completion mechanism → check fault status → seal only the established predicates. If a sequence requires intermediate completion, represent it explicitly. Join device traffic or endpoint obligations separately when the remapper's guarantee does not cover them.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Queue progress is not a universal completion signal. SMMUv3 distinguishes command consumption from completion, and failed ATC synchronization does not establish the intended completion guarantees. Device cooperation can be part of a translation-cache invalidation protocol. On timeout, retain mappings and frames whose release still depends on that operation.

### Alternatives and tradeoffs

Synchronous maintenance simplifies callers but can block in unsuitable contexts. Split-phase plans make latency and retained custody explicit at greater state-machine cost. A universal strongest operation is acceptable only when each backend proves the same semantics, not merely because every backend has a fence-like command.

### Cross-architecture realization

VT-d queued invalidation, Arm command queues and RISC-V IOMMU commands require separate specification refinements. This session rechecked SMMUv3 G.b §§4.7.3–4.8; Intel document availability and the current RISC-V documentation reader were insufficient for equivalent fresh chapter-level validation, so those mappings remain based on archived readings.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Advance a simulated command consumer without completing invalidation; no release predicate may become true.
- Fail a device-cache invalidation after earlier commands have progressed; preserve uncertainty for the affected operation.
- Use a completion for the wrong remapper, generation or range and verify rejection.

Exact command refinements, error recovery and device-cache completion conditions still require a versioned backend conformance argument.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [I/O revocation and reclamation](revocation-and-reclamation.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Intel VT-d architecture](../../../30-sources/intel-2024-vt-d-architecture.md) — I/O translation and invalidation completion are separate mechanisms.
- [Arm SMMUv3 architecture](../../../30-sources/arm-2025-smmuv3-architecture.md) — IOMMU command and translation-cache synchronization scope.
- [RISC-V IOMMU architecture](../../../30-sources/risc-v-international-2026-iommu-architecture.md) — A distinct device-translation and command-completion profile.
- [Thunderclap](../../../30-sources/markettos-et-al-2019-thunderclap.md) — DMA spatial and temporal exposure despite translation protection.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
