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
accessed: "2026-09-05"
tags:
  - cpu-architecture
  - hardware-errors
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
- Early trap code must save `xepc`, `xcause`, and other overwrite-prone state
  before enabling interrupts or causing another exception; scratch registers
  provide an architecture-defined route to hart-local entry storage but do not
  themselves switch stacks.
- Ratified double-trap and resumable-NMI extensions make recursive failure an
  explicit profile choice. Depending on the implemented extensions, an
  unexpected second trap can redirect into RNMI state or enter a platform-
  signalled critical-error state; the base trap mechanism alone supplies
  neither a portable recursive-recovery guarantee nor a universal reset
  behavior.
- Under `Ssdbltrp`, an unexpected trap from S/VS handling transfers to M-mode
  with exception code 16 in `mcause`; `mtval2` records the cause value that the
  unexpected trap would have written, while the remaining M-mode trap state is
  written for the transfer. This repurposing means a guest-page-fault guest
  physical address otherwise carried in `mtval2` is unavailable. Under
  `Smdbltrp` with `Smrnmi`, `mnepc`/`mncause` describe the unexpected trap while
  the first trap's `mepc`/`mcause` remains separately available, and the RNMI
  state supplies no corresponding `mtval`/`mtval2` detail.
- The base privileged architecture still does not define a universal hardware-
  error taxonomy. The separately ratified optional [RERI
  specification](risc-v-international-2024-ras-error-record-interface.md) adds a
  standardized record interface.

## Relevance

RISC-V is a strong test of whether the proposed contract is semantic rather
than x86-shaped: local versus remote completion, delegated versus retained
privilege, and optional extensions all need explicit representation. A port
should declare its execution-environment assumptions rather than burying them
inside generic calls, and must discover optional RERI support rather than
assuming it.

## Limits

The privileged ISA alone is not a complete platform contract. Interrupt
controllers, IOMMUs, CPU-start services, discovery data, and firmware calls are
specified separately and may be absent. This note makes no board or physical
platform recommendation.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
- [Bounded capture routine](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/bounded-capture-routine.md)
- [Double-fault guard](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/double-fault-guard.md)
