---
title: "Requester and endpoint scope binding"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - protected-io-and-dma-ownership
aliases: []
---

# Requester and endpoint scope binding

A software device endpoint is not necessarily an independently isolatable or resettable hardware unit. Protected I/O must bind the actual requester, interrupt and reset scopes before granting authority.

## Scope and research question

What is the smallest defensible authority boundary when bridges, aliases, peer-to-peer paths and shared reset mechanisms connect several functions?

This report refines [component 8: Protected I/O and DMA ownership](../protected-io-and-dma-ownership.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Keep RequesterSet, DeviceEndpoint, InterruptSourceSet and ResetDomain distinct. A Binding generation links their verified relationships and the selected isolation profile. RequesterSet accounts for all agents that can issue accesses under the shared protection boundary. Component 5 owns interrupt bindings; the I/O object holds a constrained view rather than a second mutable binding owner.

### Protocol and publication points

Discover candidate endpoint → reconcile requester aliases and topology → establish isolation and reset scopes → bind current generations → validate profile → grant scoped endpoint authority. Unresolved bypass paths or unknown aliases prevent a strong isolation claim. Rebinding closes old authority and drains its users before exposing a successor generation.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Assigning separate handles cannot split a hardware isolation group. Peer-to-peer routing can bypass the expected translation path, and a reset may affect innocent siblings. Interrupt remapping and DMA translation are different facilities. A device-provided identifier is untrusted input, not evidence that a requester belongs to a principal.

### Alternatives and tradeoffs

Whole-group assignment is conservative but can reduce availability and sharing. Fine-grained assignment is valid only when hardware and topology establish the finer boundary. Trusting cooperative drivers permits a weaker profile, which must not be labeled hardware containment.

### Cross-architecture realization

VT-d, SMMUv3 and the RISC-V IOMMU identify and translate requesters differently. PCI topology is only one possible interconnect. Normalize scope evidence and limitations, not register names or an assumption that every device is behind an enabled remapper.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Model aliases and bridge paths that merge two apparent functions; independent isolation authority must be refused.
- Change an interrupt binding while retaining an old endpoint view; stale-generation operations must fail.
- Request reset through one function in a shared domain and verify authority covers every affected endpoint.

Discovery of every bypass and collateral reset path remains platform-dependent evidence; no physical topology has been verified in this research.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [DMA buffer registration and range authority](dma-buffer-registration-and-range-authority.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [VFIO isolation groups](../../../30-sources/linux-kernel-community-2026-vfio-isolation-groups.md) — Device functions do not necessarily form independent isolation units.
- [Thunderclap](../../../30-sources/markettos-et-al-2019-thunderclap.md) — DMA spatial and temporal exposure despite translation protection.
- [Intel VT-d architecture](../../../30-sources/intel-2024-vt-d-architecture.md) — I/O translation and invalidation completion are separate mechanisms.
- [Arm SMMUv3 architecture](../../../30-sources/arm-2025-smmuv3-architecture.md) — IOMMU command and translation-cache synchronization scope.
- [RISC-V IOMMU architecture](../../../30-sources/risc-v-international-2026-iommu-architecture.md) — A distinct device-translation and command-completion profile.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
