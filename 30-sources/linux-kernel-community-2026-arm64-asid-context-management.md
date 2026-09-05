---
title: "Linux arm64 ASID context management at bc35965f6940"
kind: source
created: "2026-09-04"
authors:
  - "Linux kernel community"
published: null
citation_key: "linux-kernel-community-2026-arm64-asid-context-management"
container: "Linux source tree"
edition: "bc35965f6940a9bf834d54187b6088b8eb09206d"
isbn: null
doi: null
url: "https://github.com/torvalds/linux/blob/bc35965f6940a9bf834d54187b6088b8eb09206d/arch/arm64/mm/context.c"
accessed: "2026-09-04"
tags:
  - aarch64
  - asid
  - linux
  - operating-systems
  - tlb
  - virtual-memory
aliases:
  - "Linux arm64 ASID allocator"
---

# Linux arm64 ASID context management at bc35965f6940

## Reference

Linux kernel community. [`arch/arm64/mm/context.c` at commit
`bc35965f6940a9bf834d54187b6088b8eb09206d`](https://github.com/torvalds/linux/blob/bc35965f6940a9bf834d54187b6088b8eb09206d/arch/arm64/mm/context.c),
accessed 4 September 2026.

## Documented mechanism

This source implements AArch64 address-space-identifier allocation and context
switching in Linux. It is code-level precedent for combining bounded hardware
ASIDs with a software generation, tracking per-CPU active and reserved values,
and coordinating generation rollover with deferred local invalidation.

## Findings

- The allocator discovers the implemented ASID width and uses a bitmap for the
  bounded numeric namespace.
- Software embeds a global generation alongside the hardware ASID; a context
  whose generation is current can reuse its numeric ASID without allocation.
- Per-CPU active and reserved ASIDs close races between context switches and a
  generation rollover. The implementation comments make the required atomic
  ordering part of the algorithm.
- On rollover, every CPU is marked for a TLB flush that it performs before
  installing a context in the new generation.
- The implementation limits pinned ASIDs so enough identifiers remain for CPUs
  to make progress.

## Relevance

This is mature implementation evidence for an Atom `ContextTagLease` with a
software generation, per-CPU installed-state ledger, explicit rollover, and a
capacity rule. The design should borrow the invariants, not Linux's internal
representation or its implicit integration assumptions.

## Limits

Source code is implementation precedent, not a formal proof or stable API.
The exact behavior is AArch64- and Linux-specific and must be read with the
pinned architecture manual and surrounding kernel code. Atom's CPU lifecycle,
failure containment, and completion tokens impose additional obligations;
this file alone does not prove them.

## Derived work

- [Translation-context allocator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/translation-context-allocator.md)
- [Address-space object](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/address-space-object.md)
