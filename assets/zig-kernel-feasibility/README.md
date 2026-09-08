---
title: "Zig kernel feasibility research fixtures"
kind: map
created: "2026-09-08"
tags: [directory-index, research-evidence, zig]
aliases: []
---

# Zig kernel feasibility research fixtures

## Purpose

Retain project-authored, bounded compile/link and hosted ABI experiments for
the [Zig assessment](../../20-notes/proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md).
These are not a bootable kernel or completed M0 implementation.

## What belongs here

Small original fixtures, reproduction instructions and observed textual
results. No third-party implementation, compiler distribution or binary is
vendored. Privileged assembly is compiled and inspected, never run on the host.

## Index

### Subdirectories

- None.

### Files

- [ABI header](abi.h) — hand-authored C boundary and layout assertions.
- [C fixture](interop.c) — C callee/caller and optional hosted test driver.
- [Zig fixture](interop.zig) — C ABI exports, callbacks and layout checks.
- [Architecture fixture](arch.zig) — compile-only port I/O, MMIO, atomic and halt probes.
- [Reproduction script](run.sh) — isolated temporary output/cache, mixed-compiler checks and ELF inspection.
- [Observed results](results.txt) — execution transcript and binary identities, not boot evidence.

## Maintaining this index

Inventory every retained fixture and log. Keep limitations, commands and
results aligned with the [session journal](../../50-journal/2026-09-08-zig-kernel-feasibility-deep-dive.md).
Generated binaries and caches remain in the printed temporary output directory.
