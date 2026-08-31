---
title: "The RISC-V instruction set manual, privileged architecture"
kind: source
created: "2026-08-30"
authors:
  - "RISC-V International"
published: 2026
citation_key: "risc-v-international-2026-privileged-architecture"
container: "RISC-V Technical Specifications"
edition: "Ratified specifications, release 20260120"
isbn: null
doi: null
url: "https://docs.riscv.org/reference/isa/priv/priv-index.html"
accessed: "2026-08-30"
tags:
  - cpu-architecture
  - interrupts
  - memory-ordering
  - privilege
  - risc-v
  - virtual-memory
aliases:
  - "RISC-V privileged ISA"
---

# The RISC-V instruction set manual, privileged architecture

## Reference

RISC-V International. *The RISC-V Instruction Set Manual, Volume II:
Privileged Architecture*, ratified specifications release 20260120.
[Official privileged-architecture index](https://docs.riscv.org/reference/isa/priv/priv-index.html).
See also the [official specification library](https://docs.riscv.org/reference/home/index.html).

## Research question or contribution

Which ratified RISC-V privilege, translation, interrupt, ordering, time, and
state mechanisms must a supervisor-kernel architecture backend normalize?

## Method

The ratified privileged architecture and referenced ISA chapters were used as
the normative base. Optional platform interfaces are treated as discovered
dependencies, not assumed parts of the base ISA.

## Findings

- Machine, supervisor, and user privilege modes plus delegation registers
  determine which traps a supervisor kernel receives and which functionality
  still depends on a higher-privilege execution environment.
- `satp`, the Sv translation schemes, ASIDs, and `SFENCE.VMA` define address-
  translation state and local ordering. Remote-hart invalidation requires an
  explicit coordination mechanism beyond the local instruction.
- RVWMO is a relaxed memory model. `FENCE`, acquire/release atomics, and I/O
  ordering fields must be selected from the source-level synchronization and
  device contract, not inferred from another ISA's defaults.
- `FENCE.I` synchronizes a hart's later instruction fetches with earlier local
  stores; publishing code to other harts requires a remote synchronization
  protocol.
- Counter/timer facilities and timer-interrupt extensions can supply raw time
  and deadlines, while the supervisor's access and programming path depends on
  the implemented privilege and execution-environment profile.
- Floating-point, vector, and other extension state is optional and visible
  through architectural status. Context management must be parameterized by
  discovered extensions.

## Relevance

RISC-V is a strong test of whether the proposed contract is semantic rather
than x86-shaped: local versus remote completion, delegated versus retained
privilege, and optional extensions all need explicit representation. A port
should declare its execution-environment assumptions rather than burying them
inside generic calls.

## Limits

The privileged ISA alone is not a complete platform contract. Interrupt
controllers, IOMMUs, CPU-start services, discovery data, and firmware calls are
specified separately and may be absent. This note makes no board or physical
platform recommendation.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
