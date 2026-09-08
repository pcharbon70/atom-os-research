---
title: "Pragma Driven Shared Memory Parallelism in Zig by Supporting OpenMP Loop Directives"
kind: source
created: "2026-09-08"
authors: ["David Kacs","Joseph Lee","Justs Zarins","Nick Brown"]
published: 2024
citation_key: "kacs-et-al-2024-zig-openmp"
container: "SC24-W: Workshops of the International Conference for High Performance Computing, Networking, Storage and Analysis, pp. 930–938"
edition: null
isbn: null
doi: "10.1109/SCW63240.2024.00132"
url: "https://conferences.computer.org/sc-wpub/pdfs/SC-W2024-6oZmigAQfgJ1GhPL0yE3pS/555400a930/555400a930.pdf"
accessed: "2026-09-08"
tags: [zig, kernel-language, interoperability]
aliases: []
---

# Pragma Driven Shared Memory Parallelism in Zig by Supporting OpenMP Loop Directives

## Reference

David Kacs; Joseph Lee; Justs Zarins; Nick Brown. *Pragma Driven Shared Memory Parallelism in Zig by Supporting OpenMP Loop Directives*. SC24-W: Workshops of the International Conference for High Performance Computing, Networking, Storage and Analysis, pp. 930–938.
2024. [Primary source](https://conferences.computer.org/sc-wpub/pdfs/SC-W2024-6oZmigAQfgJ1GhPL0yE3pS/555400a930/555400a930.pdf).
DOI: [10.1109/SCW63240.2024.00132](https://doi.org/10.1109/SCW63240.2024.00132).
[Author preprint](https://arxiv.org/abs/2409.20148).

## Research question or contribution

What evidence does this work provide for Zig kernel development or a C fallback?

## Method

Peer-reviewed workshop paper; read compiler modifications, runtime integration and NAS benchmark evaluation on ARCHER2. It modified Zig 0.10.1.

## Findings

Generated code called LLVM libomp; translation and manual integration connected Zig with C/Fortran components. Performance varied by benchmark and comparison.

## Relevance

Concrete foreign-runtime integration evidence, while demonstrating that translation and integration require engineering.

## Limits

Hosted HPC, modified older compiler and AMD hardware: no current stock-Zig OpenMP promise, Nehalem result or kernel qualification. Use current official documentation, not its simplified safety background, for language semantics.

## Derived work

- [Zig kernel feasibility and C interoperability](../20-notes/proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md)
