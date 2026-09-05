---
title: "Linux virtual-memory implementation contracts at bc35965f6940"
kind: source
created: "2026-09-04"
authors:
  - "Linux kernel community"
published: null
citation_key: "linux-kernel-community-2026-virtual-memory-implementation-contracts"
container: "Linux source tree and in-tree kernel documentation"
edition: "bc35965f6940a9bf834d54187b6088b8eb09206d"
isbn: null
doi: null
url: "https://github.com/torvalds/linux/tree/bc35965f6940a9bf834d54187b6088b8eb09206d"
accessed: "2026-09-04"
tags:
  - linux
  - memory-reclamation
  - operating-systems
  - tlb
  - user-access
  - virtual-memory
aliases:
  - "Linux VM implementation contracts"
---

# Linux virtual-memory implementation contracts at bc35965f6940

## Reference

Linux kernel community. Virtual-memory implementation and in-tree
documentation at source revision
`bc35965f6940a9bf834d54187b6088b8eb09206d`, accessed 4 September 2026:

- [`include/asm-generic/tlb.h`](https://github.com/torvalds/linux/blob/bc35965f6940a9bf834d54187b6088b8eb09206d/include/asm-generic/tlb.h)
  and [`mm/mmu_gather.c`](https://github.com/torvalds/linux/blob/bc35965f6940a9bf834d54187b6088b8eb09206d/mm/mmu_gather.c);
- [`include/linux/uaccess.h`](https://github.com/torvalds/linux/blob/bc35965f6940a9bf834d54187b6088b8eb09206d/include/linux/uaccess.h)
  and [`rust/kernel/uaccess.rs`](https://github.com/torvalds/linux/blob/bc35965f6940a9bf834d54187b6088b8eb09206d/rust/kernel/uaccess.rs);
- [`Documentation/mm/mmu_notifier.rst`](https://github.com/torvalds/linux/blob/bc35965f6940a9bf834d54187b6088b8eb09206d/Documentation/mm/mmu_notifier.rst),
  [`Documentation/mm/highmem.rst`](https://github.com/torvalds/linux/blob/bc35965f6940a9bf834d54187b6088b8eb09206d/Documentation/mm/highmem.rst),
  and [`Documentation/core-api/pin_user_pages.rst`](https://github.com/torvalds/linux/blob/bc35965f6940a9bf834d54187b6088b8eb09206d/Documentation/core-api/pin_user_pages.rst).

## Documented mechanism

These commit-pinned sources expose concrete contracts around the order of table teardown and
TLB flush, lockless software walkers, secondary device translations, partial
user copies, consuming user-range readers, temporary kernel mappings, and page
pins. They are read as one implementation family, not as a single stable API.

## Findings

- Linux removes page-table reachability, invalidates relevant translations,
  and only then frees queued pages; reversing that order can expose a reused
  frame through a stale translation.
- Table-page reclamation may need to wait for lockless software walkers in
  addition to the hardware invalidation path. The implementation explicitly
  distinguishes its IPI rendezvous from a general RCU grace period.
- MMU notifiers protect secondary translations such as IOMMU/device TLBs; CPU
  TLB completion alone cannot authorize reuse of a device-visible page.
- User-copy primitives can fault or partially complete. The Rust `UserSlice`
  interface tells callers to validate the copied value and not assume two
  reads of one user address return the same bytes.
- Local temporary mappings and page pins have context, ordering, duration, and
  partial-success rules. A pin stabilizes backing but does not freeze contents.

## Relevance

The implementation shows why Atom needs typed and separate gates for hardware
translations, software readers, DMA, and copy progress. It also provides
practical precedent for consuming user-range readers and lexically scoped
temporary mappings while leaving Atom free to choose a smaller interface.

## Limits

Linux code and documentation evolve and include compatibility constraints Atom
may not need. This note preserves one revision rather than claiming current
behavior for all releases. The behavior is not a proof, and architecture-
specific completion must still be checked against normative manuals and target
errata.

## Derived work

- [Reclamation gate](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/reclamation-gate.md)
- [Safe user-access helpers](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/safe-user-access-helpers.md)
- [Shootdown coordinator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/shootdown-coordinator.md)
