---
title: "C11 committee draft N1570"
kind: source
created: "2026-09-08"
authors: ["ISO/IEC JTC1/SC22/WG14"]
published: "2011-04-12"
citation_key: "wg14-2011-c11-committee-draft"
container: "WG14 committee documents"
edition: null
isbn: null
doi: null
url: "https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf"
accessed: "2026-09-08"
tags: [c-language, kernel-language, proof-of-concept]
aliases: []
---

# C11 committee draft N1570

## Reference

WG14. *Programming languages — C*, N1570, committee draft, 12 April 2011. [Public draft](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).

## Research question or contribution

What language and environment contracts can a freestanding C implementation rely on?

## Method

Read §4, §§5.1.2.1 and 5.1.2.4, and relevant §6 pointer, qualifier and expression rules.

## Findings

Freestanding execution need not have an operating system. Entry and extra library facilities are implementation-defined. Static-storage initialization precedes startup. The C11 minimum freestanding header set excludes stdatomic.h; atomic support is conditional. Volatile access is implementation-defined, and conflicting unsynchronized thread accesses can be undefined.

## Relevance

Separate portable algorithms from explicitly documented compiler, startup, memory and hardware contracts.

## Limits

This is a public C11 draft, not the purchased final standard or current C23 text. ISO threads do not by themselves specify kernel interrupt semantics.

## Derived work

- [C kernel feasibility](../20-notes/proof-of-concept-requirements/c-kernel-language-feasibility-and-low-level-compatibility.md) — synthesis and qualification boundaries.
