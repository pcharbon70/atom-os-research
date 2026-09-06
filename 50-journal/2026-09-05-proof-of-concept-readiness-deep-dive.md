---
title: "2026-09-05 proof-of-concept readiness deep dive"
kind: journal
created: "2026-09-05"
tags:
  - proof-of-concept
  - repository-audit
  - research-assessment
  - research-session
aliases:
  - "Atom OS readiness assessment session"
---

# 2026-09-05 proof-of-concept readiness deep dive

## Observations

- Research coverage is sufficient to begin a bounded bootable prototype.
  There is no experimental basis yet for asserting that the integrated
  architecture satisfies its proposed guarantees.
- The confirmed first delivery is a minimal OS that boots into a CLI. The
  user explicitly rejected AtomVM and excluded graphical UI from this proof
  of concept. An initial reuse recommendation was withdrawn accordingly.
- The main next tasks are a reproducible target/build profile, a small native
  user-space CLI and kernel interface, the project's BEAM runtime and exact
  compatibility corpus, and resource/recovery experiments.
- The larger layer inquiries include evidence requirements that exceed a
  useful first prototype. They should remain open while the smaller
  integration milestone is tested.
- BEAM integration should occur before SMP and DMA in the proposed prototype
  sequence so the fixed platform requirement is tested early.
- Storage, networking, security, and visual computing have substantial
  research. They need concrete backends, profiles, tests, or user evidence
  before their respective capabilities can be claimed.

## Environment

- Repository: `/home/ducky/code/atom-os-research`.
- Assessed Git revision: `ae3d77d39bca10d2f61e56be975d37e54314be6d`.
- Initial worktree: clean, verified with `git status --porcelain=v1`.
- Review host: Linux x86_64; Python 3.12.12; Bash shell.
- Review date: 2026-09-05, America/Toronto local date.
- No Atom kernel, runtime port, emulator guest, hardware target, or model
  checker was built or run. The only executable checks were archive diagnostics
  and validation. No packages or toolchain versions were installed.
- The user confirmed the minimal bootable OS and CLI-first scope. No ISA,
  emulator version, firmware, or toolchain was selected by the user. QEMU
  RISC-V and the proposed campaign sizes remain recommendations.

## Evidence

### Inventory and structural baseline

The inspection used repository status, tracked/untracked file inventories,
frontmatter searches, the home map, directory indexes, and journal evidence.
Representative commands actually used included:

```bash
git status --porcelain=v1
git rev-parse HEAD
git log -5 --oneline
rg --files -g '!*.md' -g '!__pycache__/**'
rg -n '^maturity:|^status:' 20-notes 40-inquiries
python3 validate_archive.py
git diff --check
```

The assessed archive contained 103 notes, all `developing`, 300 source notes,
nine inquiries, all `open`, and sixteen deep-dive journals. The non-Markdown
inventory contained `frontmatter.schema.json`, `requirements-validation.txt`,
`validate_archive.py`, and `test_validate_archive.py`. The assets directory
had no retained attachments. These observations are limited to this checkout.

Baseline validator output:

```text
Archive validation passed: 455 completed documents, 18 directories, 4410 local links, and 300 source notes checked; 16 deep-dive source manifests classify 288 introduced and 311 reused source uses; 12 source notes entered outside a deep-dive manifest.
```

`git diff --check` produced no output and exited successfully.

### Research review method

The assessment traced the nine inquiry workbenches and layer conclusions,
implementation programs, evidence limits, and critical component contracts.
Detailed attention went to bootstrap and authority handoff, transport funding,
kernel and actor scheduling, the runtime adapter, loader/profile verification,
signals, tracing collection, resource accounting, domain recovery, translation
reclamation, storage, and networking. The application and visual inquiries
were used to distinguish a bootable systems experiment from a useful durable
desktop.

The review did not independently reread all 300 primary works or verify every
component state machine. Papers cited inside existing syntheses were not
silently treated as newly audited primary inputs. The source manifest below
classifies the six existing primary-source notes directly used and the one
new official platform record.

The earlier [AtomVM journal](2026-08-28-atomvm-deep-dive.md) records a
configuration/build attempt stopping at missing `gperf` and unselected
Erlang/rebar versions. The [runtime inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
and [kernel inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
explicitly record absent implementation/model/conformance evidence. This
session did not repeat the build or establish whether those prerequisites are
still missing on the present host.

### Current primary-document checks

Official web pages were opened and relevant body text read on 2026-09-05:

- [OTP 29.0.6 patch record](https://www.erlang.org/patches/OTP-29.0.6)
  confirmed the 2026-09-01 release and ERTS 17.0.6 baseline.
- [OTP compatibility policy](https://www.erlang.org/doc/system/misc.html)
  confirmed that binary compatibility is directional and version-sensitive.
- [ERTS collection documentation](https://www.erlang.org/doc/apps/erts/garbagecollection.html)
  confirmed the process-oriented tracing/copying mechanism used as reference
  evidence. No collector timing result was inferred.
- [AtomVM differences](https://doc.atomvm.org/main/differences-with-beam.html)
  retained the development-version label and documented limited OTP behavior
  and absent code reloading. This informed the initial candidate assessment;
  it is retained as historical evidence, not an active implementation gate.
- [QEMU virt documentation](https://www.qemu.org/docs/master/system/riscv/virt.html)
  supplied the candidate-platform evidence. The page displayed 11.1.50; no
  released or installed executable was inferred from that label.

An attempted OTP security-page URL returned an error and was not used as
evidence. Native failure-boundary conclusions here rely on the existing
runtime/source audit and architecture reports, not on that failed retrieval.
No new audit of the OTP 29.0.6 source tree was performed; the older broad
29.0.5 source audit retains its original scope.

### User scope correction on 2026-09-05

After the initial assessment, the user stated that AtomVM had been officially
rejected and that the proof of concept should build a minimal bootable OS,
starting with a CLI and excluding the graphical UI. This is a project decision
reported by the user, not a new technical finding about AtomVM. No rejection
rationale or new failed implementation experiment was supplied or inferred.

The assessment and active research program now exclude any AtomVM port,
dependency, reuse experiment, or comparison milestone. The former candidate
note, inquiry, and map were moved to `90-archive/`, and their incoming links
were repaired. The inquiry is paused, not experimentally resolved. Source
notes and prior journal evidence remain intact. The source manifest below
preserves AtomVM inputs to the original, now-withdrawn reuse recommendation.

### Resulting model and evidence boundary

The revised assessment proposes four user-mode domains in the integrated
demonstration: CLI, independent outer recovery/control, the project's BEAM
runtime, and a native test/I/O service. Five implementation gates, M0–M4,
sequence reproducible build inputs, native CLI boot, protected service
lifecycle, CLI-launched BEAM execution with tracing GC, and measured
containment/recovery. Conditional follow-ups cover durability, networking,
DMA, SMP, security, updates, and root recovery. Graphical UI is outside this
proof of concept.

The first CLI contract proposes bounded serial input and `help`, `version`,
and `uptime`, followed by lifecycle commands once the service mechanisms
exist. A privileged debug monitor is scaffolding, not completion of that
user-space CLI milestone. Neither the target recommendation nor the decision
to begin with a native CLI is evidence of a successful boot.

The report distinguishes kernel-enforced progress across domains from
same-runtime responsiveness during GC, message scans, and native work. It also
separates actor restart, runtime replacement, volatile state reset, durable
recovery, and uncertain external outcomes. No benchmark, compatibility,
isolation, recovery, or proof result was produced by writing these contracts.

### Archive outputs and verification

Created the synthesis, an integration-gate inquiry, a selective prototype map,
one QEMU source note, and this journal. Updated their directory inventories,
the sources provenance table, and the home map. The initial assessment
validation, before the CLI-first correction, passed:

```text
Archive validation passed: 460 completed documents, 18 directories, 4479 local links, and 301 source notes checked; 17 deep-dive source manifests classify 289 introduced and 317 reused source uses; 12 source notes entered outside a deep-dive manifest.
```

The correction also updated repository instructions, the archive introduction,
the broader BEAM research program and inquiry, and active navigation. Three
candidate documents were archived; their historical evidence was preserved,
and the former AtomVM inquiry was paused. Final correction validation is
recorded below:

```text
Archive validation passed: 460 completed documents, 18 directories, 4482 local links, and 301 source notes checked; 17 deep-dive source manifests classify 289 introduced and 317 reused source uses; 12 source notes entered outside a deep-dive manifest.
```

`git diff --check` passed. The final active-document search found only explicit
exclusions and historical references to AtomVM, not a remaining candidate gate.

Validation code and schema behavior were unchanged, so validator unit tests
were not required for this documentation change. All assessment and scope
correction changes remain uncommitted. No kernel or CLI implementation was
created by this documentation pass.

## Source manifest

### Newly introduced sources

- [QEMU RISC-V virt platform documentation](../30-sources/qemu-project-2026-risc-v-virt-platform.md) — supplied official evidence for a candidate emulated target and its firmware/platform boundary.

### Reused sources

- [OTP 29.0.6 managed-runtime documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md) — supplied the public compatibility and tracing-collection baseline, with targeted current official checks.
- [OTP source tree at 5cf5f9725452](../30-sources/erlang-otp-team-2026-otp-29-source-tree.md) — supplied the historical ERTS host-dependency and native-runtime audit and its version/evidence limits.
- [AtomVM main documentation](../30-sources/atomvm-project-2026-main-documentation.md) — supplied historical compatibility input to the initial reuse recommendation, subsequently withdrawn after the user's rejection.
- [AtomVM source tree at 0220c78e](../30-sources/atomvm-project-2026-source-tree.md) — supplied historical platform-seam and prerequisite-limited build evidence for the subsequently withdrawn candidate path.
- [RISC-V privileged architecture](../30-sources/risc-v-international-2026-privileged-architecture.md) — informed the proposed separation of supervisor kernel, user domains, and architecture-specific completion obligations.
- [RISC-V supervisor binary interface](../30-sources/risc-v-international-2025-supervisor-binary-interface.md) — informed the explicit higher-privilege firmware dependency in a candidate target profile.

## Threads

- [Proof-of-concept research readiness](../20-notes/proof-of-concept-research-readiness.md)
  is the durable assessment and proposed implementation scope.
- [Minimal bootable-system inquiry](../40-inquiries/can-a-minimal-bootable-system-validate-the-architecture.md)
  tracks the still-open integration gates.
- [Proof-of-concept map](../10-maps/proof-of-concept.md) is the selective
  route through existing evidence and proposed next work.

## Follow-ups

- Pin the target/build inputs, define the minimal console/time kernel interface,
  and obtain a reproducible boot into the native user-space CLI.
- Add protected service lifecycle and independent CLI recovery before extending
  the command set to expose those mechanisms.
- Implement the project's declared BEAM profile using upstream OTP as compiler
  and semantic oracle; integrate it through the CLI before SMP/DMA. Retain raw
  conformance, resource, and recovery evidence in a new experimental journal.
- Select the next capability from product needs after the integrated proof;
  the default recommendation is one durable CLI-operated local service.
  Graphical UI remains outside this proof of concept.
