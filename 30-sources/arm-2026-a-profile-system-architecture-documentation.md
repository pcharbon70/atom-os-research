---
title: "Arm A-profile system architecture documentation"
kind: source
created: "2026-08-30"
authors:
  - "Arm Limited"
published: 2026
citation_key: "arm-2026-a-profile-system-architecture-documentation"
container: "Arm Architecture Reference Manual for A-profile architecture"
edition: "Latest documentation accessed 2026-08-30"
isbn: null
doi: null
url: "https://developer.arm.com/documentation/ddi0487/latest/"
accessed: "2026-08-30"
tags:
  - arm64
  - cpu-architecture
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
latest version available 2026-08-30.
[Official manual](https://developer.arm.com/documentation/ddi0487/latest/).

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

## Relevance

Arm makes several implicit-looking operations observably multi-step. The
kernel layer therefore needs transactional mapping, code-publication, and
context-state contracts whose completion points include the necessary cache,
TLB, and remote-core synchronization.

## Limits

The manual defines an architecture family with many optional extensions and
implementation-defined properties. A concrete port must record the exact
architecture version, features, errata, interrupt controller, and firmware
interface it assumes. This source does not evaluate those implementations.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
