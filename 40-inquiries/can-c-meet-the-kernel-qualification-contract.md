---
title: "Can C meet the kernel qualification contract?"
kind: inquiry
created: "2026-09-08"
status: open
tags: [c-language, kernel-language, proof-of-concept]
aliases: []
---

# Can C meet the kernel qualification contract?

## Why this matters

The [C assessment](../20-notes/proof-of-concept-requirements/c-kernel-language-feasibility-and-low-level-compatibility.md)
finds no fundamental facility blocker. This is an alternative/fallback
evaluation, not a change from the user's selected Zig language.

## Operational question

Can a pinned C/compiler-extension/assembly profile satisfy the existing Intel
x86-64 build, ABI, privilege, resource and runtime boundaries without importing
unapproved host-OS services?

## Working hypotheses

- A narrow freestanding C implementation can express the necessary kernel mechanisms.
- Direct C compilation simplifies source integration but does not establish ABI,
  library-environment or execution compatibility.
- Explicit semantic/ownership rules and targeted tests can make remaining
  PoC risk visible; C alone cannot enforce the architecture's isolation model.

## Paths to explore

1. Expand the exact C-component dialect, ABI and runtime-helper contract within
   [M0](../60-planning/01-proof-of-concept/m0-boot-inputs/README.md).
2. Qualify memory helpers, aggregate/callback boundaries, compiler defaults,
   repeatable input closure and failure diagnostics.
3. Demonstrate real boot, exception/IRQ handling and user return under the
   existing minimum guest profile, then separately on the inventoried T7500.
4. Test resource/lifetime failures and preserve compiled-BEAM/GC requirements.
   Investigate a concrete candidate library only when it supplies required work.

## Findings

The [session journal](../50-journal/2026-09-08-c-kernel-feasibility-deep-dive.md)
records passing hosted mixed-compiler calls, dependency-closed tiny ELF links,
compile-only architecture emission and expected missing-helper failures.
It records no boot, privileged execution, sanitizer or timing qualification.
The [topic map](../10-maps/c-kernel-development.md) separates primary
specifications, historical research and local evidence.

## Outcome

Open. General feasibility is supported; implementation qualification is not
complete. This inquiry is not an extra comparison milestone or a reason to
delay the selected Zig work. A primary-language switch requires the user's
explicit decision; C components still need their own admission evidence.
