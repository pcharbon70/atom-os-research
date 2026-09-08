---
title: "C kernel development"
kind: map
created: "2026-09-08"
tags: [c-language, kernel-language, proof-of-concept]
aliases: []
---

# C kernel development

## Scope

A selective route through C as an alternative kernel language and as the
C-component path within the chosen Zig kernel. The assessment does not change
the language decision, target or M0–M4 acceptance.

## Start here

- [Zig versus C comparison](../20-notes/proof-of-concept-requirements/zig-versus-c-kernel-language-comparison.md) — tradeoffs and conditions under which C becomes preferable.
- [C feasibility assessment](../20-notes/proof-of-concept-requirements/c-kernel-language-feasibility-and-low-level-compatibility.md) — low-level coverage, compatibility, scientific evidence and missing qualification.
- [Open qualification inquiry](../40-inquiries/can-c-meet-the-kernel-qualification-contract.md) — what would establish the alternative's actual fitness.
- [Research session](../50-journal/2026-09-08-c-kernel-feasibility-deep-dive.md) — exact source manifest, claim ledger and experiment limits.

## Trails

### Separate the language from the machine

Begin with the [C11 environment contract](../30-sources/wg14-2011-c11-committee-draft.md)
and [C23 status/draft boundary](../30-sources/iso-wg14-2024-c23-status-and-draft.md).
Then read the [GCC x86 profile](../30-sources/gnu-project-2026-x86-kernel-c-profile.md)
and [Clang interrupt contract](../30-sources/llvm-project-2025-clang-x86-interrupt-contract.md).
Compiler support is not installed hardware-state correctness.

### Admit components by their dependencies

The assessment's compatibility table connects pure C, compiler helpers and
different libc environments. The [local fixtures](../assets/c-kernel-feasibility/README.md)
show cross-compiler calls and an intentionally missing runtime helper.
The [Zig map](zig-kernel-development.md) preserves the active decision and
the separate language-boundary evidence.

### Investigate failures, not only successful examples

[Csmith](../30-sources/yang-et-al-2011-csmith.md),
[optimization-unstable systems code](../30-sources/wang-et-al-2013-optimization-safe-systems.md)
and [pointer provenance](../30-sources/memarian-et-al-2019-c-pointer-provenance.md)
answer different assurance questions. Their historical results do not rank
current compilers or prove our kernel safe.

## Open questions

The [PoC map](proof-of-concept.md) retains the native CLI, protected services,
compiled BEAM and unprivileged tracing-GC obligations. Next evidence is a
qualified build/ABI/helper profile followed by real privileged execution;
another broad language survey is not the decisive missing artifact.
