---
title: "What every C programmer should know about undefined behavior"
kind: source
created: "2026-09-08"
authors: ["Chris Lattner"]
published: "2011-05-13"
citation_key: "lattner-2011-c-undefined-behavior"
container: "LLVM Project Blog"
edition: null
isbn: null
doi: null
url: "https://blog.llvm.org/2011/05/what-every-c-programmer-should-know.html"
accessed: "2026-09-08"
tags: [c-language, kernel-language, proof-of-concept]
aliases: []
---

# What every C programmer should know about undefined behavior

## Reference

Chris Lattner. *What Every C Programmer Should Know About Undefined Behavior #1/3.* LLVM Project Blog, 13 May 2011. [Original article](https://blog.llvm.org/2011/05/what-every-c-programmer-should-know.html).

## Research question or contribution

Why can optimizing C differ from the programmer's machine-instruction intuition?

## Method

Read the compiler author's explanation and examples of overflow, shifts, invalid access and alias analysis.

## Findings

Undefined operations permit transformations that violate a naive wrapping-address model. Specific switches such as fwrapv do not repair unrelated semantic errors.

## Relevance

Useful explanatory companion to empirical work and current versioned compiler contracts.

## Limits

Historical engineering explanation, not a normative standard, measured Atom performance or memory-safety guarantee. Historical volatile-null advice and performance estimates are not adopted.

## Derived work

- [C kernel feasibility](../20-notes/proof-of-concept-requirements/c-kernel-language-feasibility-and-low-level-compatibility.md) — synthesis and qualification boundaries.
