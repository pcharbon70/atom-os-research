---
title: "Off by two: a low-level compiler regression"
kind: source
created: "2026-09-08"
authors: ["Nick Desaulniers"]
published: "2020-04-06"
citation_key: "desaulniers-2020-off-by-two"
container: "Nick Desaulniers's blog"
edition: null
isbn: null
doi: null
url: "https://nickdesaulniers.github.io/blog/2020/04/06/off-by-two/"
accessed: "2026-09-08"
tags: [c-language, kernel-language, proof-of-concept]
aliases: []
---

# Off by two: a low-level compiler regression

## Reference

Nick Desaulniers. *Off by Two.* 6 April 2020. [Original article](https://nickdesaulniers.github.io/blog/2020/04/06/off-by-two/).

## Research question or contribution

What can a real low-level C/assembly debugging episode teach compiler qualification?

## Method

Read the boot-failure investigation, minimized boolean/assembly example and linked-fix account.

## Findings

An LLVM boolean-extension error interacted with Linux asm-goto/static-key address encoding and produced invalid addressing. Minimization and intermediate/generated-code comparison helped locate the defect.

## Relevance

Keep small architecture-boundary reproducers and regression tests for the exact compiler release.

## Limits

This was a historical, fixed issue, not evidence that Clang 21 has the same defect, or that GCC is universally safer.

## Derived work

- [C kernel feasibility](../20-notes/proof-of-concept-requirements/c-kernel-language-feasibility-and-low-level-compatibility.md) — synthesis and qualification boundaries.
