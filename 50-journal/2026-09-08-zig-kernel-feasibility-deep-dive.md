---
title: "2026-09-08 Zig kernel feasibility deep dive"
kind: journal
created: "2026-09-08"
tags: [zig, kernel-language, proof-of-concept, research-evidence]
aliases: []
---

# 2026-09-08 Zig kernel feasibility deep dive

## Observations

The user selected Zig as the kernel language and requested scientific,
technical and practitioner evidence for feasibility and C fallback.
The [synthesis](../20-notes/proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md)
concludes that bounded M0 qualification can proceed. It does not close M0,
demonstrate boot, or select a runtime/collector implementation.

The accepted decision is the language. The tested Zig 0.16.0 distribution,
LLVM backend and GNU linker are research inputs, not an accepted production
or M0 profile. Current planning and R02 are synchronized without marking tasks
complete or changing milestone scope.

## Scope and research method

Question: can the chosen language express our Intel x86-64 kernel mechanisms
and interoperate with sufficiently freestanding C components while preserving
the privilege, resource and BEAM/GC boundaries?

The research plan separated release/language/low-level facilities,
C ABI and library dependency closure, empirical/practitioner evidence,
bounded local probes, and synthesis/qualification gaps. Two independent
research lanes covered C interoperability and empirical sources; the main
review covered low-level source definitions, target fit and local probes.
The deep-research skill's requested planning control was unavailable; this
journal preserves the research sequence and gap record instead.

Search families included current Zig release/documentation; Zig freestanding,
inline assembly, volatile and C ABI; Zig compiler fuzzing and scholarly kernel/
embedded work; OpenMP interoperability; and primary Ymir, Ashet, MicroZig
and Uber engineering material. Search engines supplied discovery, not detailed
proof from snippets. Versioned documentation and relevant primary source
sections were read, along with full-text paper methods/results/limits and
author-written implementation reports.

The parent checked consequential claims against release notes, installed
0.16.0 standard-library definitions, primary paper passages and project
documentation. Codeberg web retrieval was unreliable; the C-interoperability
lane read tagged files with approved read-only network commands. The installed
source files independently corroborated calling/build controls. Some blog
retrievals failed; unverified numerical claims were not promoted.

This is not a systematic review, a compiler-security audit, or a claim to have
read every line of the language implementation, Intel manuals or every paper.
Research stopped once the feasibility claims had direct support and remaining
uncertainties were expressed as tests instead of additional broad searches.

## Environment

- Repository baseline: `main`, commit
  `de1395278fb665cccbe428f385f955f4b535a4a2`; initially clean.
  Research fixtures/documents were uncommitted during execution.
- Installed Zig executable:
  `/home/ducky/.asdf/installs/zig/0.16.0/zig`.
  SHA-256:
  `2317bbb91798556d9d0f38aabdac23db83f0979b25f767259ae474546724087c`.
  This identifies the installed binary; no distribution-signature verification
  or complete compiler-library closure hash was performed.
- Plain `zig version` initially failed because asdf had no selected project
  version. Temporary `ASDF_ZIG_VERSION=0.16.0` worked. No installation,
  project `.tool-versions` change or persistent environment change occurred.
- `zig env` reported host target `x86_64-linux.6.8...6.8-gnu.2.39`.
  `zig cc --version` reported Clang 21.1.0; GCC was
  Ubuntu 13.3.0-6ubuntu2~24.04 and GNU binutils/ld 2.42.
- Hosted ABI execution used Linux and GCC's hosted startup/libc.
  The separate freestanding artifacts used
  `x86_64-freestanding-none`, Nehalem code selection and explicit
  `-fllvm`; they were not executed.
- Fresh temporary directories held caches and generated binaries.
  No QEMU or physical T7500 run, privileged host instruction, device write,
  external OS build or package installation was performed.

## Evidence

Original source fixtures, reproduction script and the second-run transcript
are indexed in [research assets](../assets/zig-kernel-feasibility/README.md).
Reproduce with:

```bash
bash assets/zig-kernel-feasibility/run.sh
```

The script is deliberately local-environment-specific: it uses the installed
asdf version and binary path identified above, GCC, GNU ld and binutils.
Adapt and record those paths on another host; this is not a portable M0
launcher. Its translator invocation has a 180-second watchdog because initial
translator compilation is lazy. The first research run had no such wrapper
and completed; the later bounded run also reached its final marker.

| Research case | Observation | Interpretation |
| --- | --- | --- |
| ZIG-R01 hosted ABI | C → Zig → C → Zig callback returned tag 8 and value 42; scalar callback result and C/Zig record size/alignment/offset assertions passed | Narrow ABI mechanism evidence only |
| ZIG-R02 freestanding link | Zig/C/architecture objects linked to static ELF64; no dynamic section, interpreter segment or undefined symbols | No host runtime needed by this fixture; not a bootable-image claim |
| ZIG-R03 architecture emission | Disassembly contained port output, volatile load, lock-prefixed atomic increment and naked CLI/HLT loop | Expression/codegen evidence, never executed at privilege |
| ZIG-R04 translation | Expected extern record/callback/functions emitted, alongside deferred errors for unsupported macros | Successful translation command does not qualify every generated declaration |
| ZIG-R05 header generation | Bare -femit-h produced the compiler's currently-broken diagnostic | Real limitation; hand-maintained header route worked |
| ZIG-R06 repetition | Both hosted runs passed; image hashes differed | Not reproducible-build acceptance |

Initial output directory: `/tmp/atom-zig-probe.oWfBY4`.
Hosted hash:
`87a36aecb37c519f29965869906665b4c628a399222c4a86fcaded0dbc8494b3`.
ELF hash:
`4bcd34bdffcffb08b5d1c871f31037d4f94657a5d11ecedcfd09003ce9b54701`.

Transcript output directory: `/tmp/atom-zig-probe.wm0Mrk`.
Hosted hash:
`1abd3b7ff98589dc23e864d382d8af63787c031c31013654d3f92dd4677b23ad`.
ELF hash:
`ff257e9a8e56857cecac8d5074565039d3d88e946026d594bef59516d5583769`.

A follow-up read-only `readelf --debug-dump=info` inspection found each
temporary output path in its ELF's `DW_AT_comp_dir`. That confirms one
uncontrolled input; it does not explain every byte difference or establish
reproducibility. The ELF also retained `.eh_frame`; no accepted
unwind/image policy is inferred from the simple linker command.

Both runs used the same compile/link/host-execution commands now retained in
run.sh. The first run printed the whole translated header and did not include
the header-emission check; the second filtered translation output and added
that check. Review later tightened the check to require the exact known
diagnostic, so an unrelated compiler failure cannot count as confirmation.
That revised check was rerun separately and passed; the appended transcript
records it. The complete build was not rerun after this checker-only change.

The command transcript includes tool identities, flags, fixture hashes,
ELF headers and disassembly. Translated output is intentionally filtered by
the recorded script; the full first translation was inspected but is not
retained as a new source artifact. The ABI execution uses manually audited
declarations, not a compiled consumer of all translated declarations.

No tests of allocation failure, invalid foreign pointers, deep stack usage,
interrupt entry/return, context leakage, user protection, GC, latency or the
full helper closure were run. These results inform `m0-p01-decisions` and
`m0-p01-build` but are not an implementation execution record or completion
of either task.

## Claim and gap ledger

| Claim slot | Evidence state | Confidence and contradiction | Remaining decisive check |
| --- | --- | --- | --- |
| Language supports freestanding mechanisms | Tagged source, author implementation and local object/ELF probes | High for expression/link feasibility; no boot claim | Accepted linker/startup and exact guest boot |
| C calls/layout/callbacks are viable | Documented convention plus mixed GCC/Zig execution | High for the small tested subset | Every intended boundary type, errors, lifetime and target invocation |
| C translation is reliable for all APIs | Refuted as a blanket claim by source limitations and deferred macro errors | Bounded only; old documentation lags 0.16 | Pin translator and compile intended binding consumers |
| All C libraries can be reused | Refuted by libc/platform dependency contracts | Library-specific assessment required | Selected component import/helper/service census |
| Zig supplies memory/lifetime/temporal safety | Not established; language checks are narrower | No global safety claim | Kernel ownership/race/negative tests and real measurements |
| Compiler is mature enough for a bounded PoC | Supported conditionally by tooling/project evidence | Known defects and changing interfaces remain | Pin, regression corpus, disassembly and upgrade qualification |
| Physical Intel target is supported | No local physical evidence | Unknown installed-unit details | Separate T7500 inventory and M1 physical gate |

## Archive verification

Archive validation passed: 572 completed documents, 28 directories, 5,594
local links, 349 source notes and 21 deep-dive manifests. This session adds
13 source notes and reuses 2. Git whitespace and shell syntax checks passed.
No validator/schema code changed, so its unit suite was not rerun.

Independent factual reviews checked C/ABI/probe limits and scholarly/practitioner
attribution. Their fixes clarify pending QEMU qualification, exact primary
publication titles and diagnostic-specific negative-test handling. The M0
decision edits preserve task IDs, descriptions before children, needs-based
work counts and the final integration-tests section; no delivery checkbox or
acceptance result changed. The complete diff and new document bundle were
reviewed for stale paths and accidental changes. All changes remain uncommitted;
no push or PR was requested or performed.

## Source manifest

### Newly introduced sources

- [Zig 0.16.0 language reference](../30-sources/zig-project-2026-language-reference-0-16.md) — language mechanisms and safety limits.
- [Zig 0.16.0 release and compatibility changes](../30-sources/zig-project-2026-release-0-16.md) — current release and version-sensitive changes.
- [Zig 0.16.0 freestanding build and runtime source profile](../30-sources/zig-project-2026-freestanding-source-profile.md) — calling conventions, build controls and runtime integration.
- [Zig C translator: bitfields and unsupported statements](../30-sources/zig-project-2026-c-translator-limits.md) — translation failure boundaries.
- [Clang 21.1.0 freestanding compilation contract](../30-sources/llvm-project-2025-clang-21-freestanding.md) — C helper requirements.
- [Newlib C library system-call dependencies](../30-sources/newlib-project-2026-libc-system-hooks.md) — portable-libc service hooks.
- [musl and its Linux syscall dependency](../30-sources/musl-project-2026-linux-dependency.md) — Linux dependency boundary.
- [LZ4 1.10.0 freestanding library profile](../30-sources/collet-2024-lz4-freestanding-profile.md) — concrete restricted C fallback.
- [Making No-Fuss Compiler Fuzzing Effective](../30-sources/groce-et-al-2022-no-fuss-compiler-fuzzing.md) — peer-reviewed historical compiler robustness evidence.
- [Pragma Driven Shared Memory Parallelism in Zig by Supporting OpenMP Loop Directives](../30-sources/kacs-et-al-2024-zig-openmp.md) — peer-reviewed foreign-runtime integration.
- [Writing Hypervisor in Zig and the Ymir implementation](../30-sources/smallkirby-2024-writing-hypervisor-in-zig.md) — Intel low-level practitioner mechanisms and limits.
- [Bootstrapping Uber's Infrastructure on arm64 with Zig](../30-sources/lubys-et-al-2023-uber-zig-toolchain.md) — industrial C-toolchain adoption versus language adoption.
- [Ashet OS: Zig operating-system practice and scope](../30-sources/ashet-technologies-2026-operating-system.md) — primary OS implementation context.

### Reused sources

- [SysV AMD64 procedure ABI](../30-sources/x86-psabi-project-2026-amd64-procedure-abi.md) — procedure, red-zone and processor-state boundaries.
- [Intel system programming documentation](../30-sources/intel-2026-system-programming-documentation.md) — vendor architecture authority distinct from language facilities and physical qualification.

## Threads

The [qualification inquiry](../40-inquiries/can-zig-meet-the-kernel-qualification-contract.md)
tracks the unresolved executable contract. The [topic map](../10-maps/zig-kernel-development.md)
connects evidence classes without replacing this manifest.

## Follow-ups

Seek the submitted thesis/code/results behind the
[LLZig bachelor-project record](https://www.sra.uni-hannover.de/Theses/2025/BA-LLZig.html)
if stronger direct scholarly kernel evidence becomes useful. Its completed
status and prospective text do not demonstrate successful Linux integration.
A surfaced ESP32-P4 thesis was not used because full-text retrieval failed.
MicroZig's inspected development-version dependency was contextual, not a
proposed stable-release or T7500 dependency.

Prioritize the synthesis's M0 ABI/build qualification and M1 transition tests
over another general language comparison. No follow-up research, monitor,
implementation, installation or Git publication is started automatically.
