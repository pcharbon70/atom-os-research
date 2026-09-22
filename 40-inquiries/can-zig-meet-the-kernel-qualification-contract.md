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

1. Preserve and rerun the selected compiler/backend/linker, repository and
   ownership record in [M0 Phase 1](../60-planning/01-proof-of-concept/m0-boot-inputs/phase-01-target-toolchain-and-build-baseline.md)
   when an input changes.
2. Extend the demonstrated fixed-signature ABI/helper fixtures only as later
   kernel interfaces require; do not generalize the bounded closure result.
3. Define boot, trap, syscall, stack/FP and panic contracts, then demonstrate
   the exact minimum QEMU boot and native user-mode CLI.
4. Exercise privilege, interrupt, preemption, allocation, callback lifetime and
   reclamation failures; qualify every physical fixture separately.

## Findings

The [research session](../50-journal/2026-09-08-zig-kernel-feasibility-deep-dive.md)
demonstrated a narrow hosted C/Zig/callback path and freestanding mixed-language
link. It found current header-generation and translation limitations, and did
not demonstrate reproducible images, boot, privilege transitions or timing.
The [Zig map](../10-maps/zig-kernel-development.md) separates specifications,
scholarly evidence and practitioner examples.

The [2026-09-17 M0 build-closure run](../50-journal/2026-09-17-m0-phase-01-build-closure.md)
then pinned Zig 0.16.0/LLVM/LLD and exercised a non-bootable static ELF64
fixture at a fixed address. Assembly called Zig, Zig consumed the C header and
called C, and C called a Zig callback. Two clean absolute-path builds produced
the same stripped ELF; the audit found no dynamic/unresolved dependency or
FP/SIMD use. Deliberate compiler-helper, host-import and CPU-profile drift all
failed. This closes the bounded M0 build task, not interrupt transitions,
privileged execution, boot, allocation/reclamation, user mode or the full
kernel qualification question.

## Outcome

Open. Language selection is accepted, not under general comparative review.
Resolve the qualification question only with identified input pins and the
required executable evidence. Reopen affected results on toolchain, ABI,
processor-state or dependency changes. A serious code-generation or boundary
failure requires a recorded workaround/profile revision, not a silent pass.
