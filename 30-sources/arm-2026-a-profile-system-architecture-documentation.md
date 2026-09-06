---
title: "Arm A-profile system architecture documentation"
kind: source
created: "2026-08-30"
authors:
  - "Arm Limited"
published: 2026
citation_key: "arm-2026-a-profile-system-architecture-documentation"
container: "Arm Architecture Reference Manual for A-profile architecture"
edition: "Issue M.c"
isbn: null
doi: null
url: "https://developer.arm.com/documentation/ddi0487/mc/"
accessed: "2026-09-05"
tags:
  - arm64
  - cpu-architecture
  - hardware-errors
  - interrupts
  - memory-ordering
  - privilege
  - virtual-memory
aliases:
  - "Arm A-profile architecture reference manual"
---

# Arm A-profile system architecture documentation

## Reference

Arm Limited. *Arm Architecture Reference Manual for A-profile architecture*,
Issue M.c.
[Official versioned manual](https://developer.arm.com/documentation/ddi0487/mc/).

## Research question or contribution

Which AArch64 architectural semantics shape a kernel's privileged entry,
context, translation, ordering, cache, timer, and optional virtualization
contracts?

## Method

The architecture reference manual was treated as the normative source. The
analysis focuses on architectural effects visible to kernel code, not SoC
selection, board wiring, firmware implementation, or peripheral protocols.

## Findings

- Exception levels and exception classes define explicit privilege and entry
  transitions. Saved program state, exception link state, stack selection, and
  vector layout must be normalized before common kernel handling and validated
  on return.
- Translation regimes, ASIDs, stage-1/stage-2 translation, break-before-make
  requirements, TLBI operations, and barriers form a mapping-update protocol;
  changing a page-table word alone is not the complete operation.
- Arm's relaxed memory model requires explicit ordering chosen for the relevant
  shareability and access domain. Device accesses, normal memory, and DMA
  visibility cannot be represented by one undifferentiated fence.
- Data-cache cleaning, instruction-cache invalidation, and synchronization
  barriers make publishing generated or newly loaded executable code an
  ordered transition, potentially involving other processing elements.
- The generic timer provides architectural counters and timer facilities that
  can back a raw clock and per-CPU deadlines, while time policy and timer queues
  can remain architecture-neutral.
- Floating-point/SIMD, SVE, SME, debug, performance-monitoring, pointer
  authentication, and memory-tagging features enlarge or qualify execution
  context and should be exposed through discovered feature profiles.
- SError delivery, exception synchronization, optional RAS features, and
  double-fault routing do not provide one universal recovery meaning.
- AArch64 vector selection distinguishes origin, exception level, and use of
  `SP_EL0` versus `SP_ELx`; it is not an x86-style independently selected stack
  for every vector.

## Relevance

Arm makes several implicit-looking operations observably multi-step. The
kernel layer therefore needs transactional mapping, code-publication, and
context-state contracts whose completion points include the necessary cache,
TLB, and remote-core synchronization. A port must preserve architectural
validity and precision while pinning the exact feature/firmware profile that
justifies any return or containment claim. It also needs an early preallocated
software stack strategy and must save overwrite-prone entry state before a
higher-priority exception can replace it.

## Limits

The manual defines an architecture family with many optional extensions and
implementation-defined properties. A concrete port must record the exact
architecture version, features, errata, interrupt controller, and firmware
interface it assumes. This source does not evaluate those implementations.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
- [Bounded capture routine](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/bounded-capture-routine.md)
- [Double-fault guard](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/double-fault-guard.md)
