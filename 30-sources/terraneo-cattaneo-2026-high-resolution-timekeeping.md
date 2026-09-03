---
title: "Efficient design of high-resolution timekeeping in real-time operating systems"
kind: source
created: "2026-09-02"
authors:
  - "Federico Terraneo"
  - "Daniele Cattaneo"
published: 2026
citation_key: "terraneo-cattaneo-2026-high-resolution-timekeeping"
container: "7th Workshop on Next Generation Real-Time Embedded Systems"
edition: null
isbn: null
doi: "10.4230/OASIcs.NG-RES.2026.4"
url: "https://drops.dagstuhl.de/entities/document/10.4230/OASIcs.NG-RES.2026.4"
accessed: "2026-09-02"
tags:
  - embedded-systems
  - multicore
  - real-time
  - scheduling
  - timekeeping
aliases:
  - "1+N timing subsystem"
---

# Efficient design of high-resolution timekeeping in real-time operating systems

## Reference

Federico Terraneo and Daniele Cattaneo. “Efficient Design of High-Resolution
Timekeeping in Real-Time Operating Systems.” *7th Workshop on Next Generation
Real-Time Embedded Systems (NG-RES 2026)*, Article 4. DOI
[10.4230/OASIcs.NG-RES.2026.4](https://doi.org/10.4230/OASIcs.NG-RES.2026.4).

## Research question or contribution

Can an embedded real-time kernel retain high-resolution, tickless time while
removing time conversion and shared-timer work from the context-switch path?

## Method

The authors compare a periodic-tick design, a conventional high-resolution
single-timer design, and a proposed “1+N” design: one shared high-resolution
timekeeping/wakeup timer plus one local preemption timer per CPU. They implement
the designs in the Miosix kernel and report a synthetic maximum-context-switch
rate on an STM32F469 and a dual-core RP2040.

## Findings

- A periodic tick couples time resolution to interrupt overhead and can lose
  time if interrupts remain disabled across multiple tick periods.
- A free-running counter plus match/compare facility supports high-resolution
  time reads and event-driven wakeups; narrow counters still require software
  extension across wrap.
- A tickless timer should be programmed for the earliest pending event rather
  than interrupting at a fixed rate when no work is due.
- The proposed 1+N design separates the globally meaningful timebase from
  per-CPU preemption deadlines. This avoids repeating general time conversion
  in the measured scheduler path.
- The preliminary experiment reports higher context-switch rates for 1+N than
  for the conventional high-resolution design on both tested microcontrollers.
  The paper does not establish an end-to-end response-time bound.

## Relevance

The result supports an interface with a globally qualified counter domain and
CPU-local one-shot deadline channels. It also warns against embedding scheduler
quantum policy into the raw-time component. Atom OS can multiplex wakeups,
budget expiry, and runtime scheduling above the architecture layer while the
backend supplies only measurement and one-shot programming.

## Limits

The measurements are preliminary, synthetic, and limited to two small
microcontroller platforms, one with only two cores. Miosix's scheduler and
hardware timer inventory differ from a capability microkernel on x86-64,
AArch64, or server-class RISC-V. The paper's 1+N allocation is useful precedent,
not evidence that every target needs a physically separate global timer.

## Derived work

- [Raw time and deadline programming](../20-notes/kernel-hardware-and-architecture-components/raw-time-and-deadline-programming.md)
