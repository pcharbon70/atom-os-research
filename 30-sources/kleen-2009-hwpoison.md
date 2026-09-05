---
title: "Linux hwpoison memory-failure handling design"
kind: source
created: "2026-09-05"
authors:
  - "Andi Kleen"
published: 2009
citation_key: "kleen-2009-hwpoison"
container: "The Linux Kernel documentation"
edition: "October 2009 design note; current copy accessed 2026-09-05"
isbn: null
doi: null
url: "https://docs.kernel.org/mm/hwpoison.html"
accessed: "2026-09-05"
tags:
  - fault-containment
  - hardware-errors
  - memory-management
  - ras
aliases:
  - "Linux hwpoison documentation"
---

# Linux hwpoison memory-failure handling design

## Reference

Andi Kleen. [*hwpoison*](https://docs.kernel.org/mm/hwpoison.html), October
2009; current copy in the Linux kernel documentation accessed 2026-09-05.

## Research question or contribution

How does a mature kernel turn some address-bearing machine-error reports into
page retirement and process-level containment, and where does that recovery
model stop?

## Method

This historical design note's memory-failure overview,
background-versus-consumed-error distinction,
early/late kill modes, injection interfaces, and documented limitations were
read as implementation precedent. Linux signals and VM internals are not
adopted as an Atom ABI.

## Findings

- Linux marks a reported physical page poisoned, prevents future use, locates
  mappings, and terminates affected processes. This composes error evidence
  with VM ownership; the machine-check handler alone cannot retire memory.
- The high-level path distinguishes background-detected corruption from data
  consumed by the current CPU. In the background case, failure of the
  best-effort recovery may be deferred until a later access raises another
  machine check; consumed corruption requires a stronger immediate response.
- Memory errors may arrive asynchronously with respect to ordinary VM users.
  The implementation therefore takes normal locks and may run for a long time;
  this work cannot be assumed safe in a bounded machine-check entry path.
- Early-kill and late-kill modes expose different notification timing. A
  specialized process may receive address-specific failure information, but
  most applications do not repair memory corruption themselves.
- Injection through `MADV_HWPOISON`, debugfs, or architecture-specific MCE
  tools exercises selected software paths. Software-unpoison is restricted to
  injected failures and is disabled once real hardware failure is observed.
- Not every page type is recoverable; the documentation explicitly excludes
  most kernel-internal objects. A physical address therefore enables a lookup,
  not a general proof that local containment is possible.

## Relevance

The architecture-fault classifier should emit a generation-bound
`ContainmentRequirement<MemoryExtent>` after capturing sufficient address and
consumption evidence. A VM/mapping/DMA coordinator outside hard entry must
retire mappings and the frame, stop affected domains, and return a joined
completion. Only that completion can justify continued service. Page identity,
mapping generation, requester set, poison-consumption state, and unsupported
page class must all remain explicit.

## Limits

This is an October 2009 Linux design note still hosted in the current
documentation, not proof of current implementation behavior or a controlled
research evaluation. It inherits the then-proposed Linux VM, signal, KVM, and
locking models. It does not prove containment for kernel memory, page-table
pages, DMA targets, persistent-memory writes, device caches, or arbitrary
platform reports. Current code and target experiments must corroborate any
implementation claim.

## Derived work

- [Containment classifier and promotion](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/containment-classifier-and-promotion.md)
- [Escalation channel](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/escalation-channel.md)
- [Architecture faults and diagnostics](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics.md)
