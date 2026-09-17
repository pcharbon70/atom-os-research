---
title: "2026-09-17 — M0 phase 01 build closure"
kind: journal
created: "2026-09-17"
tags:
  - implementation-planning
  - m0
  - proof-of-concept
  - zig
aliases: []
---

# 2026-09-17 — M0 phase 01 build closure

Kay OS M0 Phase 1 Section 1.2 produced and exercised the selected non-bootable
freestanding qualification ELF. The run supports completion of
`m0-p01-build` and the compiler portion of `m0-p01-decisions`; it does not run
the phase integration gate or qualify QEMU, SeaBIOS, or the physical T7500.

## Plan and acceptance baseline

The governing plan was [M0 Phase 1](../60-planning/01-proof-of-concept/m0-boot-inputs/phase-01-target-toolchain-and-build-baseline.md)
at research revision `bb80394`. The user accepted a fixed-address
non-bootable ELF, `build.zig` plus validation scripts, a bidirectional Zig/C
boundary with an assembly entry, and Apache-2.0 on 2026-09-17.

The run evaluated task `m0-p01-build`, M0-A02's native build contribution and
the still-preliminary input portions of M0-T01/M0-T02. No milestone acceptance
case closed because Phase 1 integration, the installed-unit inventory, later
boot-image work, and acceptance review remain absent.

Predeclared invariants were a static ELF64 `ET_EXEC` at `0x200000`, explicit
`x86_64-freestanding-none`/Nehalem code generation, no libc or compiler runtime,
no unresolved symbols, no dynamic loader, disabled red zone, no observed
x87/MMX/SSE/AVX-family register use, stable C/Zig record layout, equal clean
build outputs, and explicit rejection of helper, host-import, and CPU-profile
drift.

## Environment and provenance

- Implementation repository: [pcharbon70/kay-os](https://github.com/pcharbon70/kay-os)
- Tested implementation commit: `be4a230` (`M0 phase 1 section 1.2: qualify freestanding build`)
- Tested state: clean
- Evidence record: `evidence/m0-p01-build-2026-09-17.md` at the same commit
- Zig: 0.16.0, executable SHA-256
  `2317bbb91798556d9d0f38aabdac23db83f0979b25f767259ae474546724087c`
- Backend/linker: LLVM/LLD; C compiled through Zig's bundled Clang path
- Host boundary: Linux x86-64 build host supplied Zig, POSIX shell, GNU ELF
  inspection tools, temporary directories, and hashing
- Guest/physical target: not run; no QEMU or T7500 result is claimed
- Artifact resource limit: the fixture owns a 16 KiB stack; it has no allocator
  and the build uses no writable guest storage

The implementation repository retains the human-readable record at
`evidence/m0-p01-build-2026-09-17.md`; generated ELF, maps, disassembly and raw
logs remained outside version control under the requested absolute evidence
directory.

## Execution and results

| Task / case IDs | Fixture and exact command | Expected result | Actual observation | Result | Raw evidence / artifact identity |
| --- | --- | --- | --- | --- | --- |
| m0-p01-build / clean-build-a,b | `ZIG=/home/ducky/.asdf/installs/zig/0.16.0/zig scripts/m0/verify-build-closure.sh /tmp/kay-m0-section-1-2-evidence-v5` | Two distinct absolute-path source copies and caches produce identical stripped ELFs and equal audit symbol/ELF maps. | Driver exited zero; both acceptance hashes were `e94b127fcc4388e73b4620a8b0908dcdeed0c3a08fbf0052d92cce58a3baf31a`; maps compared equal. | pass | Implementation record at `be4a230`; local `canonical-builds.sha256`, `symbols.map`, and `elf.map` |
| m0-p01-build / elf-and-abi-audit | Same driver; `build.zig`, linker script, Zig `@cImport`, C11 assertions and assembly entry | Static ELF64 `ET_EXEC`, entry `0x200000`, no dynamic/unresolved dependency, required boundary symbols, no FP/SIMD use. | All header, program-header, undefined-symbol, symbol and disassembly checks passed. | pass | Acceptance ELF hash above; local `elf.map`, `symbols.map`, and `disassembly.txt` |
| m0-p01-build / undefined-compiler-helper | Driver compiles `tests/m0/negative/undefined-helper.c` with compiler-rt disabled. | Link fails on `__udivti3`. | LLD reported `undefined symbol: __udivti3`; command returned nonzero. | pass | Local `negative-undefined-helper.log` |
| m0-p01-build / host-syscall-import | Driver compiles `tests/m0/negative/host-syscall.c` without libc. | Link fails on `write`. | LLD reported `undefined symbol: write`; command returned nonzero. | pass | Local `negative-host-syscall.log` |
| m0-p01-build / cpu-option-drift | Driver invokes `zig build -Dcpu=haswell`. | Build rejects the unregistered CPU override. | Zig reported `invalid option: -Dcpu`; command returned nonzero. | pass | Local `negative-cpu-option.log` |

The unstripped audit ELF hashes differed because DWARF encoded the two absolute
source paths. That predeclared audit-only difference is not present in the
directly generated stripped acceptance artifact. This is build evidence, not
execution of the ELF.

## Review and handoff

Implementation-agent review supports checking `m0-p01-build`, both Section
1.2 subtasks, and the compiler-qualification subtask under
`m0-p01-decisions`. Acceptance review is unassigned, so no phase handoff is
approved.

At the time of this run, the plan made the user-deferred `m0-p01-inventory`
evidence an integration dependency. The subsequent user clarification moved
that obligation to `m0-p03-inventory`: it still blocks final M0 and physical
claims, but no longer blocks Phase 1 virtual integration or Phase 2 planning.
This planning correction does not change the build observations above.

Changes to Zig version or executable identity, target/CPU/features, build flags,
linker layout, ABI header, native signatures, panic/stack contract, negative
cases, or reproducibility policy reopen this build result. A later merge SHA
does not by itself prove the merged tree passed. This record authorizes no
push, PR, device write, QEMU execution, or Phase 2 implementation.

## Follow-ups

- Run [Phase 1 Integration Tests](../60-planning/01-proof-of-concept/m0-boot-inputs/phase-01-target-toolchain-and-build-baseline.md)
  against the independent pinned virtual fixture.
- Collect the redacted T7500 installed-unit record in Phase 3 when the physical
  operator makes the machine available.
- Assign an acceptance reviewer before `m0-p01-handoff` can decide closure.
