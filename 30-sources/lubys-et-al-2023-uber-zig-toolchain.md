---
title: "Bootstrapping Uber's Infrastructure on arm64 with Zig"
kind: source
created: "2026-09-08"
authors: ["Laurynas Lubys","Motiejus Jakštys","Neringa Lukoševičiūtė"]
published: "2023-05-03"
citation_key: "lubys-et-al-2023-uber-zig-toolchain"
container: "Uber Engineering"
edition: null
isbn: null
doi: null
url: "https://www.uber.com/gb/en/blog/bootstrapping-ubers-infrastructure-on-arm64-with-zig/"
accessed: "2026-09-08"
tags: [zig, kernel-language, interoperability]
aliases: []
---

# Bootstrapping Uber's Infrastructure on arm64 with Zig

## Reference

Laurynas Lubys; Motiejus Jakštys; Neringa Lukoševičiūtė. *Bootstrapping Uber's Infrastructure on arm64 with Zig*. Uber Engineering.
2023-05-03. [Primary source](https://www.uber.com/gb/en/blog/bootstrapping-ubers-infrastructure-on-arm64-with-zig/).


## Research question or contribution

What evidence does this work provide for Zig kernel development or a C fallback?

## Method

First-party engineering article; read adoption, hermetic-build failures and the explicit distinction between compiler-toolchain and language use.

## Findings

Authors report production use of Zig's C/C++ toolchain for their Go monorepo, following dependency and build fixes. They explicitly did not claim production application adoption of Zig-the-language at that time.

## Relevance

Industrial evidence for the C toolchain and dependency-closure discipline.

## Limits

Hosted infrastructure, not a freestanding kernel or an independent ABI conformance study. The article's toolchain packaging descriptions are historical.

## Derived work

- [Zig kernel feasibility and C interoperability](../20-notes/proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md)
