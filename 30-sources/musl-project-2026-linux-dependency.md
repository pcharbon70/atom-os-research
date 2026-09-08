---
title: "musl and its Linux syscall dependency"
kind: source
created: "2026-09-08"
authors: ["musl project"]
published: null
citation_key: "musl-project-2026-linux-dependency"
container: "musl project documentation"
edition: "About page accessed 2026-09-08"
isbn: null
doi: null
url: "https://musl.libc.org/about.html"
accessed: "2026-09-08"
tags: [zig, kernel-language, interoperability]
aliases: []
---

# musl and its Linux syscall dependency

## Reference

musl project. *About musl*. Publication date unspecified.
[Primary page](https://musl.libc.org/about.html).


## Research question or contribution

What evidence does this work provide for Zig kernel development or a C fallback?

## Method

Read the official platform and implementation description.

## Findings

musl is a C library built on the Linux system-call API.

## Relevance

A statically linked Linux/musl executable cannot be assumed to run on Atom merely because its machine code and C calling convention match.

## Limits

This is a platform-dependency fact, not a comparative libc benchmark. No Linux syscall-emulation layer is proposed for the PoC.

## Derived work

- [Zig kernel feasibility and C interoperability](../20-notes/proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md)
