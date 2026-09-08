---
title: "Kernel-language selection"
kind: map
created: "2026-09-08"
tags: [zig, c-language, kernel-language, language-comparison]
aliases: []
---

# Kernel-language selection

## Scope

Compare Zig and C against the same Intel T7500 kernel contract. Separate the
operative language decision, engineering recommendation and executable
qualification. This is not a new language-comparison implementation milestone.

## Start here

- [Zig versus C comparison](../20-notes/proof-of-concept-requirements/zig-versus-c-kernel-language-comparison.md) — pros, cons, conditional recommendation and circumstances favoring C.
- [Decision-change inquiry](../40-inquiries/what-evidence-would-change-the-kernel-language-choice.md) — what could falsify the recommendation.
- [Comparison journal](../50-journal/2026-09-08-zig-versus-c-kernel-language-deep-dive.md) — source provenance and fair-comparison limits.

## Trails

### First establish feasibility, then compare risks

The [Zig route](zig-kernel-development.md) and [C route](c-kernel-development.md)
both establish plausible low-level mechanisms. Neither has demonstrated
Atom's boot or protected execution. The comparison evaluates their different
source, compiler, integration and assurance risks without treating either
small ELF as a working kernel.

### Distinguish language checks from system isolation

The comparison's safety discussion connects checked operations to error
handling, panic and the privileged failure domain. The
[minimal-kernel map](minimal-privileged-kernel.md) owns the capability,
lifetime and containment model; choosing a language does not supply it.

### Let priorities change the recommendation

A small greenfield research kernel can reasonably favor Zig's integrated
idioms. A governing C verification path, extensive actual C reuse or a
requirement to minimize additional toolchain uncertainty can favor C.
The decision must use real constraints, not invented productivity estimates.

## Open questions

Can the team sustain the selected profile, and can it pass the shared
build/debug/boot/lifetime gates? The [PoC map](proof-of-concept.md) retains
the same CLI-first and unprivileged BEAM/GC obligations under either choice.
