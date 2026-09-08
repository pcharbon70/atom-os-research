---
title: "Can Zig meet the kernel qualification contract?"
kind: inquiry
created: "2026-09-08"
status: open
tags: [zig, kernel-language, proof-of-concept, qualification]
aliases: []
---

# Can Zig meet the kernel qualification contract?

## Why this matters

Zig is the user's selected kernel language. The [feasibility assessment](../20-notes/proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md)
supports beginning implementation qualification, but availability of language
features does not establish a working privileged kernel.

## Operational question

Can one pinned Zig/C/assembly toolchain produce reproducible, dependency-closed
Intel x86-64 images whose ordinary calls, interrupt transitions, state ownership,
panic and memory behavior satisfy the existing M0–M4 contracts?

## Working hypotheses

- A narrow Zig kernel with audited assembly and optional C components can meet
  the required low-level contract without a guest host OS.
- C ABI boundaries are practical when representation, lifetime, execution
  context and dependency closure are explicit.
- Compiler qualification and kernel invariant tests can bound the remaining
  risk sufficiently for a PoC, without claiming formal memory safety.

## Paths to explore

1. Resolve the remaining compiler/backend/linker/translator, repository and
   ownership choices in [M0 Phase 1](../60-planning/01-proof-of-concept/m0-boot-inputs/phase-01-target-toolchain-and-build-baseline.md).
2. Expand ABI/helper/generated-code fixtures and establish controlled clean
   builds; translation command success alone is insufficient.
3. Define boot, trap, syscall, stack/FP and panic contracts, then demonstrate
   the exact minimum QEMU boot and native user-mode CLI.
4. Exercise privilege, interrupt, preemption, allocation, callback lifetime and
   reclamation failures; qualify the physical T7500 separately.

## Findings

The [research session](../50-journal/2026-09-08-zig-kernel-feasibility-deep-dive.md)
demonstrated a narrow hosted C/Zig/callback path and freestanding mixed-language
link. It found current header-generation and translation limitations, and did
not demonstrate reproducible images, boot, privilege transitions or timing.
The [Zig map](../10-maps/zig-kernel-development.md) separates specifications,
scholarly evidence and practitioner examples.

## Outcome

Open. Language selection is accepted, not under general comparative review.
Resolve the qualification question only with identified input pins and the
required executable evidence. Reopen affected results on toolchain, ABI,
processor-state or dependency changes. A serious code-generation or boundary
failure requires a recorded workaround/profile revision, not a silent pass.
