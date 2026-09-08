---
title: "Towards optimization-safe systems"
kind: source
created: "2026-09-08"
authors: ["Xi Wang","Nickolai Zeldovich","M. Frans Kaashoek","Armando Solar-Lezama"]
published: 2013
citation_key: "wang-et-al-2013-optimization-safe-systems"
container: "SOSP 2013"
edition: null
isbn: null
doi: "10.1145/2517349.2522728"
url: "https://people.csail.mit.edu/nickolai/papers/wang-stack.pdf"
accessed: "2026-09-08"
tags: [c-language, kernel-language, proof-of-concept]
aliases: []
---

# Towards optimization-safe systems

## Reference

Wang, Zeldovich, Kaashoek and Solar-Lezama. *Towards Optimization-Safe Systems: Analyzing the Impact of Undefined Behavior.* SOSP 2013, pp. 260–275. [Author text](https://people.csail.mit.edu/nickolai/papers/wang-stack.pdf); [DOI](https://doi.org/10.1145/2517349.2522728).

## Research question or contribution

When can undefined-behavior assumptions undermine defensive systems code?

## Method

Read the semantic model, pointer-overflow example, §4.6 limitations and §6 evaluation/Figure 9. Stack uses LLVM analysis and constraint solving.

## Findings

The study identified 160 developer-confirmed/fixed bugs, including 32 in Linux. Performing invalid arithmetic before checking its result can invalidate the intended guard.

## Relevance

Validate bounds before forming invalid pointers or overflowing signed expressions.

## Limits

The count is not 160 exploited vulnerabilities or present-day compiler bugs. The model omits some undefined behavior; approximations/timeouts miss cases, and redundant checks can produce false warnings.

## Derived work

- [C kernel feasibility](../20-notes/proof-of-concept-requirements/c-kernel-language-feasibility-and-low-level-compatibility.md) — synthesis and qualification boundaries.
