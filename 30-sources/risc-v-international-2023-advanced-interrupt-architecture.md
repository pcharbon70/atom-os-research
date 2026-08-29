---
title: "RISC-V Advanced Interrupt Architecture 1.0"
kind: source
created: "2026-08-29"
authors:
  - "RISC-V International"
published: 2023
citation_key: "risc-v-international-2023-aia-1-0"
container: "RISC-V Advanced Interrupt Architecture"
edition: "Version 1.0; clarification release 20250312"
isbn: null
doi: null
url: "https://docs.riscv.org/reference/aia/index.html"
accessed: "2026-08-29"
tags:
  - interrupt-controllers
  - interrupts
  - operating-systems
  - risc-v
  - virtualization
aliases:
  - "RISC-V AIA 1.0"
---

# RISC-V Advanced Interrupt Architecture 1.0

## Reference

RISC-V International. *The RISC-V Advanced Interrupt Architecture*, version
1.0, ratified June 2023, clarification release 20250312. [Official HTML](https://docs.riscv.org/reference/aia/index.html)
and [official PDF](https://docs.riscv.org/reference/aia/_attachments/riscv-interrupts.pdf).
Accessed 2026-08-29.

## Research question or contribution

How should an interrupt subsystem accommodate wired sources, message-signaled
interrupts, per-hart delivery, priority, IPIs, and virtualization without
embedding one controller's register model in driver code?

## Method

The reading covered AIA goals, hart CSRs, IMSIC interrupt files, APLIC wired
sources and wired-to-MSI conversion, priorities, IPIs, virtual interrupt files,
and IOMMU interaction.

## Findings

- AIA combines ISA additions with two controllers: APLIC for wired sources and
  IMSIC for incoming MSIs. It is designed around high-performance and
  virtualized systems rather than being a drop-in alias for the older PLIC.
- MSI delivery makes the interrupt destination itself an address-translation
  and isolation concern. Interrupt identity and remapping must be coordinated
  with device assignment and IOMMU state.
- The architecture supports priority and per-hart files but leaves scheduling,
  affinity policy, storm control, handler budgeting, and actor notification to
  software.
- The specification explicitly does not supply automatic stack switching or
  the small-system interrupt behavior expected from some real-time MCUs.

## Relevance

The architecture-neutral interrupt API should represent source configuration,
destination, trigger mode, mask state, completion, affinity, and ownership. A
bootstrap PLIC driver can implement that API first; an AIA profile then tests
whether the abstraction really supports MSI and per-domain routing.

## Limits

AIA availability on physical boards and in firmware is not uniform. It does
not define the device's interrupt-clear protocol or make a handler safe to run
in privileged trap context.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
