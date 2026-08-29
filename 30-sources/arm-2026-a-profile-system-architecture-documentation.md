---
title: "Arm A-profile system architecture documentation"
kind: source
created: "2026-08-29"
authors:
  - "Arm Limited"
published: null
citation_key: "arm-a-profile-system-architecture"
container: "Arm Architecture and System Specifications"
edition: "Current issues accessed 2026-08-29"
isbn: null
doi: null
url: "https://developer.arm.com/documentation/ddi0487/latest/"
accessed: "2026-08-29"
tags:
  - aarch64
  - arm
  - cache-coherence
  - interrupt-controllers
  - iommu
  - operating-systems
  - power-management
aliases:
  - "Arm A-profile architecture set"
---

# Arm A-profile system architecture documentation

## Reference

Arm Limited. Current A-profile architecture set: [Arm Architecture Reference
Manual for A-profile](https://developer.arm.com/documentation/ddi0487/latest/),
[GIC architecture specification](https://developer.arm.com/documentation/ihi0069/latest/),
[SMMUv3 architecture specification](https://developer.arm.com/documentation/ihi0070/latest/),
[PSCI specification](https://developer.arm.com/documentation/den0022/latest/),
and [Generic Timer guide](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/Generic%20Timer.pdf?revision=c710e7a7-9f52-4901-8c9d-91b19f44f9c7).
Accessed 2026-08-29.

Two official engineering articles were used to clarify the normative cache
rules: [implementing instruction-cache synchronization](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/caches-self-modifying-code-implementing-clear-cache)
and [multicore code publication](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/caches-self-modifying-code-working-with-threads).

## Research question or contribution

What complete set of AArch64 architectural mechanisms must an EL1 kernel
coordinate for privilege, translation, interrupts, time, DMA isolation, CPU
power state, weak memory ordering, and native-code publication?

## Method

This was a cross-document reading of exception levels and traps, stage-1
translation and TLB maintenance, memory attributes and barriers, GICv3/v4,
generic counters and timers, SMMUv3, PSCI, and instruction/data cache
maintenance.

## Findings

- AArch64 provides mature, orthogonal system components, but the OS contract is
  spread across the CPU architecture, GIC, timer, SMMU, firmware, and platform
  specifications. A CPU-only port is incomplete.
- Weak memory ordering, shareability domains, memory types, and explicit
  barriers affect locks, MMIO, page-table publication, DMA, interrupt
  acknowledgement, and code loading.
- GIC separates interrupt distribution from per-CPU interfaces and supports
  wired and message-signaled delivery. Correct level-triggered handling still
  depends on device-specific masking and clearing before completion.
- The generic timer separates a continuously advancing counter from comparator
  timers and delivers per-CPU level-sensitive interrupts. PSCI provides a
  firmware interface for CPU and system power state; policy remains in the OS.
- SMMUv3 translates and protects device memory transactions, with command,
  event, and page-request queues whose lifecycle must compose with driver and
  device reset.
- Generated native code can require data-cache clean, instruction-cache
  invalidation, completion barriers, and an instruction synchronization event
  on every executing core. The exact sequence is an architecture service, not
  a runtime implementation detail.

## Relevance

AArch64 `virt` is the recommended second architecture because it exercises a
different firmware/power stack, GICv3, a mature SMMU, and strict cache and weak-
ordering rules. It is a portability test, not merely another backend.

## Limits

The documents specify architecture, not a concrete SoC. Optional features,
errata, firmware versions, cache topology, device integration, and board
description still need target-specific evidence.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
