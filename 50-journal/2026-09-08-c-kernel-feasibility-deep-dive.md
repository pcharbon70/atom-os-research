---
title: "2026-09-08 C kernel feasibility deep dive"
kind: journal
created: "2026-09-08"
tags: [c-language, kernel-language, proof-of-concept]
aliases: []
---

# 2026-09-08 C kernel feasibility deep dive

## Observations

The user requested a C-language assessment with scientific papers, articles,
blogs and low-level/library compatibility verification. The
[synthesis](../20-notes/proof-of-concept-requirements/c-kernel-language-feasibility-and-low-level-compatibility.md)
supports feasibility but leaves executable qualification open. Zig remains
selected; this session changes neither AGENTS.md nor phased plans.

## Scope and method

The operational question was whether C plus an explicit implementation
profile can satisfy the existing Intel T7500 PoC contract. Research separated
language/environment support, compiler/ABI/hardware boundaries, library
dependencies, scientific failure evidence, bounded local probes and remaining
acceptance gates. The deep-research skill's planning control was unavailable;
this journal preserves the working sequence and claim/gap ledger instead.

Two independent lanes examined compiler/library contracts and scientific/
practitioner evidence. The main lane checked standard status and drafts,
reviewed consequential primary passages, executed original probes, and
synthesized the result. Reviewers did not edit files or run experiments.

Search families covered ISO C23 and WG14 freestanding drafts; GCC/Clang
freestanding, x86 attributes, atomics and assembly; Linux's language/build
profile; compiler differential testing, optimization-related undefined
behavior and pointer provenance; and original compiler-engineering articles.
Search snippets were discovery aids, not evidence for detailed claims.
Versioned manuals, relevant draft clauses, full-text paper methods/limits and
author-written articles supplied the evidence.

This is a focused assessment, not an exhaustive or systematic literature
review. Historical studies explain failure mechanisms, not the defect rate of
current compilers. ISO's catalogue was read for final-standard status; the
paid final C23 standard was not read. N1570 and N3096 are explicitly dated
public drafts. Parent web retrieval of GCC's atomic-builtin page failed;
the independent compiler lane read the versioned page, and our probe verifies
only the displayed 64-bit atomic sequence, not all atomic lowering rules.
Research stopped when decisive feasibility claims were supported and remaining
uncertainty was expressible as concrete qualification work.

## Claim and gap ledger

| Claim | Evidence basis | Remaining gap |
| --- | --- | --- |
| C can run without a host OS | C11 draft; GCC/Clang freestanding records | Actual startup, memory initialization and boot |
| C has an established kernel route | Linux dialect/build evidence; GCC/Clang attributes | Atom-specific profile and hardware-state correctness |
| C ABI integration is feasible | AMD64 procedure ABI; C-R01 | Broader types, error/cancellation/ownership and cross-language contracts |
| Static C is not dependency-free | GCC support/link rules; C-R04; library records | Approved implementations and complete helper/service census |
| Volatile is not general synchronization | GCC asm/volatile/atomic documentation; Intel boundary | IRQ/device ordering and later SMP tests |
| Mature tooling does not prove correctness | Csmith, Stack, provenance research and engineering articles | Actual source/optimization regressions and semantic discipline |
| C can receive stronger assurance | Existing seL4/translation-validation papers | Our models, code, assumptions and proofs, none supplied here |
| No language switch follows from this survey | Existing selected Zig decision and comparison scope | Explicit user decision if a switch is desired |

The exhaustive primary source-note identities appear in the manifest below;
the synthesis places them beside supported claims. Proposed controls are our
inferences, not reported experimental results.

## Environment and reproduction

Baseline: `main`, commit `de1395278fb665cccbe428f385f955f4b535a4a2`.
The previous Zig research bundle and related navigation/planning changes were
already uncommitted and were preserved. C fixtures are original research
assets, not kernel implementation or third-party vendored code.

Installed inputs:

- GCC 13.3.0, Ubuntu 13.3.0-6ubuntu2~24.04, target `x86_64-linux-gnu`.
- Clang 21.1.0 supplied through Zig 0.16.0; C source compiled by Clang.
- GNU ld/binutils 2.42; Linux hosted clients.
- Explicit GNU11, Nehalem, O2 and warning/error controls. The freestanding
  profile additionally excluded red-zone use, FP/vector register generation,
  default stack protection, PIC/PIE and unwind tables.

The exact [script](../assets/c-kernel-feasibility/run.sh) and
[transcript](../assets/c-kernel-feasibility/results.txt) preserve commands,
versions, source/compiler hashes, headers, symbols and disassembly:

```bash
timeout 180 bash assets/c-kernel-feasibility/run.sh
```

The script assumes the installed asdf Zig path and GCC/GNU binutils commands.
On another host, adapt those paths and record the new identities. It is not
an accepted portable M0 launcher. GCC is a Linux-target compiler used for
freestanding objects; the Clang fixture uses an explicit freestanding triple.
No complete compiler/header/support-library distribution closure was hashed.

An initial `zig cc --version` without isolated caches failed with
`ReadOnlyFilesystem` while creating its cache. The script fixed this by
using temporary per-probe cache directories and an explicit
`ASDF_ZIG_VERSION=0.16.0`; no installation or persistent configuration change
was made.

## Local evidence

| ID | Observation | Limits |
| --- | --- | --- |
| C-R01 | Both hosted cross-compiler clients returned the expected record and callback result; layout assertions passed | One small Linux-hosted integer interface |
| C-R02 | GCC and Clang objects independently linked at entry 0x100000; no dynamic section, interpreter segment or undefined symbols observed | No C startup or boot protocol; only selected objects |
| C-R03 | Both emitted port output, width-specific load, lock xadd and iretq | No real MMIO, atomic-contention, interrupt installation or privileged execution |
| C-R04 | Both separate wide-division objects imported __udivti3; omitted-helper links failed with the required diagnostic | Negative dependency evidence, not helper implementation |
| C-R05 | Initial GCC disassembly contained endbr64; adding -fcf-protection=none removed it | Ambient compiler behavior needs explicit control; no old-CPU fault claim |

The first run retained outputs at `/tmp/atom-c-probe.q2qaDQ`.
The final run used `/tmp/atom-c-probe.Ph7PRu` and exited 0. Both transcripts
are retained, with the changed flag explained. Source hashes in the first
transcript identify the earlier script; the final transcript identifies the
current script.

Final observed ELF hashes:

- GCC: `554a70cc01ec862cb3d550baf2f6e9ebd43b05bb65c27235dd182fb4c0d09341`.
- Clang: `19b1c47c15c24c51ea5f3950e24d3b32eec45788bcdc9d1f01f1d7403d1f6666`.

The runs do not form a same-input reproducibility test. Generated binaries
remain temporary; retained source/transcripts are the durable evidence.
No sanitizer, compiler fuzzing, library port, guest boot, physical T7500 test,
privileged host instruction, disk/device write, SMP or timing test occurred.
No M0–M4 task was checked off.

## Corpus changes and verification

Created the C synthesis, ten primary-source records, topic map, open inquiry,
this journal and original fixture directory. Reused eleven existing sources,
including records introduced in the earlier Zig session on the same date.
Their creation date does not make them newly introduced here.

Navigation connects the C assessment to R02, the Zig study, the home and PoC
maps, and all affected directory indexes. Earlier Zig edits remain intact.
No commits, pushes, PRs or publishing were requested or performed.

Verification passed: `python3 validate_archive.py` checked 587 completed
documents, 29 directories, 5709 local links and 359 source notes. Its 22
deep-dive manifests classified 347 introduced and 373 reused source uses;
the 12 source notes outside a deep-dive manifest are pre-existing.
`git diff --check` and `bash -n assets/c-kernel-feasibility/run.sh` passed.
No validator/schema code changed, so validator unit tests were not required.
Two independent read-only factual reviews found no actionable inaccuracies
in the scientific summaries, compatibility claims or retained probe evidence.
The final Markdown structure, source provenance, navigation and change scope
were reviewed; no rendered visual-layout review is claimed.

## Source manifest

### Newly introduced sources

- [C11 committee draft N1570](../30-sources/wg14-2011-c11-committee-draft.md) — C11 freestanding startup, headers and semantic boundaries.
- [C23 publication status and public working draft](../30-sources/iso-wg14-2024-c23-status-and-draft.md) — published C23 status versus earlier draft library provisions.
- [GCC x86 kernel C extensions and dependency contract](../30-sources/gnu-project-2026-x86-kernel-c-profile.md) — x86 ABI/assembly/interrupt controls and compiler-helper dependencies.
- [Clang 21 x86 interrupt attribute contract](../30-sources/llvm-project-2025-clang-x86-interrupt-contract.md) — versioned Clang hardware-interrupt declaration and callee constraints.
- [Linux kernel C dialect and compiler profile](../30-sources/linux-community-2026-kernel-c-dialect.md) — mature kernel dialect, compiler support and implementation-specific flags.
- [Finding and understanding bugs in C compilers](../30-sources/yang-et-al-2011-csmith.md) — historical differential-testing evidence for compiler defects.
- [Towards optimization-safe systems](../30-sources/wang-et-al-2013-optimization-safe-systems.md) — undefined-behavior effects on defensive systems checks.
- [Exploring C semantics and pointer provenance](../30-sources/memarian-et-al-2019-c-pointer-provenance.md) — pointer/provenance models and low-level semantic assumptions.
- [What every C programmer should know about undefined behavior](../30-sources/lattner-2011-c-undefined-behavior.md) — compiler-author explanation of optimization and undefined behavior.
- [Off by two: a low-level compiler regression](../30-sources/desaulniers-2020-off-by-two.md) — historical fixed C/assembly regression and debugging method.

### Reused sources

- [GCC freestanding environment](../30-sources/gnu-project-2026-gcc-freestanding-environment.md) — startup and memory/helper requirements.
- [Clang 21 freestanding builds](../30-sources/llvm-project-2025-clang-21-freestanding.md) — memory helper and library limits.
- [AMD64 procedure ABI](../30-sources/x86-psabi-project-2026-amd64-procedure-abi.md) — ordinary LP64/SysV call contract.
- [Intel system programming](../30-sources/intel-2026-system-programming-documentation.md) — hardware privilege, state and interrupt boundaries.
- [Newlib system hooks](../30-sources/newlib-project-2026-libc-system-hooks.md) — explicit bare-board service adaptation.
- [musl Linux dependency](../30-sources/musl-project-2026-linux-dependency.md) — why a C libc is not automatically OS-independent.
- [LZ4 freestanding profile](../30-sources/collet-2024-lz4-freestanding-profile.md) — bounded C subset example, not a selected dependency.
- [Flux OSKit](../30-sources/ford-et-al-1997-flux-oskit.md) — historical environment-adapter requirements.
- [Translation validation](../30-sources/sewell-et-al-2013-translation-validation.md) — binary assurance and excluded hardware/assembly scope.
- [Verified microkernel](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md) — disciplined C feasibility and non-transferring proof assumptions.
- [Zig 0.16 language reference](../30-sources/zig-project-2026-language-reference-0-16.md) — limited comparison with the still-selected language.

## Threads

The [C map](../10-maps/c-kernel-development.md) is selective navigation.
The [Zig session](2026-09-08-zig-kernel-feasibility-deep-dive.md) records the
earlier language-specific experiments and introducing provenance.

## Follow-ups

Prioritize actual component/profile qualification and an assembled M1 boot
contract. Do not add a broad C-versus-Zig benchmark or library-port milestone
without a concrete decision need and authorization.
