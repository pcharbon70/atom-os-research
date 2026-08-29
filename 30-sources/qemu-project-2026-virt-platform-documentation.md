---
title: "QEMU Arm and RISC-V virt platform documentation"
kind: source
created: "2026-08-29"
authors:
  - "QEMU Project contributors"
published: null
citation_key: "qemu-project-virt-platforms"
container: "QEMU System Emulator documentation"
edition: "QEMU 11.1.50 development documentation, accessed 2026-08-29"
isbn: null
doi: null
url: "https://www.qemu.org/docs/master/system/targets.html"
accessed: "2026-08-29"
tags:
  - aarch64
  - emulation
  - operating-systems
  - qemu
  - risc-v
  - testing
aliases:
  - "QEMU virt platforms"
---

# QEMU Arm and RISC-V virt platform documentation

## Reference

QEMU Project contributors. [RISC-V system emulator](https://www.qemu.org/docs/master/system/target-riscv.html),
[RISC-V `virt` board](https://www.qemu.org/docs/master/system/riscv/virt.html),
[Arm `virt` board](https://www.qemu.org/docs/master/system/arm/virt), and [Arm
SBSA reference board](https://www.qemu.org/docs/master/system/arm/sbsa.html).
The rendered manual identified itself as QEMU 11.1.50 development
documentation when accessed on 2026-08-29.

## Research question or contribution

Which reproducible virtual platforms can exercise the proposed hardware
components before a physical board fixes the project to one vendor SoC?

## Method

The reading inventoried CPUs, firmware paths, discovery formats, interrupt
controllers, timers, UARTs, PCI/virtio, IOMMUs, watchdogs, machine-version
behavior, and documented differences between generic virtual and hardware-like
reference machines.

## Findings

- Both Arm and RISC-V `virt` are synthetic platforms designed for guests, not
  models of one physical board. That improves controlled bring-up but cannot
  establish real-hardware correctness.
- RISC-V `virt` supports PLIC or AIA, ACPI or Devicetree, PCI/virtio, and both
  PCI and platform RISC-V IOMMU devices. These switches allow the same kernel
  interfaces to be tested against progressively stronger mechanisms.
- Arm `virt` supports GIC variants, ITS/MSI, optional SMMUv3, a generic
  watchdog, PSCI-compatible firmware paths, PCI, virtio-mmio, many CPUs, and
  machine-version pinning.
- Arm `virt` offers versioned `virt-N.N` machine types. The current RISC-V
  `virt` documentation exposes a moving `virt` configuration rather than an
  Arm-style versioned alias, and `-cpu max` can also change with QEMU.
  Reproducible tests must therefore record the QEMU release/build, use a
  versioned machine type where available, pin the CPU model and every feature
  switch, retain firmware artifacts, and hash the generated description.

## Relevance

QEMU enables a bootstrap profile, protection profile, fault injection, and
cross-architecture CI without pretending that one successful boot validates a
physical target. The recommended sequence is RV64 `virt`, then AArch64 `virt`,
then one selected physical board.

## Limits

Emulated timing, cache behavior, coherency, DMA races, firmware bugs, errata,
power transitions, and device reset behavior can differ radically from real
hardware. KVM and TCG also expose different behavior.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
- [2026-08-29 research journal](../50-journal/2026-08-29-hardware-and-architecture-support-deep-dive.md)
