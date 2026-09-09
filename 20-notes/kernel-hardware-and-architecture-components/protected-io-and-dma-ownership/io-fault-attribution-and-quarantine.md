---
title: "I/O fault attribution and quarantine"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - protected-io-and-dma-ownership
aliases: []
---

# I/O fault attribution and quarantine

Fault reporting should preserve capture-time identity while keeping diagnosis separate from containment. An informative fault record does not itself stop a requester or make its buffers safe to release.

## Scope and research question

How can asynchronous I/O failures be attributed after bindings change without granting diagnostic code control over live hardware authority?

This report refines [component 8: Protected I/O and DMA ownership](../protected-io-and-dma-ownership.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

The bounded capture path records requester identity, binding and mapping generations, operation ID, raw syndrome and capture context. Component 9 owns diagnostic capture and custody; component 5 owns interrupt flow; this service owns I/O fault-to-transaction attribution and quarantine transitions. Deferred reports carry redacted identifiers, not live capabilities.

### Protocol and publication points

Capture bounded immutable event → resolve against capture-time generations → classify known operation, stale event or unattributed event → request authorized containment → retain unresolved resources in quarantine → publish diagnosis independently. DeviceRemovedUnknown remains uncertain until the applicable access and reset evidence closes it.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Fault storms can exhaust storage or livelock decoding. Preallocated capacity, explicit loss accounting and quarantine escalation are necessary. A stale fault cannot be reassigned to the current owner of a reused address. Device-provided status can be hostile; absence of reported faults is not proof that isolation works.

### Alternatives and tradeoffs

Immediate rich decoding improves convenience but increases dependencies in a fragile context. Raw bounded capture with deferred interpretation preserves a smaller failure path, at the cost of possible missing context unless identities and raw evidence are sealed early.

### Cross-architecture realization

IOMMU event queues, device interrupts and platform error signals have different ordering and loss behavior. Backend capture must retain those limitations rather than presenting every event stream as reliable or complete.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Rebind a requester before deferred decoding; the event must retain its original attribution or explicit uncertainty.
- Overflow capture capacity and verify bounded behavior with visible loss accounting and preserved terminal evidence.
- Remove a device during an active transfer; fault delivery alone must not release frames or queue leases.

Fault-rate bounds, reliable attribution under firmware intervention and quarantine capacity policy remain research obligations.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Requester and endpoint scope binding](requester-endpoint-scope-binding.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Thunderclap](../../../30-sources/markettos-et-al-2019-thunderclap.md) — DMA spatial and temporal exposure despite translation protection.
- [Arm SMMUv3 architecture](../../../30-sources/arm-2025-smmuv3-architecture.md) — IOMMU command and translation-cache synchronization scope.
- [RISC-V IOMMU architecture](../../../30-sources/risc-v-international-2026-iommu-architecture.md) — A distinct device-translation and command-completion profile.
- [Tock deployment retrospective](../../../30-sources/schuermann-et-al-2025-tock-decade.md) — Typed interfaces still require sound ABI and runtime validation.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
