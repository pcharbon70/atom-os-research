---
title: "Zig kernel development"
kind: map
created: "2026-09-08"
tags: [zig, kernel-language, proof-of-concept]
aliases: []
---

# Zig kernel development

## Scope

A selective route through the chosen kernel language, its C/assembly boundary,
compiler qualification and evidence limits. This is not a language-comparison
roadmap or an endorsement of a pre-existing OS foundation.

## Start here

- [Zig versus C comparison](../20-notes/proof-of-concept-requirements/zig-versus-c-kernel-language-comparison.md) — conditional recommendation and strongest alternative case; separate from the recorded selection.
- [Feasibility assessment](../20-notes/proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md) — conclusion, low-level coverage, C fallback, local results and prioritized qualification.
- [Qualification inquiry](../40-inquiries/can-zig-meet-the-kernel-qualification-contract.md) — what remains falsifiable after language selection.
- [Session evidence](../50-journal/2026-09-08-zig-kernel-feasibility-deep-dive.md) — exact source manifest and probe limits.

## Trails

### Separate language from ABI and platform

Read the [versioned language reference](../30-sources/zig-project-2026-language-reference-0-16.md),
[release changes](../30-sources/zig-project-2026-release-0-16.md) and
[tagged build/runtime definitions](../30-sources/zig-project-2026-freestanding-source-profile.md)
together. Then compare the selected [T7500 target](../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md)
with the actual emitted instructions and native-state contract.

### Reuse C without importing another OS

The [translator limitations](../30-sources/zig-project-2026-c-translator-limits.md)
and [Clang freestanding contract](../30-sources/llvm-project-2025-clang-21-freestanding.md)
explain why a small wrapper and helper census matter. The
[local fixtures](../assets/zig-kernel-feasibility/README.md) test a narrow ABI,
not universal library compatibility.

### Distinguish mechanisms from assurance

[Compiler fuzzing](../30-sources/groce-et-al-2022-no-fuss-compiler-fuzzing.md)
and [OpenMP integration](../30-sources/kacs-et-al-2024-zig-openmp.md) provide
different scholarly evidence. [Ymir](../30-sources/smallkirby-2024-writing-hypervisor-in-zig.md)
shows concrete Intel mechanisms but does not qualify our boot fixture or
user transitions. None establishes a safe completed Atom kernel.

## Open questions

The next work belongs in [M0](../60-planning/01-proof-of-concept/m0-boot-inputs/README.md),
then [M1](../60-planning/01-proof-of-concept/m1-boot-to-cli/README.md):
which exact compiler profile passes, and do its assembled privilege and
resource contracts hold in the guest? The [PoC map](proof-of-concept.md)
preserves the later protected-service and compiled-BEAM/GC obligations.
