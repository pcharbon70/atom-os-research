---
title: "Exploring C semantics and pointer provenance"
kind: source
created: "2026-09-08"
authors: ["Kayvan Memarian","Victor B. F. Gomes","Brooks Davis","Stephen Kell","Alexander Richardson","Robert N. M. Watson","Peter Sewell"]
published: 2019
citation_key: "memarian-et-al-2019-c-pointer-provenance"
container: "Proceedings of the ACM on Programming Languages 3 (POPL), Article 67"
edition: null
isbn: null
doi: "10.1145/3290380"
url: "https://www.cl.cam.ac.uk/~km569/exploring_provenance.pdf"
accessed: "2026-09-08"
tags: [c-language, kernel-language, proof-of-concept]
aliases: []
---

# Exploring C semantics and pointer provenance

## Reference

Memarian et al. *Exploring C Semantics and Pointer Provenance.* PACMPL 3 (POPL), Article 67, January 2019, 32 pages. [Author text](https://www.cl.cam.ac.uk/~km569/exploring_provenance.pdf); [DOI](https://doi.org/10.1145/3290380).

## Research question or contribution

How can C pointer semantics reconcile optimization with low-level implementation practices?

## Method

Read PVI/PNVI proposals, pointer/integer examples, Cerberus evaluation and shadow-memory experiment.

## Findings

The work distinguishes numeric addresses from allocation/lifetime-sensitive provenance. Candidate executable semantics and tests explore implementation behavior; a ten-benchmark SPEC experiment exposes practical modeling and instrumentation limits.

## Relevance

Document the assumptions behind direct maps, integer-pointer conversion, allocator reuse and tagged identities.

## Limits

These are 2019 proposals, not today's binding ISO rules or uniform GCC/Clang guarantees. Token collisions and incomplete library, assembly and allocator treatment limit the experiment. CHERI hardware protection is not supplied by the T7500.

## Derived work

- [C kernel feasibility](../20-notes/proof-of-concept-requirements/c-kernel-language-feasibility-and-low-level-compatibility.md) — synthesis and qualification boundaries.
