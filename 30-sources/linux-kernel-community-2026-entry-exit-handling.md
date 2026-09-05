---
title: "Linux entry and exit handling"
kind: source
created: "2026-09-05"
authors:
  - "The Linux kernel development community"
published: null
citation_key: "linux-kernel-community-2026-entry-exit-handling"
container: "The Linux Kernel documentation"
edition: "Latest documentation accessed 2026-09-05"
isbn: null
doi: null
url: "https://www.kernel.org/doc/html/latest/core-api/entry.html"
accessed: "2026-09-05"
tags:
  - exception-entry
  - interrupts
  - kernels
  - nmi
aliases:
  - "Linux entry/exit documentation"
---

# Linux entry and exit handling

## Reference

The Linux kernel development community. [*Entry/exit handling for exceptions,
interrupts, syscalls and KVM*](https://www.kernel.org/doc/html/latest/core-api/entry.html),
latest documentation accessed 2026-09-05.

## Research question or contribution

Which low-level entry phases must execute outside ordinary instrumentation and
context assumptions, especially for NMI-like machine-check and double-fault
paths?

## Method

The official entry-state, non-instrumentable code, ordinary interrupt, and NMI-
like exception rules were read as mature implementation discipline rather than
as portable ISA semantics.

## Findings

- Low-level assembly must establish a safe architectural state before calling
  ordinary language code; architecture-independent bookkeeping is not the
  first instruction of entry.
- Early entry and late exit regions are marked non-instrumentable because
  tracing, lock checking, RCU, and other helpers can assume context that has not
  yet been established or has already been torn down.
- NMI-like entries include machine checks and double faults on relevant
  architectures. They can arrive in contexts in which ordinary interrupt or
  scheduler assumptions are false and may nest.
- State transitions are ordered; invoking helpers before the matching entry
  state is established can itself create recursion or corrupted accounting.
- The documentation supplies a maintainable phase boundary, not a guarantee
  that arbitrary C, instrumentation, or memory remains safe after machine
  corruption.

## Relevance

Atom component 1 should own audited assembly leaves, component 2 should own
entry stacks/nesting/context tokens, and component 9 should receive only a
bounded raw-frame view after the minimum safe state exists. Capture and
recursive-guard code should be `noinstr`-equivalent, with generated call-graph
and disassembly checks excluding unapproved helpers.

## Limits

This is Linux implementation documentation. It does not define x86 IST, Arm
stack selection, RISC-V scratch-register behavior, Atom's language subset, or a
worst-case execution bound. Online text can change after the access date.

## Derived work

- [Bounded capture routine](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/bounded-capture-routine.md)
- [Double-fault guard](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/double-fault-guard.md)
