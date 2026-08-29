---
title: "Improving the reliability of commodity operating systems"
kind: source
created: "2026-08-29"
authors:
  - "Michael M. Swift"
  - "Brian N. Bershad"
  - "Henry M. Levy"
published: 2003
citation_key: "swift-et-al-2003-nooks"
container: "Proceedings of the 19th ACM Symposium on Operating Systems Principles"
edition: null
isbn: "1-58113-757-5"
doi: "10.1145/1165389.945466"
url: "https://nooks.cs.washington.edu/nooks-sosp.pdf"
accessed: "2026-08-29"
tags:
  - device-drivers
  - fault-containment
  - operating-systems
  - recovery
  - reliability
aliases:
  - "Nooks reliability subsystem"
---

# Improving the reliability of commodity operating systems

## Reference

Michael M. Swift, Brian N. Bershad, and Henry M. Levy. “Improving the
Reliability of Commodity Operating Systems.” *SOSP '03*, 2003. DOI
[10.1145/1165389.945466](https://doi.org/10.1145/1165389.945466).
[Project PDF](https://nooks.cs.washington.edu/nooks-sosp.pdf).

## Research question or contribution

Can a compatibility-oriented subsystem isolate and recover faulty kernel
extensions, especially device drivers, without redesigning the whole OS or
rewriting existing C drivers?

## Method

Nooks places extensions in lightweight kernel protection domains, interposes
kernel calls, tracks resources for cleanup, and evaluates performance and
2,000 injected faults across several Linux extensions.

## Findings

- Drivers were a major historical failure source, and page protection plus
  interposition prevented many extension faults from corrupting the kernel.
- The reported tests automatically recovered from 99 percent of injected
  faults that otherwise crashed Linux, but containment was deliberately
  incomplete for compatibility.
- Recovery requires a resource ledger, not only a fault boundary. References,
  allocations, registrations, interrupts, and device state must be cleaned or
  reconstructed.
- Running code in privileged mode with restricted mappings reduces some damage
  but is weaker than an unprivileged driver domain with DMA and MMIO authority
  explicitly constrained.

## Relevance

Driver restart should be designed with a generation-tagged ownership ledger
from the start. On failure the kernel must mask interrupts, stop DMA, reset or
quarantine the device, revoke mappings and capabilities, reclaim buffers, and
report what could not be proven clean to a supervisor.

## Limits

The paper evaluates an old Linux and compatibility design. Its fault injector
does not cover every malicious behavior, device firmware failure, DMA race, or
modern side channel, and recovery percentages must not be generalized.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
