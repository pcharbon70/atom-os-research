---
title: "Clang 21 x86 interrupt attribute contract"
kind: source
created: "2026-09-08"
authors: ["LLVM Project contributors"]
published: 2025
citation_key: "llvm-project-2025-clang-x86-interrupt-contract"
container: "Clang documentation"
edition: "21.1.0"
isbn: null
doi: null
url: "https://releases.llvm.org/21.1.0/tools/clang/docs/AttributeReference.html#interrupt-x86"
accessed: "2026-09-08"
tags: [c-language, kernel-language, proof-of-concept]
aliases: []
---

# Clang 21 x86 interrupt attribute contract

## Reference

LLVM Project. *Attributes in Clang*, 21.1.0, “interrupt (X86).” [Versioned reference](https://releases.llvm.org/21.1.0/tools/clang/docs/AttributeReference.html#interrupt-x86).

## Research question or contribution

Can Clang generate hardware-interrupt entry/return conventions from C declarations?

## Method

Read x86 interrupt signatures, register preservation, permitted calls and error-code behavior.

## Findings

The attribute generates interrupt-specific return behavior and requires the matching frame/error-code parameters. Such handlers are not ordinary C call targets. Register-use and callee constraints remain part of the contract.

## Relevance

GCC and Clang support a similar mechanism, but the emitted instructions and reachable callees need independent checks.

## Limits

An accepted declaration or emitted iretq does not validate the IDT, stack mapping, nesting, state ownership or user return. Our empty compile-only handler deliberately establishes none of those.

## Derived work

- [C kernel feasibility](../20-notes/proof-of-concept-requirements/c-kernel-language-feasibility-and-low-level-compatibility.md) — synthesis and qualification boundaries.
