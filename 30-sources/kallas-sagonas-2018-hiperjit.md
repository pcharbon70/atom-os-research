---
title: "HiPErJiT: A profile-driven just-in-time compiler for Erlang"
kind: source
created: "2026-09-03"
authors:
  - "Konstantinos Kallas"
  - "Konstantinos Sagonas"
published: 2018
citation_key: "kallas-sagonas-2018-hiperjit"
container: "30th Symposium on Implementation and Application of Functional Languages"
edition: "IFL 2018, 25-36"
isbn: "978-1-4503-7143-8"
doi: "10.1145/3310232.3310234"
url: "https://doi.org/10.1145/3310232.3310234"
accessed: "2026-09-03"
tags:
  - beam
  - code-loading
  - erlang
  - just-in-time-compilation
  - virtual-machines
aliases:
  - "HiPErJiT"
---

# HiPErJiT: A profile-driven just-in-time compiler for Erlang

## Reference

Konstantinos Kallas and Konstantinos Sagonas. “[HiPErJiT: A Profile-Driven
Just-in-Time Compiler for Erlang](https://doi.org/10.1145/3310232.3310234).”
*30th Symposium on Implementation and Application of Functional Languages*,
pages 25–36, 2018. [Author-hosted
paper](https://angelhof.github.io/files/papers/hiperjit-2018-ifl.pdf).

## Research question or contribution

The work asks whether runtime profiles can select Erlang modules and functions
for HiPE native compilation, inlining, and type specialization while retaining
tail calls and module-level hot code loading.

## Method

The authors integrate profiling and HiPE compilation into Erlang/OTP, describe
the compilation and code-replacement path, and compare HiPErJiT with BEAM,
ahead-of-time HiPE, and Pyrlang across their benchmark set.

## Findings

- In the reported experiments, HiPErJiT was roughly twice as fast as the then
  BEAM baseline and approached HiPE despite profiling and compilation costs;
  profile-driven specialization surpassed HiPE on some programs.
- Preserving tail-call optimization and hot module replacement materially
  constrains native-code design; execution speed is not the only contract.
- Profiling overhead ends for a module once it is selected and compiled in the
  prototype, but the authors identify overhead as a concern for lifelong
  feedback-directed optimization.
- The result shows a viable sophisticated tier, not that adaptive compilation
  is always superior. Modern BeamAsm later chose simple whole-module load-time
  translation to avoid tier switching and optimizer complexity.

## Relevance

HiPErJiT provides positive and negative evidence for Atom OS. Native lowering
can preserve important Erlang behavior, but profiles, deoptimization state,
compiler memory, hot-code generations, roots, and publication add failure and
latency surface. The recommended sequence is therefore an auditable
interpreter, then simple whole-module load-time translation, with adaptive
optimization only if measured workloads justify the additional trusted state.

## Limits

The comparison predates current BeamAsm and current OTP workloads, and the
benchmarks do not include the Atom OS kernel boundary, W^X publication,
reproducible failure injection, or hard memory/CPU accounts. Reported speedups
must not be carried forward as target predictions.

## Derived work

- [Code execution, safe points, and version publication](../20-notes/managed-actor-runtime-components/code-execution-safe-points-and-version-publication.md)
- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
