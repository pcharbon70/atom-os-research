---
title: "Live Objects All The Way Down: Removing the Barriers between Applications and Virtual Machines"
kind: source
created: "2026-09-04"
authors:
  - "Javier E. Pimás"
  - "Stefan Marr"
  - "Diego Garbervetsky"
published: "2023-12-28"
citation_key: "pimas-et-al-2023-live-objects-all-the-way-down"
container: "arXiv"
edition: null
isbn: null
doi: null
url: "https://arxiv.org/abs/2312.16973"
accessed: "2026-09-04"
tags:
  - live-programming
  - metacircular-runtime
  - smalltalk
  - virtual-machines
aliases:
  - "Live Metacircular Runtimes"
---

# Live Objects All The Way Down: Removing the Barriers between Applications and Virtual Machines

## Reference

Javier E. Pimás, Stefan Marr, and Diego Garbervetsky. “[Live Objects All The
Way Down: Removing the Barriers between Applications and Virtual
Machines](https://arxiv.org/abs/2312.16973).” arXiv:2312.16973, 28 December
2023.

## Research question or contribution

The paper asks whether virtual-machine components can inhabit the same live,
object-oriented environment as applications, reducing the conceptual and tool
barrier between application code and runtime implementation. It proposes Live
Metacircular Runtimes and implements Bee/LMR.

## Method

The authors report a 22,057-line live runtime for a Smalltalk-derivative
industrial environment and analyze case studies involving garbage-collector
tuning, JIT recompilation behavior, and SIMD optimization.

## Findings

- Runtime components such as the collector and JIT can be represented,
  inspected, debugged, and changed with high-level live tools.
- The approach shortens feedback loops and strengthens the causal connection
  between application behavior and VM implementation.
- Application developers can inspect runtime mechanisms without switching to a
  wholly separate low-level toolchain, while VM developers retain live-system
  facilities.
- The case studies demonstrate feasibility for a small production team; they
  do not establish safe end-user runtime modification or broad portability.

## Relevance

The result is contemporary evidence that Smalltalk's live-system ambition is
not only historical. For Atom OS it motivates reflective service protocols and
inspectable runtime components, but the privileged kernel and authority model
must remain protected. Live access should be capability-scoped, audited, and
transactional.

## Limits

The evaluation concerns one Smalltalk-derived runtime and expert developers.
It does not solve hostile-code isolation, distributed actor upgrades, ordinary
user learnability, or safe modification of a privileged OS substrate.

## Derived work

- [Alan Kay's Smalltalk visual interface and the modern desktop](../20-notes/alan-kay-smalltalk-visual-interface-and-modern-desktop.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
