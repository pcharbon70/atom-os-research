---
title: "System V AMD64 procedure ABI and microarchitecture levels"
kind: source
created: "2026-09-06"
authors:
  - "x86-64 psABI project contributors"
published: null
citation_key: "x86-psabi-project-2026-amd64-procedure-abi"
container: "x86-64 psABI project"
edition: "Moving master source, low-level-sys-info.tex, accessed 2026-09-06"
isbn: null
doi: null
url: "https://gitlab.com/x86-psABIs/x86-64-ABI"
accessed: "2026-09-06"
tags:
  - abi
  - boot
  - x86-64
aliases: []
---

# System V AMD64 procedure ABI and microarchitecture levels

## Reference

x86-64 psABI project contributors. *System V AMD64 ABI*, moving source.
[Official repository](https://gitlab.com/x86-psABIs/x86-64-ABI) and
[low-level system information](https://gitlab.com/x86-psABIs/x86-64-ABI/-/raw/master/x86-64-ABI/low-level-sys-info.tex).

## Research question or contribution

Which procedure and enabled-state expectations must a freestanding AMD64
build either implement or explicitly narrow?

## Method

Read the source sections on processor features, data representation, register
ownership and stack frames. This was not a complete ABI or object-format audit;
the moving source has not been pinned to an implementation commit.

## Findings

- LP64 uses 64-bit pointers and longs; the document also distinguishes ILP32.
- Baseline features include x87, MMX, SSE/SSE2 and required OS enablement.
  Later v2/v3/v4 levels add features; higher vector levels require state checks.
- Procedure callee-save rules do not save every interrupted register.
- Ordinary calls have defined stack alignment. The user ABI's 128-byte red
  zone relies on preservation by asynchronous handlers.

## Relevance

Atom must declare its native procedure subset, maintain stack discipline and
audit generated state use. An interruptible kernel should not assume a
user-space red-zone guarantee on its own stack. A restricted integer-only
bring-up is not full ordinary AMD64 ABI support.

## Limits

A procedure convention is not Atom's syscall ABI or an OS implementation.
This source cannot select firmware, a CPU SKU, privileged return instructions,
or physical memory and interrupt-controller behavior.

## Derived work

- [T7500 / Intel x86-64 target](../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md)
- [Freestanding build](../20-notes/proof-of-concept-requirements/freestanding-build-and-static-images.md)
