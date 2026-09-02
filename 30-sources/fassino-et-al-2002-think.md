---
title: "Think: A software framework for component-based operating system kernels"
kind: source
created: "2026-09-02"
authors:
  - "Jean-Philippe Fassino"
  - "Jean-Bernard Stefani"
  - "Julia Lawall"
  - "Gilles Muller"
published: 2002
citation_key: "fassino-et-al-2002-think"
container: "2002 USENIX Annual Technical Conference"
edition: null
isbn: null
doi: null
url: "https://www.usenix.org/conference/2002-usenix-annual-technical-conference/think-software-framework-component-based"
accessed: "2026-09-02"
tags:
  - component-architecture
  - interfaces
  - operating-systems
  - portability
  - type-safety
aliases:
  - "Think component framework"
---

# Think: A software framework for component-based operating system kernels

## Reference

Jean-Philippe Fassino, Jean-Bernard Stefani, Julia Lawall, and Gilles Muller.
“Think: A Software Framework for Component-based Operating System Kernels.”
*2002 USENIX Annual Technical Conference*.
[USENIX record and paper](https://www.usenix.org/conference/2002-usenix-annual-technical-conference/think-software-framework-component-based).

## Research question or contribution

Can strongly typed components and explicit bindings support reusable kernel
construction without forcing every system into one kernel architecture or
adding material overhead?

## Method

Think defines components, typed client/server interfaces, bindings, names, and
domains, then implements the Kortex component library and several assembled
kernels. The evaluation compares componentized paths and specialized systems
on the paper's PowerPC platform.

## Findings

- Components interact only through named, strongly typed interfaces; bindings
  can be constructed only between compatible interface types.
- Domains identify resource and protection boundaries, while bindings can
  cross a boundary through an explicit composite path.
- Hardware facilities such as exceptions, the MMU, and controllers are exposed
  through separate HAL components rather than one undifferentiated interface.
- Binding structure is itself explicit and composable, which makes local calls,
  system calls, and remote interactions variations of a described connection
  rather than hidden calling convention changes.
- The reported experiments show that systematic componentization need not add
  measurable overhead in those configurations, but the framework permits more
  runtime flexibility than a small verified kernel may want.

## Relevance

The typed architecture facade should be divided by semantic family and should
make its binding, context, and completion mode explicit. Static composition is
the recommended baseline for Atom OS; Think supports the value of typed
boundaries without requiring its runtime component model.

## Limits

The language, target, hardware, and measurements are historical. Strongly typed
function signatures do not establish authority, lifetime, temporal isolation,
memory safety of unsafe implementations, or correct weak-memory/DMA behavior.
Dynamic rebinding would also enlarge the trusted state machine and is not
justified for the first kernel.

## Derived work

- [Typed kernel-facing architecture facade](../20-notes/typed-kernel-facing-architecture-facade.md)
- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
