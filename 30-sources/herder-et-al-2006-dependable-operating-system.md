---
title: "Construction of a highly dependable operating system"
kind: source
created: "2026-08-31"
authors:
  - "Jorrit N. Herder"
  - "Herbert Bos"
  - "Ben Gras"
  - "Philip Homburg"
  - "Andrew S. Tanenbaum"
published: 2006
citation_key: "herder-et-al-2006-dependable-operating-system"
container: "Sixth European Dependable Computing Conference"
edition: null
isbn: "0-7695-2648-9"
doi: "10.1109/EDCC.2006.7"
url: "https://research.vu.nl/en/publications/construction-of-a-highly-dependable-operating-system"
accessed: "2026-08-31"
tags:
  - device-drivers
  - fault-containment
  - microkernels
  - operating-systems
aliases:
  - "MINIX 3 dependable construction"
---

# Construction of a highly dependable operating system

## Reference

Jorrit N. Herder, Herbert Bos, Ben Gras, Philip Homburg, and Andrew S.
Tanenbaum. “Construction of a Highly Dependable Operating System.” *EDCC '06*,
2006. DOI [10.1109/EDCC.2006.7](https://doi.org/10.1109/EDCC.2006.7).
[Publication record](https://research.vu.nl/en/publications/construction-of-a-highly-dependable-operating-system).
[Open PDF](https://www.cs.vu.nl/~ast/Publications/Papers/edcc-2006.pdf).

## Research question or contribution

How does moving drivers and operating-system services into restricted user
processes change failure propagation and recovery in a UNIX-like system?

## Method

The authors restructure MINIX into a small microkernel plus isolated drivers
and servers, enumerate driver-to-kernel dependencies, replace them with IPC and
checked kernel operations, apply per-component privilege policies, and report
performance and dependability observations.

## Findings

- Address-space separation converts many driver memory faults from machine
  crashes into component exits.
- Each driver receives only declared IPC peers, kernel calls, memory, IRQs, and
  I/O-port ranges. Isolation without restricted authority would still permit a
  malfunctioning user driver to damage the system.
- The reincarnation server holds recovery and privilege-assignment authority
  outside the driver and can replace selected failed components.
- Kernel-originated interrupts become notifications processed by the user-mode
  driver.
- Restart is most effective for transient and relatively stateless failures.
  The paper explicitly reports that loss of a core server was usually fatal
  because too much state was lost.

## Relevance

Drivers, network stacks, storage services, and the BEAM runtime should be
separate domains with manifest-derived authority. A supervisor must be outside
the child boundary and retain independent CPU and memory. Restarting a domain is
not a state-recovery guarantee.

## Limits

The implementation and measurements are historical and focus heavily on
accidental driver faults. The paper does not provide malicious DMA containment,
general transparent recovery, or a capability derivation model. Its line-count
and performance comparisons are system-specific.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
