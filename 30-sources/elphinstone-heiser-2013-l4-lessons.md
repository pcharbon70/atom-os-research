---
title: "From L3 to seL4: What have we learnt in 20 years of L4 microkernels?"
kind: source
created: "2026-08-30"
authors:
  - "Kevin Elphinstone"
  - "Gernot Heiser"
published: 2013
citation_key: "elphinstone-heiser-2013-l4-lessons"
container: "Proceedings of the 24th ACM Symposium on Operating Systems Principles"
edition: null
isbn: "978-1-4503-2388-8"
doi: "10.1145/2517349.2522720"
url: "https://eecs582.github.io/readings/l3-20years.pdf"
accessed: "2026-08-30"
tags:
  - capabilities
  - interrupts
  - microkernels
  - operating-systems
  - portability
  - virtual-memory
aliases:
  - "Twenty years of L4 lessons"
---

# From L3 to seL4: What have we learnt in 20 years of L4 microkernels?

## Reference

Kevin Elphinstone and Gernot Heiser. “From L3 to seL4: What Have We Learnt in
20 Years of L4 Microkernels?” *SOSP '13*, pages 133–150, 2013. DOI
[10.1145/2517349.2522720](https://doi.org/10.1145/2517349.2522720).
[Open PDF](https://eecs582.github.io/readings/l3-20years.pdf).

## Research question or contribution

Which L4 design principles survived two decades of reimplementation,
deployment, architecture ports, performance work, and formal verification?

## Method

The authors compare several L4 generations and implementations, revisiting
minimality, IPC, address spaces, capabilities, scheduling, user-level drivers,
kernel execution structure, portability, and implementation language.

## Findings

- Minimal general mechanisms and fast protected communication remained durable;
  several policy-bearing mechanisms, including rigid process hierarchies, did
  not.
- Modern L4 systems normally keep ordinary device drivers outside the kernel,
  while a small interrupt-controller and timer mechanism remains privileged so
  the kernel can route events safely.
- Interrupt delivery evolved toward asynchronous notification because forcing a
  synchronous thread model onto every interrupt source complicated servers and
  kernel implementation.
- Capability-mediated authority replaced several implicit or hierarchical
  resource-control schemes. The seL4 approach also makes kernel objects and the
  memory backing them explicit to improve isolation and reasoning.
- Portability is not an all-or-nothing property. The paper reports substantial
  architecture-neutral code in some L4 implementations, while noting that
  virtual-memory code remains heavily architecture-specific and critical paths
  may still need tailored implementations.
- Later kernels reduced assembly to small entry paths and measured fast paths;
  maintainability and verification outweighed non-standard calling conventions
  and whole-kernel assembly.

## Relevance

The kernel hardware layer should preserve architecture-specific knowledge where
the semantics really differ, but expose small common contracts for events,
address spaces, and CPU-local operations. Interrupts should become typed,
capability-authorized notifications above the controller backend. Architecture
portability should be judged by contract stability and bounded port surface,
not by forcing identical low-level code.

## Limits

This is a retrospective by principal L4 researchers, not a controlled
comparison of all kernel architectures. Several measurements and hardware
assumptions are historical, and the paper does not prescribe an OTP-inspired
runtime or this project's exact kernel boundary.

## Derived work

- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
