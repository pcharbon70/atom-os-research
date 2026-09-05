---
title: "Linux pstore block oops/panic logger"
kind: source
created: "2026-09-05"
authors:
  - "The Linux kernel development community"
published: null
citation_key: "linux-kernel-community-2026-pstore-crash-backends"
container: "The Linux Kernel documentation"
edition: "Latest documentation accessed 2026-09-05"
isbn: null
doi: null
url: "https://docs.kernel.org/admin-guide/pstore-blk.html"
accessed: "2026-09-05"
tags:
  - crash-dumps
  - diagnostics
  - persistent-memory
  - ras
aliases:
  - "Linux pstore/blk crash backend"
---

# Linux pstore block oops/panic logger

## Reference

The Linux kernel development community. [*pstore block oops/panic
logger*](https://docs.kernel.org/admin-guide/pstore-blk.html), latest
documentation accessed 2026-09-05.

## Research question or contribution

What operational constraints arise when a failing kernel writes a bounded
record to a block-like persistent backend before reset?

## Method

The official pstore/blk panic-time driver contract, zone layout, overwrite
behavior, readback, and operation-result rules were inspected.

## Findings

- The pstore/blk panic contract forbids allocation, sleeping, ordinary locks,
  and interrupt-driven completion. Buffers and I/O mappings must be prepared
  during initialization; CPU-driven polling is preferred, and uncertain
  controller state can require reset.
- The block backend overwrites the oldest panic chunk when full and reports
  byte count or failure. This is a write-call/adapter-acceptance result, not a
  power-fail durability proof; durability remains unconfirmed until the
  media/controller-specific persistence contract supplies it.
- A persistent backend still depends on its controller, bus, mapping, power,
  and crash-time code.

## Relevance

Atom's `CrashSink` should be a capability profile with independently stated
`sealed-in-reserved-memory`, `accepted-by-adapter`, `durability-confirmed`, and
`recovered-on-next-boot` evidence. CPU-polled block I/O is an optional post-seal
adapter with its own response bounds, media ordering, overwrite policy, and
failure fallback; successful `panic_write` return establishes only adapter
acceptance. As an Atom architectural synthesis rather than a pstore/blk result,
reserved RAM is the smaller-dependency mandatory floor even when a richer
backend exists.

## Limits

The documentation describes Linux implementations, not a formal durability or
power-failure model. It does not authenticate records, encrypt them, establish
ordering to nonvolatile media on every platform, contain hostile DMA, or prove
that a failed controller can be reset safely. Online behavior can change after
the access date.

## Derived work

- [Crash-safe sink](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/crash-safe-sink.md)
- [Double-fault guard](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/double-fault-guard.md)
- [Architecture faults and diagnostics](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics.md)
