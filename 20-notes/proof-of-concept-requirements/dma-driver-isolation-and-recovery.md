---
title: "DMA driver isolation and recovery"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - capability-roadmap
  - proof-of-concept
  - requirements
aliases: []
---

# DMA driver isolation and recovery

Requirement R16, after M4. Safely replace a bus-mastering driver without allowing old device activity to corrupt newly assigned memory. A user-space address boundary alone cannot enforce this property.

## Evidence and the completion gap

As comparative evidence, the [RISC-V IOMMU specification](../../30-sources/risc-v-international-2026-iommu-architecture.md) defines translation/invalidation commands and completion ordering. Its read/write fencing covers relevant already-processed activity; it does not automatically prove that every request still upstream in the device/interconnect has disappeared.

[MINIX driver recovery research](../../30-sources/herder-et-al-2006-dependable-operating-system.md) supports separating driver failures from the kernel, but its software recovery topology is not an end-to-end proof of DMA quiescence for an arbitrary device.

Choose one device and actual requester/reset topology. Begin with mediated buffers and no ATS/PRI or peer-to-peer DMA unless the selected hardware contract requires them. These are proposed restrictions; device support must be verified.

For the selected T7500, investigate the Intel 5520 platform and the actual [VT-d capabilities](../../30-sources/intel-2024-vt-d-architecture.md), firmware DMAR tables, requester coverage and device reset rules. The modern VT-d 5.0 reference is not proof that this older platform implements those features or has remapping enabled. AMD IOMMU is not the backend for this target. The initial serial-only virtual profile makes no DMA-isolation claim.

## Proposed authority and ownership model

Identify requester IDs, functions sharing a reset domain, interrupt routing, IOMMU grouping, translation mode and firmware ownership. A device advertised as separate may share reset or isolation scope with another service.

The driver receives only its device control range and bounded buffer authority. A trusted mediator installs mappings for explicitly owned buffers. Kernel/user page permissions do not constrain DMA; record the IOMMU or other hardware protection that does.

Each descriptor and completion belongs to a driver/service epoch and a buffer ownership state. Validate completions against outstanding descriptors; an old descriptor index is not sufficient authority to release a newly reused buffer.

Copying through dedicated DMA buffers reduces the set of exposed pages at the cost of bandwidth and CPU. Zero-copy is a later optimization requiring pinned lifetime, cancellation and accounting protocols, not merely a different API.

## Recovery and safe reuse

On failure, close new submissions, stop driver execution and prevent new MMIO/doorbell access. Establish device quiescence or reset under the actual device specification. Remove or deny DMA mappings and complete required invalidations and fences. Account for requests still in the device or interconnect before freeing buffers.

The exact ordering depends on the device and IOMMU contract; this outline is an obligation list, not a universal reset recipe. If completion cannot be established, quarantine memory and potentially the whole device. Define a finite quarantine budget and escalation when it fills.

Retire interrupts, timers and software references as well as DMA access. A late completion can be harmless to memory but still corrupt accounting if it frees a new epoch's buffer.

Reset collateral matters: recovering one function may interrupt another service or destroy shared device state. Include those services in the declared recovery boundary or choose another device.

## Acceptance and next exploration

Before implementation, read the selected device's reset, descriptor and completion specifications alongside the platform IOMMU and interconnect rules. Confirm which emulator behaviors are faithful enough to test and which require physical hardware.

Inject delayed DMA, stale completions, lost interrupts, reset timeout, driver failure after descriptor publication and exhaustion of quarantined buffers. Place canaries in memory reassigned to another domain and verify that old activity cannot alter it.

Retain command/fence/reset traces and the evidence used to declare each buffer reusable. A successful driver restart or IOMMU-enabled boot is insufficient.

The next artifact is a device-specific ownership and quiescence state machine. No device/requester/reset profile has been selected, and no isolated DMA recovery claim is supported yet.

## Connections

[Lifecycle](domain-lifecycle-and-safe-reclamation.md) supplies the software close protocol. [Networking](networking-and-remote-actor-boundaries.md) and [storage](durable-state-and-crash-consistency.md) may introduce the first DMA consumers.
