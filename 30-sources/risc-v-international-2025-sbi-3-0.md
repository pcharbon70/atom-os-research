---
title: "RISC-V Supervisor Binary Interface Specification 3.0"
kind: source
created: "2026-08-29"
authors:
  - "RISC-V International"
published: 2025
citation_key: "risc-v-international-2025-sbi-3-0"
container: "RISC-V Supervisor Binary Interface Specification"
edition: "Version 3.0, ratified"
isbn: null
doi: null
url: "https://github.com/riscv-non-isa/riscv-sbi-doc/releases/tag/v3.0"
accessed: "2026-08-29"
tags:
  - boot
  - firmware
  - operating-systems
  - privilege
  - risc-v
  - sbi
aliases:
  - "SBI 3.0"
---

# RISC-V Supervisor Binary Interface Specification 3.0

## Reference

RISC-V International. *RISC-V Supervisor Binary Interface Specification*,
version 3.0, ratified in 2025. [Official release](https://github.com/riscv-non-isa/riscv-sbi-doc/releases/tag/v3.0)
and [official PDF](https://docs.riscv.org/reference/platform-software/sbi/_attachments/riscv-sbi.pdf).
Accessed 2026-08-29.

## Research question or contribution

Which machine-mode mechanisms can a supervisor kernel deliberately delegate
to firmware without making that firmware its general hardware abstraction?

## Method

The reading covered the base extension and calling convention, timer, IPI,
remote fence, hart-state management, reset, performance monitoring, debug
console, system suspend, nested acceleration, and firmware-feature interfaces.

## Findings

- SBI is an `ecall` interface between supervisor software and its execution
  environment; OpenSBI is one implementation, not the specification itself.
- Standard calls can keep board-specific M-mode details out of an S-mode
  kernel while supplying early timers, IPIs, remote fences, CPU start/stop,
  reset, and an emergency console.
- Extensions are probed and versioned. The kernel needs explicit degraded
  paths when an extension is absent rather than assuming one OpenSBI build.
- Remote-fence and hart-state calls are mechanisms, not a substitute for the
  kernel's own CPU lifecycle, TLB-generation, or timeout protocols.

## Relevance

The preferred RV64 profile keeps M-mode in pinned OpenSBI firmware and enters
the Zig kernel in S-mode. This shrinks initial bring-up while preserving a
clear firmware dependency ledger and the option to replace the implementation.

## Limits

SBI does not specify Devicetree contents, page tables, external interrupt
controllers, device drivers, DMA isolation, or recovery policy. Firmware bugs
and latency remain below the kernel's trust boundary.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
