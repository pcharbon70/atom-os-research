---
title: "LZ4 1.10.0 freestanding library profile"
kind: source
created: "2026-09-08"
authors: ["Yann Collet","LZ4 contributors"]
published: 2024
citation_key: "collet-2024-lz4-freestanding-profile"
container: "LZ4 public header"
edition: "v1.10.0"
isbn: null
doi: null
url: "https://github.com/lz4/lz4/blob/v1.10.0/lib/lz4.h"
accessed: "2026-09-08"
tags: [zig, kernel-language, interoperability]
aliases: []
---

# LZ4 1.10.0 freestanding library profile

## Reference

Yann Collet and LZ4 contributors. *lz4.h*, LZ4 v1.10.0 (2024),
freestanding configuration documentation. [Primary header](https://github.com/lz4/lz4/blob/v1.10.0/lib/lz4.h).


## Research question or contribution

What evidence does this work provide for Zig kernel development or a C fallback?

## Method

Read the freestanding documentation and configuration definitions at source lines 90–114.

## Findings

LZ4_FREESTANDING requires supplied memory-operation macros and restricts use to the no-heap LZ4/HC subset; the frame API is excluded.

## Relevance

A concrete example of a C library with a bounded porting surface, unlike arbitrary hosted software.

## Limits

Header inspection only: no LZ4 build, fuzzing, performance measurement or dependency selection was performed.

## Derived work

- [Zig kernel feasibility and C interoperability](../20-notes/proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md)
