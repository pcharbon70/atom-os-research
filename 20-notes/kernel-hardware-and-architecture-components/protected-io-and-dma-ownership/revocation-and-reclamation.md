---
title: "I/O revocation and reclamation"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - protected-io-and-dma-ownership
aliases: []
---

# I/O revocation and reclamation

Revocation closes authority; reclamation reuses storage. A safe design joins every outstanding access and software-lifetime obligation between those two events.

## Scope and research question

What evidence permits a frame or IOVA to be reused after a principal, mapping or device loses access?

This report refines [component 8: Protected I/O and DMA ownership](../protected-io-and-dma-ownership.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

A RevocationTransaction captures the mapping generation, frame epochs, requester scope and immutable set of outstanding leases. Its release predicate joins CPU restriction quiescence, device permission closure, remapper and device-cache maintenance, required traffic drainage, queue references and deferred diagnostic/software readers. Each contributing service certifies only its own scope.

### Protocol and publication points

Close new admission → revoke device access → issue required maintenance → resolve or quarantine active transfers → drain relevant access and software references → join exact predicates → retire mapping → release IOVA and frame authority. Revocation may complete as an authority change before all retained resources are reusable; expose those states separately.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Removing a table entry does not erase cached translation or cancel requests already accepted downstream. A missing device may leave activity uncertain. Reusing an IOVA too early can redirect a delayed transaction to unrelated memory. A reset completion with narrower scope cannot discharge wider mapping obligations.

### Alternatives and tradeoffs

Never reusing revoked storage avoids some temporal attacks but is not sustainable without bounded admission and failure policy. Eager reuse improves capacity only by weakening safety if drainage is unproven. Bounce-buffer pools can bound exposure but require the same reuse reasoning.

### Cross-architecture realization

Translation-cache completion and interconnect transaction observability differ by architecture and device profile. CPU TLB quiescence and IOMMU completion must not be collapsed into a single architecture-neutral Boolean.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Delay one contributor to the release join while completing all others; neither frames nor IOVA may be reused.
- Replay a delayed DMA or completion after revocation begins; it must not acquire authority over a successor generation.
- Lose the device during drainage and verify that unresolved resources transfer to an accountable quarantine owner.

The joined proof is an architectural proposal. Its completeness against every CPU alias, device request and software observer remains to be established.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Reset-domain and recovery authority](reset-domain-and-recovery-authority.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Thunderclap](../../../30-sources/markettos-et-al-2019-thunderclap.md) — DMA spatial and temporal exposure despite translation protection.
- [CleanQ](../../../30-sources/haecki-et-al-2019-cleanq.md) — Transfer-set conservation under cooperative ownership assumptions.
- [Intel VT-d architecture](../../../30-sources/intel-2024-vt-d-architecture.md) — I/O translation and invalidation completion are separate mechanisms.
- [Arm SMMUv3 architecture](../../../30-sources/arm-2025-smmuv3-architecture.md) — IOMMU command and translation-cache synchronization scope.
- [RISC-V IOMMU architecture](../../../30-sources/risc-v-international-2026-iommu-architecture.md) — A distinct device-translation and command-completion profile.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
