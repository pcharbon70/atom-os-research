---
title: "Multiprogramming a 64 kB computer safely and efficiently"
kind: source
created: "2026-08-29"
authors:
  - "Amit Levy"
  - "Bradford Campbell"
  - "Branden Ghena"
  - "Daniel B. Giffin"
  - "Pat Pannuto"
  - "Prabal Dutta"
  - "Philip Levis"
published: 2017
citation_key: "levy-et-al-2017-tock"
container: "Proceedings of the 26th ACM Symposium on Operating Systems Principles"
edition: null
isbn: "978-1-4503-5085-3"
doi: "10.1145/3132747.3132786"
url: "https://tockos.org/assets/papers/tock-sosp2017.pdf"
accessed: "2026-08-29"
tags:
  - embedded-systems
  - memory-protection
  - mpu
  - operating-systems
  - resource-control
aliases:
  - "Tock SOSP 2017"
---

# Multiprogramming a 64 kB computer safely and efficiently

## Reference

Amit Levy et al. “Multiprogramming a 64 kB Computer Safely and Efficiently.”
*SOSP '17*, 2017. DOI
[10.1145/3132747.3132786](https://doi.org/10.1145/3132747.3132786).
[Project PDF](https://tockos.org/assets/papers/tock-sosp2017.pdf).

## Research question or contribution

Can an OS provide fault isolation, flexible concurrency, and dynamic
applications on a microcontroller with tens of kilobytes of memory and only an
MPU rather than an MMU?

## Method

Tock combines a type-safe kernel, MPU-isolated processes, capsules, grants, and
upcalls; the paper evaluates memory use, syscall and context-switch overhead,
and representative embedded applications.

## Findings

- MPU-based isolation is practical on constrained systems, but region counts,
  alignment, no virtual addressing, and per-switch reprogramming shape the
  process and allocation model.
- Language safety can compartmentalize cooperative kernel components while
  hardware protects untrusted processes. The two mechanisms provide different
  guarantees and compose rather than replace one another.
- Asynchronous upcalls and shared hardware virtualization fit event-driven
  embedded workloads, but callbacks and resource grants require explicit
  liveness and memory accounting.
- Resource scarcity makes static maxima and failure behavior first-class API
  concerns.

## Relevance

An MPU/PMP target should be a distinct constrained profile, not a claim that
the MMU design transparently scales down. It can reuse capability, endpoint,
driver, and supervision semantics while using fixed regions, physical
addresses, static pools, and stricter admission limits.

## Limits

Tock uses Rust and its own kernel architecture; its results do not validate
Zig memory safety or this project's actor runtime. Tested MCUs and applications
do not represent server-class SMP, IOMMU, or virtual-memory behavior.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
