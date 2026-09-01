---
title: "EROS: A fast capability system"
kind: source
created: "2026-08-31"
authors:
  - "Jonathan S. Shapiro"
  - "Jonathan M. Smith"
  - "David J. Farber"
published: 1999
citation_key: "shapiro-et-al-1999-eros"
container: "Proceedings of the 17th ACM Symposium on Operating Systems Principles"
edition: null
isbn: "1-58113-140-2"
doi: "10.1145/319151.319163"
url: "https://www.princeton.edu/~rblee/ELE572Papers/Fall04Readings/Eros.pdf"
accessed: "2026-08-31"
tags:
  - capabilities
  - ipc
  - operating-systems
  - persistence
aliases:
  - "EROS capability system"
---

# EROS: A fast capability system

## Reference

Jonathan S. Shapiro, Jonathan M. Smith, and David J. Farber. “EROS: A Fast
Capability System.” *SOSP '99*, pages 170–185. DOI
[10.1145/319151.319163](https://doi.org/10.1145/319151.319163).
[Open PDF](https://www.princeton.edu/~rblee/ELE572Papers/Fall04Readings/Eros.pdf).

## Research question or contribution

Can a pure capability system with transparent persistence provide competitive
primitive performance on commodity processors?

## Method

EROS implements capability-only naming and invocation, protected pages and
capability nodes, user-level fault and storage allocation, software caching,
and a persistent single-level store. Microbenchmarks compare semantically
similar operations with Linux 2.2.5 on a 400 MHz Pentium II.

## Findings

- All resource access is through capabilities; entry capabilities combine a
  protected service reference with invocation authority.
- Capabilities are separated from ordinary writable data, preventing programs
  from forging authority by constructing bit patterns.
- Kernel objects were chosen to map closely to hardware-supported pages,
  mappings, and execution contexts, with less common representations cached or
  reconstructed.
- The microbenchmarks showed that capability invocation and protected subsystem
  composition need not be prohibitively slow.

## Relevance

EROS supports a kernel object model in which naming and authority are not
separate ambient mechanisms. It also supports user-level allocation and fault
policy. For this project, BEAM PIDs and service names should remain routing
identities above the kernel; possession of an endpoint capability should be the
authority to invoke.

## Limits

Application benchmarks and networking were absent from the evaluation, and the
hardware is historical. EROS placed bottom-half drivers and persistence inside
the kernel, enlarging the failure boundary relative to this project's goal.
Transparent checkpointing can also preserve corrupt state, so its persistence
model is evidence about capabilities, not the selected recovery architecture.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
