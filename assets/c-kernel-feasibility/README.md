---
title: "C kernel feasibility research fixtures"
kind: map
created: "2026-09-08"
tags: [directory-index, research-evidence, c-language]
aliases: []
---

# C kernel feasibility research fixtures

## Purpose

Original research probes for the [C feasibility assessment](../../20-notes/proof-of-concept-requirements/c-kernel-language-feasibility-and-low-level-compatibility.md).
They examine C compiler interoperability and freestanding code generation,
not a bootable Atom kernel or a change from the selected Zig language.

## What belongs here

Small project-authored fixtures and textual observations. No third-party code
or compiler distribution is vendored. Generated binaries/caches remain in
temporary directories; privileged routines are never executed on the host.

## Index

### Subdirectories

- None.

### Files

- [ABI header](abi.h) — explicit record, callback and layout assertions.
- [Library fixture](library.c) — C aggregate/callback implementation.
- [Hosted driver](host.c) — bidirectional GCC/Clang checks under Linux.
- [Architecture fixture](arch.c) — compile-only MMIO, port, atomic and interrupt examples.
- [Assembly entry](entry.S) — compile-only halt entry; no boot protocol or startup.
- [Helper-demand fixture](helpers.c) — 128-bit division to expose compiler support imports.
- [Reproduction script](run.sh) — builds with installed GCC and Clang via Zig, inspects ELF and verifies a helper-related rejection.
- [Observed results](results.txt) — command transcript and hashes; no boot evidence.

## Maintaining this index

Inventory all retained attachments and keep the [research journal](../../50-journal/2026-09-08-c-kernel-feasibility-deep-dive.md)
aligned with actual command scope, failures and evidence limits.
