---
title: "Zig C translator: bitfields and unsupported statements"
kind: source
created: "2026-09-08"
authors: ["Zig translate-c contributors"]
published: 2026
citation_key: "zig-project-2026-c-translator-limits"
container: "Official translate-c source repository"
edition: "41c10fa66ac81343c33f2b8c746f181b41eaaa27"
isbn: null
doi: null
url: "https://codeberg.org/ziglang/translate-c/src/commit/41c10fa66ac81343c33f2b8c746f181b41eaaa27/src/Translator.zig"
accessed: "2026-09-08"
tags: [zig, kernel-language, interoperability]
aliases: []
---

# Zig C translator: bitfields and unsupported statements

## Reference

Zig translate-c contributors. *Translator.zig*, revision
41c10fa66ac81343c33f2b8c746f181b41eaaa27, linked by the 0.16.0 release notes.
[Primary source file](https://codeberg.org/ziglang/translate-c/src/commit/41c10fa66ac81343c33f2b8c746f181b41eaaa27/src/Translator.zig).


## Research question or contribution

What evidence does this work provide for Zig kernel development or a C fallback?

## Method

Read the exact translator revision linked by the 0.16.0 release notes, especially lines 617–621, 1344–1347 and 1681–1685.

## Findings

Records containing bitfields are demoted to opaque. Goto-related, labeled and assembly statements are unsupported by the inspected translation paths.

## Relevance

Keep difficult implementation bodies in C and expose small accessors or opaque handles. C-to-Zig translation is optional for calling original compiled C.

## Limits

The release-linked revision is evidence about those paths, not an assertion that every installed translator uses that exact revision. Pin and test the actual translator used by M0.

## Derived work

- [Zig kernel feasibility and C interoperability](../20-notes/proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md)
