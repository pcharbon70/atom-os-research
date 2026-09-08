---
title: "Making No-Fuss Compiler Fuzzing Effective"
kind: source
created: "2026-09-08"
authors: ["Alex Groce","Rijnard van Tonder","Goutamkumar Tulajappa Kalburgi","Claire Le Goues"]
published: 2022
citation_key: "groce-et-al-2022-no-fuss-compiler-fuzzing"
container: "31st ACM SIGPLAN International Conference on Compiler Construction (CC '22), pp. 194–204"
edition: null
isbn: null
doi: "10.1145/3497776.3517765"
url: "https://agroce.github.io/cc22.pdf"
accessed: "2026-09-08"
tags: [zig, kernel-language, interoperability]
aliases: []
---

# Making No-Fuss Compiler Fuzzing Effective

## Reference

Alex Groce; Rijnard van Tonder; Goutamkumar Tulajappa Kalburgi; Claire Le Goues. *Making No-Fuss Compiler Fuzzing Effective*. 31st ACM SIGPLAN International Conference on Compiler Construction (CC '22), pp. 194–204.
2022. [Primary source](https://agroce.github.io/cc22.pdf).
DOI: [10.1145/3497776.3517765](https://doi.org/10.1145/3497776.3517765).


## Research question or contribution

What evidence does this work provide for Zig kernel development or a C fallback?

## Method

Peer-reviewed paper; read mutation/splicing method, controlled evaluation, Zig results and limitations. Zig received three configurations with fourteen single-core 24-hour trials each.

## Findings

Syntax-aware splicing found more distinct historical Zig compiler crashes than baseline AFL. Uniqueness required manual expert classification; crash discovery is not generated-program correctness testing.

## Relevance

Retain minimized compiler regressions and test critical code generation independently when selecting or upgrading a compiler.

## Limits

Older compiler revision; not a measurement of 0.16.0 defect rates, kernel safety or comparative language security.

## Derived work

- [Zig kernel feasibility and C interoperability](../20-notes/proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md)
