---
title: "UEFI Specification 2.11"
kind: source
created: "2026-08-29"
authors:
  - "UEFI Forum"
published: 2024
citation_key: "uefi-forum-2024-uefi-2-11"
container: "Unified Extensible Firmware Interface Specification"
edition: "Version 2.11"
isbn: null
doi: null
url: "https://uefi.org/specs/UEFI/2.11/"
accessed: "2026-08-29"
tags:
  - boot
  - firmware
  - hardware-discovery
  - operating-systems
  - secure-boot
  - uefi
aliases:
  - "UEFI 2.11"
---

# UEFI Specification 2.11

## Reference

UEFI Forum. *Unified Extensible Firmware Interface Specification*, version
2.11, December 2024. [HTML specification](https://uefi.org/specs/UEFI/2.11/)
and [official specification index](https://uefi.org/specifications/). Accessed
2026-08-29.

## Research question or contribution

What firmware-owned services and data can a portable kernel loader use, and
where does ownership transfer irreversibly from firmware to the operating
system?

## Method

The reading covered the boot manager, architecture-specific handoff state,
system and configuration tables, memory maps, image loading,
`ExitBootServices`, runtime services, watchdog and reset calls, Secure Boot,
and the ability to pass ACPI or Devicetree data.

## Findings

- UEFI supplies a common pre-boot execution environment, image format and
  loading protocol across x64, AArch64, and RISC-V, but it is not the kernel's
  permanent hardware abstraction.
- The loader must obtain and validate the current memory map immediately before
  `ExitBootServices`. After a successful call, boot services, including
  firmware memory management, terminate and the loader owns continued system
  operation.
- Runtime services may remain callable, but require reserved runtime memory,
  mapping rules, prescribed execution state, serialization, and architecture-
  specific care. Every retained runtime call therefore extends the live
  firmware trust and failure boundary.
- UEFI configuration tables can carry ACPI and Devicetree roots. A portable
  handoff can normalize those inputs rather than expose firmware pointers to
  the rest of the kernel.
- Secure Boot authenticates images against firmware-managed policy. It does not
  by itself provide measured-boot evidence, rollback safety, runtime
  isolation, or recovery from a corrupted accepted image.

## Relevance

The specification supports a small UEFI loader as one boot adapter and a
firmware-neutral `BootInfo` contract as the kernel boundary. It argues against
letting allocation, console, filesystem, or device discovery continue to rely
silently on boot services after entry.

## Limits

UEFI specifies an interface rather than any firmware implementation's quality,
security, latency, or hardware-description accuracy. It does not replace the
processor, interrupt-controller, timer, IOMMU, ACPI, or device specifications.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
- [2026-08-29 research journal](../50-journal/2026-08-29-hardware-and-architecture-support-deep-dive.md)
