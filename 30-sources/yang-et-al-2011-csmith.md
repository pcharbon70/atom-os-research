---
title: "Finding and understanding bugs in C compilers"
kind: source
created: "2026-09-08"
authors: ["Xuejun Yang","Yang Chen","Eric Eide","John Regehr"]
published: 2011
citation_key: "yang-et-al-2011-csmith"
container: "PLDI 2011"
edition: null
isbn: null
doi: "10.1145/1993498.1993532"
url: "https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf"
accessed: "2026-09-08"
tags: [c-language, kernel-language, proof-of-concept]
aliases: []
---

# Finding and understanding bugs in C compilers

## Reference

Yang, Chen, Eide and Regehr. *Finding and Understanding Bugs in C Compilers.* PLDI 2011, pp. 283–294. [Author text](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf); [conference DOI](https://doi.org/10.1145/1993498.1993532).

## Research question or contribution

Can randomized differential testing expose defects missed by compiler regression suites?

## Method

Read introduction, generation/safety methods, coverage and evaluation. Csmith generates programs intended to avoid undefined/unspecified behavior, then compares compiled executions.

## Findings

The authors reported more than 325 previously unknown defects over three years. Voting is a heuristic for identifying the faulty implementation. CompCert defects occurred outside its verified middle end.

## Relevance

Retain minimized regressions and compare suitable pure-C components across compiler profiles.

## Limits

Historical compiler versions, not a current defect census. The evaluated generator excluded allocation, floating point, unions, recursion and function pointers. It did not establish interrupt, assembly or device correctness.

## Derived work

- [C kernel feasibility](../20-notes/proof-of-concept-requirements/c-kernel-language-feasibility-and-low-level-compatibility.md) — synthesis and qualification boundaries.
