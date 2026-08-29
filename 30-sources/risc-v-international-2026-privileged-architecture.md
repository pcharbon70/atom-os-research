---
title: "RISC-V privileged and unprivileged architecture specifications"
kind: source
created: "2026-08-29"
authors:
  - "RISC-V International"
published: 2026
citation_key: "risc-v-international-2026-architecture"
container: "RISC-V Ratified Specifications Library"
edition: "Release v20260120; privileged architecture 1.13"
isbn: null
doi: null
url: "https://docs.riscv.org/reference/home/index.html"
accessed: "2026-08-29"
tags:
  - memory-models
  - memory-protection
  - operating-systems
  - privilege
  - risc-v
  - virtual-memory
aliases:
  - "RISC-V privileged architecture 1.13"
  - "RVWMO specification"
---

# RISC-V privileged and unprivileged architecture specifications

## Reference

RISC-V International. *The RISC-V Instruction Set Manual*, unprivileged and
privileged architecture release v20260120, January 2026; privileged
architecture version 1.13. [Ratified library](https://docs.riscv.org/reference/home/index.html),
[privileged PDF](https://docs.riscv.org/reference/isa/_attachments/riscv-privileged.pdf),
and [RVWMO chapter](https://docs.riscv.org/reference/isa/unpriv/rvwmo.html).
Accessed 2026-08-29.

## Research question or contribution

What exact CPU contract would an RV64 kernel own for traps, privilege,
translation, protection, counters, atomics, memory ordering, instruction
publication, and multicore coordination?

## Method

The reading covered M/S/U privilege, delegation, CSRs and trap entry, PMP and
Smepmp, Sv39 translation, ASIDs, `SFENCE.VMA`, counter access, supervisor timer
extensions, RVWMO, atomics and fences, and `FENCE.I`.

## Findings

- RISC-V separates an open unprivileged ISA from a conventional optional
  privileged architecture. An OS must select and probe an explicit extension
  profile rather than infer one monolithic "RISC-V" machine.
- Supervisor mode plus Sv39 provides a conventional 64-bit kernel/user split;
  machine mode can remain firmware-owned through SBI. PMP protects physical
  regions below S-mode but has finite entries and different semantics from
  page-based virtual memory.
- Address-translation updates have explicit ordering and invalidation rules.
  `SFENCE.VMA` is local, so remote shootdown is a protocol involving IPIs,
  acknowledgements, and the architecture's memory-order guarantees.
- RVWMO permits other harts to observe operations in orders that differ from
  program order unless preserved by dependencies, acquire/release operations,
  atomics, or fences. Correct code must state a language-to-ISA ordering
  contract.
- `FENCE.I` only synchronizes instruction fetch on the executing hart. Publishing
  generated or loaded native code across harts needs data ordering, remote
  instruction synchronization, and a migration-safe kernel interface.

## Relevance

The specifications make RV64 a useful first architecture: its contracts are
open and decomposed, and QEMU exposes both simple and modern platform options.
They also show why the architecture port must expose typed operations for
barriers, translation synchronization, and code publication instead of
scattered inline assembly.

## Limits

The ISA does not define a complete board. Interrupt controllers, firmware,
IOMMUs, buses, cache topology, discovery, and platform quality are separate.
The RVWMO chapter explicitly leaves some interactions with I/O, instruction
fetch, and page-table walks outside its formalized core.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
