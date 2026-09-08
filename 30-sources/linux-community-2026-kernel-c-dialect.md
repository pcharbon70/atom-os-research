---
title: "Linux kernel C dialect and compiler profile"
kind: source
created: "2026-09-08"
authors: ["Linux kernel development community"]
published: null
citation_key: "linux-community-2026-kernel-c-dialect"
container: "Linux documentation and tagged source"
edition: "Current documentation; Linux v6.12 source"
isbn: null
doi: null
url: "https://docs.kernel.org/process/programming-language.html"
accessed: "2026-09-08"
tags: [c-language, kernel-language, proof-of-concept]
aliases: []
---

# Linux kernel C dialect and compiler profile

## Reference

Linux kernel community. [Programming Language](https://docs.kernel.org/process/programming-language.html) and [Building Linux with Clang/LLVM](https://docs.kernel.org/kbuild/llvm.html). Tagged implementation: Linux v6.12 [root Makefile](https://github.com/torvalds/linux/blob/v6.12/Makefile) and [x86 Makefile](https://github.com/torvalds/linux/blob/v6.12/arch/x86/Makefile).

## Research question or contribution

What does a mature C kernel actually require beyond portable C?

## Method

Read language/extension and LLVM support documentation, and the tagged Makefile language, aliasing, overflow, register and red-zone flags.

## Findings

The documented C dialect is GNU C11, with extensions; GCC and Clang are supported. The tagged build constrains aliasing/overflow assumptions and x86 register use and placement. Backend support alone does not qualify every configuration.

## Relevance

A named C standard is only one part of an engineered kernel compilation contract.

## Limits

Linux flags, memory model and internal APIs are Linux-specific. They are evidence of feasibility, not an Atom configuration to copy wholesale or a stable reusable driver ABI.

## Derived work

- [C kernel feasibility](../20-notes/proof-of-concept-requirements/c-kernel-language-feasibility-and-low-level-compatibility.md) — synthesis and qualification boundaries.
