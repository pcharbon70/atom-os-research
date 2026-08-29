---
title: "Intel 64 system programming and VT-d documentation"
kind: source
created: "2026-08-29"
authors:
  - "Intel Corporation"
published: 2026
citation_key: "intel-2026-system-programming"
container: "Intel Architecture Specifications"
edition: "SDM version 092; VT-d revision 5.0"
isbn: null
doi: null
url: "https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html"
accessed: "2026-08-29"
tags:
  - interrupt-controllers
  - iommu
  - memory-models
  - operating-systems
  - privilege
  - x86-64
aliases:
  - "Intel SDM and VT-d"
---

# Intel 64 system programming and VT-d documentation

## Reference

Intel Corporation. *Intel 64 and IA-32 Architectures Software Developer's
Manual*, version 092, 19 August 2026. [Official manual page](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html).
Also used: *Intel Virtualization Technology for Directed I/O Architecture
Specification*, revision 5.0, August 2024. [Official VT-d PDF](https://cdrdv2-public.intel.com/831418/vt-directed-io-spec.pdf).
Accessed 2026-08-29.

## Research question or contribution

What does an x86-64 hardware-support port gain from the mature PC architecture,
and which legacy and platform mechanisms increase its initial trusted and
testing surface?

## Method

The reading covered long-mode privilege, paging and PCIDs, IDT exceptions,
local APIC and I/O APIC, MSI, TSC and deadline timers, multiprocessor startup,
cache and TLB control, XSAVE extended state, machine checks, VMX, and VT-d
translation and interrupt remapping.

## Findings

- x86-64 supplies mature paging, interrupt, timer, virtualization, RAS, and
  IOMMU facilities with broad emulator and physical-hardware support.
- The practical PC platform also includes boot compatibility, ACPI/AML, APIC
  variants, chipset and PCI enumeration, model-specific registers, feature
  probing, firmware quirks, and security mitigations. That makes it a wide
  first bring-up target.
- TSO is stronger than Arm and RISC-V weak ordering, but it is not sequential
  consistency. An x86-only implementation can accidentally omit portable
  acquire/release or device-ordering contracts.
- PCID, large pages, TSC-deadline, MSI-X, interrupt remapping, and VT-d offer a
  strong eventual server profile. Every feature needs absence and fallback
  behavior.
- XSAVE state is variable by feature set; vector and accelerator extensions can
  make thread context substantially larger than integer trap state.

## Relevance

x86-64 is a valuable later compatibility and commodity-hardware target, but it
is not the preferred architecture for proving the first layer decomposition.
Its mature features should shape interfaces without forcing PC legacy into the
architecture-neutral core.

## Limits

Intel's documents do not describe AMD differences or all motherboard firmware
behavior. Model-specific errata, microcode, speculative-execution mitigations,
and non-Intel IOMMUs require separate target evidence.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
