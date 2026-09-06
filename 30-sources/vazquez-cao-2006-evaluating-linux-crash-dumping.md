---
title: "Evaluating Linux kernel crash dumping mechanisms"
kind: source
created: "2026-09-05"
authors:
  - "Fernando Luis Vázquez Cao"
published: 2006
citation_key: "vazquez-cao-2006-evaluating-linux-crash-dumping"
container: "Proceedings of the 2006 Linux Symposium, Volume One"
edition: null
isbn: null
doi: null
url: "https://www.kernel.org/doc/ols/2006/ols2006v1-pages-153-176.pdf"
accessed: "2026-09-05"
tags:
  - crash-dumps
  - fault-injection
  - linux
  - reliability
aliases:
  - "Linux crash dump evaluation"
---

# Evaluating Linux kernel crash dumping mechanisms

## Reference

Fernando Luis Vázquez Cao. “Evaluating Linux Kernel Crash Dumping
Mechanisms.” *Proceedings of the 2006 Linux Symposium*, volume 1, pages
153–176, 2006. [Official conference
paper](https://www.kernel.org/doc/ols/2006/ols2006v1-pages-153-176.pdf).

## Research question or contribution

How should crash-dump mechanisms be tested so their success, completeness, and
accuracy are measured under representative execution and hardware conditions
rather than a single synthetic panic?

## Method

The paper describes the Linux Kernel Dump Test Tool, compares crash-dump
families, enumerates failure contexts, and reports faults found while varying
crash trigger, stack, interrupt state, DMA, machine load, CPU coordination, and
device state on Linux 2.6.16-era x86 systems.

## Findings

- Crash dumping is multistage: detect the crash, perform minimal machine
  shutdown, then capture the dump. Success in a late stage cannot repair missed
  detection or corrupted handoff evidence.
- Simple `panic` or null-dereference tests leave execution context, hardware
  condition, I/O load, interrupts, and DMA uncontrolled and can make materially
  different designs appear equally reliable.
- Stack overflow, corruption of stack-derived CPU identity, recursive page
  faults, lock state, nonresponsive CPUs, device state, and outstanding DMA can
  defeat a dump path.
- Per-CPU crash stacks, independent NMI paths, reserved memory, and a separately
  prepared capture environment reduce dependence on the failed kernel.
- Device shutdown and reinitialization after a crash are dangerous and must be
  minimized; capture completeness is still conditional on surviving hardware.
- A captured dump can be incomplete or inaccurate even when the export path
  returns success. Integrity and coverage require explicit checking.

## Relevance

Atom should define outcome classes for detection, local seal, terminal
handoff, sink acceptance, persistence, and recovered-on-next-boot instead of a
single crash-log success. Its test matrix must cross every capture phase with
stack corruption, nesting, masked interrupts, DMA, CPU loss, storage failure,
and load. The paper strongly supports independent stacks and storage but not a
claim that they survive arbitrary corruption.

## Limits

The platforms, kernel, and dump implementations are historical and mostly
x86-specific. The evaluation does not cover current Arm or RISC-V RAS,
confidential-computing modes, IOMMUs, persistent-memory ordering, or hostile
fault injection. Its methodology and failure modes remain relevant; its
measured success rates are not portable.

## Derived work

- [Bounded capture routine](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/bounded-capture-routine.md)
- [Crash-safe sink](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/crash-safe-sink.md)
- [Double-fault guard](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/double-fault-guard.md)
