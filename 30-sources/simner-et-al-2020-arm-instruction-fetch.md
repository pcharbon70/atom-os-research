---
title: "ARMv8-A system semantics: Instruction fetch in relaxed architectures"
kind: source
created: "2026-08-30"
authors:
  - "Ben Simner"
  - "Shaked Flur"
  - "Christopher Pulte"
  - "Alasdair Armstrong"
  - "Jean Pichon-Pharabod"
  - "Luc Maranget"
  - "Peter Sewell"
published: 2020
citation_key: "simner-et-al-2020-arm-instruction-fetch"
container: "29th European Symposium on Programming"
edition: null
isbn: "978-3-030-44914-8"
doi: "10.1007/978-3-030-44914-8_23"
url: "https://www.cl.cam.ac.uk/~pes20/iflat/"
accessed: "2026-08-30"
tags:
  - aarch64
  - cache-maintenance
  - code-loading
  - formal-methods
  - instruction-fetch
aliases:
  - "Arm instruction-fetch semantics"
---

# ARMv8-A system semantics: Instruction fetch in relaxed architectures

## Reference

Ben Simner et al. “ARMv8-A System Semantics: Instruction Fetch in Relaxed
Architectures.” *ESOP 2020*, pages 626–655. DOI
[10.1007/978-3-030-44914-8_23](https://doi.org/10.1007/978-3-030-44914-8_23).
[Authors' project page and executable model](https://www.cl.cam.ac.uk/~pes20/iflat/).

## Research question or contribution

What may an Armv8-A processor execute after software writes new instructions,
given instruction caches, data caches, out-of-order fetch, prefetch, and
concurrent cores?

## Method

The authors develop operational and axiomatic models with Arm architects,
exercise self-modifying and cross-thread examples, provide executable test
oracles, and compare predictions with hardware observations.

## Findings

- Writing bytes to memory does not by itself publish executable instructions
  on every architecture. Data-cache clean, instruction-cache invalidation,
  completion barriers, instruction synchronization, and remote-core action may
  form one required protocol.
- The observable semantics cannot always abstract away the instruction/data
  cache distinction, even though most microarchitectural detail should remain
  hidden.
- Program loading, dynamic linking, JIT compilation, debugging, and kernel code
  patching all depend on this system-level contract.
- Executable models and litmus tests exposed ambiguity and even a hardware bug,
  showing why code publication cannot be left to folklore.

## Relevance

The architecture layer needs a first-class `CodePublication` transition. It
should own writable-to-executable sealing, cache maintenance, remote CPU
synchronization, migration exclusion, generation tracking, and retirement. A
runtime should request publication, not scatter cache instructions or infer
that ordinary release stores are enough.

## Limits

The work models Armv8-A rather than all architectures and has published errata.
It does not provide the kernel's authorization, W^X policy, code signature,
rollback, or quiescent reclamation mechanisms.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
