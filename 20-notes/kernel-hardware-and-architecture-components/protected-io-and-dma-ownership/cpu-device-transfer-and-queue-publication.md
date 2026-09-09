---
title: "CPU-device transfer and queue publication"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - protected-io-and-dma-ownership
aliases: []
---

# CPU-device transfer and queue publication

Ownership transfer has both a software protocol and an enforcement profile. Clean transfer bookkeeping is valuable, but it does not by itself stop a malicious device or a stale CPU alias.

## Scope and research question

Which evidence is required before a buffer becomes DeviceOwned and before CPU access may resume?

This report refines [component 8: Protected I/O and DMA ownership](../protected-io-and-dma-ownership.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

BufferState, FrameAuthorityEpoch and QueueLease have one protected owner. EnforcedExclusive closes all relevant CPU access paths before device admission and removes device access before CPU reacquisition. TrustedTypestateExclusive relies on cooperating agents; CoherentShared intentionally permits concurrency under a separate synchronization contract. A completion descriptor is untrusted until matched to a current queue lease and bounds.

### Protocol and publication points

CpuOwned → DormantMappedCpuOwned → CpuClosing → CpuAccessClosed → Offered → DeviceOwned → Returned → CpuReacquiring → DormantMappedCpuOwned or CpuOwned. RestrictionQuiescent is required at the CPU-close boundary for enforced exclusivity. Publish initialized descriptors with the necessary memory/device ordering before notification. Returned begins reacquisition; it does not independently certify revoked access or cache visibility.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

An interrupt or device-written index can be forged, duplicated or delayed. It cannot return arbitrary buffer authority. CPU aliases, speculative exposure and noncoherent caches are separate obligations. Conservation of software ownership sets assumes agents respect relinquishment; hardware containment requires additional translation and access controls.

### Alternatives and tradeoffs

Copying isolates producer and consumer buffers but adds latency and storage pressure. Cooperative zero-copy transfer offers efficiency under trust assumptions. Enforced zero-copy exclusivity has stronger security goals and substantially more expensive closure and maintenance requirements.

### Cross-architecture realization

Coherent DMA does not imply ordering, ownership or permission revocation. Noncoherent profiles add direction-specific cache maintenance. Each backend must name the point at which descriptor publication and data visibility become valid for that interconnect and device.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Forge queue indices and replay completions after lease reuse; only the exact live transfer may change ownership.
- Retain a writable CPU alias through CpuClosing; EnforcedExclusive must not reach DeviceOwned.
- Race cancellation and completion while delaying visibility; terminal ownership must be unique and CPU reads must wait for reacquisition.

No end-to-end proof connects queue conservation, all CPU aliases and malicious-device containment for the proposed profiles.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [IOMMU maintenance and completion](iommu-maintenance-and-completion.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [CleanQ](../../../30-sources/haecki-et-al-2019-cleanq.md) — Transfer-set conservation under cooperative ownership assumptions.
- [Thunderclap](../../../30-sources/markettos-et-al-2019-thunderclap.md) — DMA spatial and temporal exposure despite translation protection.
- [Linux device-I/O contracts](../../../30-sources/linux-kernel-community-2026-device-io-contracts.md) — Posted-write receipt differs from CPU-side ordering.
- [Tock HIL design](../../../30-sources/tock-project-2026-hil-design.md) — Submission, returned ownership and asynchronous completion contracts.
- [Zig language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
