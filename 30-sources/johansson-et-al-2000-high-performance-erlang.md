---
title: "A high performance Erlang system"
kind: source
created: "2026-09-03"
authors:
  - "Erik Johansson"
  - "Mikael Pettersson"
  - "Konstantinos Sagonas"
published: 2000
citation_key: "johansson-et-al-2000-hipe"
container: "2nd ACM SIGPLAN International Conference on Principles and Practice of Declarative Programming"
edition: "PPDP '00, 32-43"
isbn: null
doi: "10.1145/351268.351273"
url: "https://doi.org/10.1145/351268.351273"
accessed: "2026-09-03"
tags:
  - beam
  - erlang
  - native-compilation
  - virtual-machines
aliases:
  - "HiPE"
---

# A high performance Erlang system

## Reference

Erik Johansson, Mikael Pettersson, and Konstantinos Sagonas. “[A High
Performance Erlang System](https://doi.org/10.1145/351268.351273).” *2nd ACM
SIGPLAN International Conference on Principles and Practice of Declarative
Programming*, pages 32–43, 2000.

## Research question or contribution

The paper presents the HiPE native-code compiler and its integration with an
Erlang runtime, asking how native execution can improve sequential code while
retaining concurrency, exceptions, garbage collection, and interoperability
with interpreted code.

## Method

The authors describe compiler and runtime changes, mixed interpreted/native
calls, native stack and garbage-collection support, and benchmark the system
against the contemporary BEAM implementation.

## Findings

- Native compilation can materially improve selected Erlang kernels when the
  runtime supplies correct calling, root, exception, and process interfaces.
- Mixed execution creates transition paths and metadata that are part of the
  trusted runtime, not a free optimization layer.
- Speedups are workload-dependent; code dominated by messaging, allocation,
  tables, or I/O may not benefit like sequential kernels.

## Relevance

HiPE demonstrates that an optimized tier must preserve the managed-runtime
contract at every safe point. It also provides contrast with the later
BeamAsm choice to translate every loaded module simply and avoid mixed-mode
complexity. Atom OS should measure both code speed and system-level latency,
memory, upgrade, and assurance costs.

## Limits

The compiler, VM, hardware, and benchmarks are more than two decades old and
do not predict current OTP or Atom OS. The paper does not address capability
boundaries, W^X publication, deterministic replay, or kernel CPU budgets.

## Derived work

- [Code execution, safe points, and version publication](../20-notes/managed-actor-runtime-components/code-execution-safe-points-and-version-publication.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
