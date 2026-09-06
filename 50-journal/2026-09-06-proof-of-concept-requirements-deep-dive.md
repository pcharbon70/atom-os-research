---
title: "2026-09-06 proof-of-concept requirements deep dive"
kind: journal
created: "2026-09-06"
tags:
  - beam
  - boot
  - deep-dive
  - proof-of-concept
  - requirements
  - research-session
aliases: []
---

# 2026-09-06 proof-of-concept requirements deep dive

## Observations

The user requested a deep dive into each requirement in the [readiness assessment](../20-notes/proof-of-concept-research-readiness.md), using scientific papers, articles and blogs, with reports in a subdirectory. This session created [19 connected requirement reports](../20-notes/proof-of-concept-requirements/README.md), covering M0–M4 and all six later-capability rows.

The confirmed scope remains a custom bootable OS whose first delivery is a native user-mode CLI. Compiled BEAM and automatic process-local tracing GC outside the privileged kernel remain requirements for the completed proof. AtomVM and graphical UI are excluded.

Research began on 2026-09-05 and continued across the local date boundary. Source access dates record 2026-09-05; new archive documents were created on 2026-09-06. This session is distinct from the earlier readiness assessment. Existing source notes are reused even where their files were still uncommitted.

The resulting decision is still conditional readiness to implement. Reading clarifies failure models and contract choices, but cannot supply the missing pinned boot, executable kernel/runtime, conformance or recovery evidence.

## Environment

- Repository: /home/ducky/code/atom-os-research, Markdown archive.
- Host role: source retrieval, archive analysis and document validation only.
- Proposed guest: one RV64 hart, QEMU virt, Sv39, explicitly identified OpenSBI, S-mode Atom kernel and U-mode services. No release, firmware build, compiler or address layout was adopted or executed.
- First threat profile: trusted host, firmware, kernel and boot images; user domains may fault, loop, exhaust resources or submit unauthorized requests. Hostile actors sharing one runtime, physical attacks and speculative channels are not established claims.
- Worktree: pre-existing readiness and AtomVM archival edits were preserved. No commit, push or publication was requested.

## Research method and search scope

The operational question was: what must be selected, implemented and tested to satisfy every readiness requirement without widening the minimum proof? Requirement groups were extracted from the four work packages, CLI table, six safety properties, integrated demonstration, milestone/negative-evidence lists and six post-PoC rows.

The Deep Research skill guided independent evidence reviews for kernel contracts, runtime requirements and later capabilities while the coordinator researched boot/build/CLI and integrated the reports. It also guided a claim/source ledger and canonical drafting source; these internal working files are not additional archive reports.

Searches targeted the named technical questions: RISC-V/QEMU/OpenSBI handoff and UART bring-up; freestanding ABI/ELF/reproducibility; capability IPC, temporal authority and reclamation; BEAM loader/GC/signal and generic-call closure; crash consistency; QUIC flow control; IOMMU completion; cross-core publication; authenticator/entropy requirements; and update/root recovery.

Primary papers and official specifications/documentation carried normative and research claims. First-party implementation articles and blogs supplied operational examples and design explanations, with their limitations recorded. Full text or relevant source-code sections were read for substantive claims; search snippets were discovery aids, not detailed evidence. This was a targeted engineering review, not an exhaustive systematic review with a complete literature-search recall claim.

The manifest contains 36 substantive source records: 12 newly introduced and 24 reused. Existing broader syntheses provided context and navigation; their entire bibliographies were not silently treated as reread evidence.

Discovery stopped once every requirement group had primary support or an explicit limitation, the consequential source discrepancies were resolved, and the remaining uncertainties required a concrete implementation/profile choice or experiment. The coordinator independently checked the finite generic-call path and FSCQ disk-model distinction. Another broad search was unlikely to decide the still-unselected compiler, device or numerical operating limits.

## Evidence and findings

### Boot and toolchain

Official QEMU platform documentation supports a manageable synthetic target, but the moving master pages displayed version 11.1.50 and are not an installed executable pin. OpenSBI dynamic and configured-jump handoffs need different predecessor/layout assumptions. A reset-to-user trace remains the decisive M0/M1 artifact.

The rendered Devicetree “stable” page identified itself as v0.3-dirty. The versioned v0.4 flattened-format source was used instead. The UART walkthrough is helpful but historical: multi-cell addresses require concatenation, and a UART clock is not evidence of CPU/timer frequency.

Freestanding compilation still needs startup, linking, support-library and generated-helper audits. The procedure ABI does not define the kernel syscall ABI. ELF describes segments but does not supply a hostile-input verifier or mandate Atom's strict W^X policy.

### Kernel and runtime composition

Finite capability/object tables require explicit admission, payer, terminal disposition and reuse rules. Server-funded leaf services reduce initial complexity but do not eliminate server saturation or permit blocking the runtime's only scheduler.

Fixed-period CPU budgets allow boundary-straddling bursts. Neither aggregate utilization nor a timer interrupt proves response-time bounds when privileged work is unbounded.

The tagged OTP 29.0.6 generic-call source has different local infinite and finite-timeout paths. Finite calls require alias/monitor and cleanup semantics. This is a targeted source-file check, not a new whole-tree audit or compiled opcode census.

Private tracing heaps meet an ownership/GC requirement, not an automatic same-runtime latency bound. The GC paper's shared/private organization and workload-specific timing cannot be promoted to a new interpreter's deadline guarantee. Global atoms, code, binaries, timers, mailbox storage and collector workspace remain in the resource ledger.

### Recovery and later capabilities

A managed supervisor can replace an actor only while its runtime works. Independent recovery needs separate protection, authority, CPU, memory, fault delivery and replacement capacity. Repeated successful launches without reclamation fail the intended recovery claim.

The existing [durable-state component](../20-notes/otp-like-system-services-components/durable-state-transactions-and-outcome-recovery.md) incorrectly referred to FSCQ's synchronous disk model. The paper models asynchronous disk writes and builds a synchronous transactional interface above them. That sentence was corrected; no storage implementation result changed.

Transport flow control does not bound every local buffer or establish durable application effects. IOMMU completion does not necessarily drain requests still upstream. Local translation/instruction synchronization does not establish remote-core completion. Authentication, update acquisition, activation, data migration and recovery-root takeover each need distinct contracts.

### Evidence quality and unresolved decisions

| Area | Confidence in responsibility/requirement | Remaining uncertainty and next decisive evidence |
| --- | --- | --- |
| Boot/build/CLI | Strong specification and teaching-implementation support | Exact tool/firmware/layout selection; real U-mode prompt and negative parser/protection tests |
| Bounded kernel operations | Strong precedents; Atom encoding remains proposed | Executable operation table and bounded lifecycle/accounting models |
| BEAM/OTP profile | Strong evidence that dependency closure matters | Compiler-generated corpus, exact supported manifest and hosted/guest conformance |
| GC and responsiveness | Strong ownership distinction; performance unmeasured | Live-set/allocation/mailbox/budget sweeps and separate actor/domain delays |
| Independent recovery | Strong topology precedent; composition untested | Four-domain fault campaign, reserve conservation and 1,000 fixed-capacity restarts |
| Later capabilities | Defensible failure models, no qualified backend/profile | Device, storage, stack, second-target and security/update selection experiments |

“Strong” describes support for the engineering obligation, not confidence that an unimplemented Atom design will pass.

## Retrieval limitations

- The coordinator's RISC-V supervisor HTML retrieval failed twice; the independent architecture review successfully read the versioned official page. The report uses that review and the existing source record rather than claiming a repeated successful fetch.
- An initial QEMU replay URL failed; the official system/replay.html and GDB pages were read.
- Some attempted OTP source fetches failed. Only the successful tagged gen.erl inspection is claimed as newly introduced source-code evidence.
- Shapiro's original institutional PDF endpoint was unavailable; the kernel review used an author-uploaded full-text copy with matching publication identity.
- Moving official documentation and nightly tool help are labeled as such. No documentation version was substituted for a tested binary version.

These limitations are recorded rather than filled with inferred implementation results.

## Local verification

Commands run from the repository root:

```text
python3 validate_archive.py
Archive validation passed: 493 completed documents, 19 directories,
4711 local links, and 313 source notes checked; 18 deep-dive source
manifests classify 301 introduced and 341 reused source uses;
12 source notes entered outside a deep-dive manifest.

git diff --check
Exit 0; no whitespace errors.
```

All 33 newly created archive files were read back and matched the reviewed
drafts. A coverage check confirmed all 19 reports contain primary-source links,
acceptance sections and connections. Per-file `git diff --no-index --check`
checks also covered the 33 new files and three related untracked PoC documents,
with no whitespace diagnostics. The changed indexes, map, inquiry, assessment
and storage correction were reviewed; pre-existing changes were preserved.

Markdown received structural/content review, not a rendered visual review;
native visual inspection was unavailable through the enabled UI controls.
No validator or schema behavior changed, so validator unit tests were not
required. No guest, compiler fixture, model checker, timing benchmark or
fault-injection experiment was run. Changes remain uncommitted.

## Source manifest

### Newly introduced sources

- [xv6: a simple, Unix-like teaching operating system](../30-sources/cox-et-al-2026-xv6-risc-v-book.md) — Teaching implementation of protection, trap entry, UART and wakeups.
- [OTP 29.0.6 generic behaviour call protocol](../30-sources/erlang-otp-team-2026-otp-29-0-6-generic-behaviour-call-protocol.md) — Tagged finite/infinite call paths and alias/monitor dependency closure.
- [GCC standards and the freestanding environment](../30-sources/gnu-project-2026-gcc-freestanding-environment.md) — Freestanding startup, linking and generated support dependencies.
- [SOURCE_DATE_EPOCH specification](../30-sources/lamb-luo-2017-source-date-epoch.md) — Deterministic build timestamps and the limits of timestamp control.
- [OpenSBI firmware handoff: FW_DYNAMIC and FW_JUMP](../30-sources/opensbi-project-2026-firmware-handoff.md) — Dynamic versus configured-jump firmware handoff and payload placement.
- [All File Systems Are Not Created Equal: On the Complexity of Crafting Crash-Consistent Applications](../30-sources/pillai-et-al-2014-crash-consistent-applications.md) — Persistence-ordering counterexamples and application-level crash testing.
- [QEMU debugging and record/replay](../30-sources/qemu-project-2026-debugging-and-record-replay.md) — Debugger entry control and qualified replay configurations.
- [RISC-V ABIs Specification](../30-sources/risc-v-international-2026-elf-psabi.md) — Procedure ABI, enabled state and the separate syscall contract.
- [TLC model configuration and specification options](../30-sources/tlaplus-project-2026-tlc-model-configuration.md) — Model properties, fairness, bounds and state-constraint limitations.
- [Recommendation for the Entropy Sources Used for Random Bit Generation](../30-sources/turan-et-al-2018-entropy-source-requirements.md) — Entropy-source assumptions, health tests and failure policy.
- [RISC-V from scratch 3: Writing a UART driver in assembly (1 / 3)](../30-sources/twilco-2019-risc-v-uart-driver.md) — First-party UART/DTB bring-up workflow and historical-example cautions.
- [ELF object file format: Program loading](../30-sources/xinuos-2026-elf-program-loading.md) — Native segment loading, lengths, alignment and permission fields.

### Reused sources

- [Timing analysis of a protected operating system kernel](../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md) — Nonpreemptible kernel paths, cleanup work and limits of observed timing.
- [Caches and self-modifying code: Working with threads](../30-sources/bramley-2025-arm-self-modifying-code-threads.md) — Executing-core instruction synchronization and multicore publication limits.
- [Using Crash Hoare Logic for certifying the FSCQ file system](../30-sources/chen-et-al-2015-fscq.md) — Crash-aware storage contracts, recovery interruption and disk-model correction.
- [Devicetree specification, release 0.4](../30-sources/devicetree-org-2023-devicetree-specification-0-4.md) — Versioned flattened-tree format and conservative handoff parsing.
- [NixOS: A Purely Functional Linux Distribution](../30-sources/dolstra-et-al-2008-nixos.md) — Explicit build-input closure and immutable deployment precedent.
- [Erlang/OTP 29.0.6 managed-runtime documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md) — BEAM format, signals, GC, native boundaries and resource semantics.
- [Erlang/OTP 29.0.6 system-services documentation](../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md) — Selected supervisor and behaviour semantics rather than generic restart claims.
- [Construction of a highly dependable operating system](../30-sources/herder-et-al-2006-dependable-operating-system.md) — User-service recovery topology and its core-service/state limits.
- [A brief introduction to BEAM](../30-sources/hogberg-2020-brief-introduction-to-beam.md) — Compiler/interpreter conventions and limits of tutorial-level opcode evidence.
- [QUIC: A UDP-based multiplexed and secure transport](../30-sources/iyengar-thomson-2021-quic.md) — Transport flow control and the separation from application outcomes.
- [Scheduling-context capabilities: A principled, light-weight operating-system mechanism for managing time](../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md) — CPU authority, budgets and server funding alternatives.
- [Read-copy update: Using execution history to solve concurrency problems](../30-sources/mckenney-slingwine-1998-read-copy-update.md) — Removal-before-reclamation and software-reader quiescence.
- [A firmware update architecture for Internet of Things](../30-sources/moran-et-al-2021-firmware-update-architecture.md) — Firmware verification and recovery-image architectural alternatives.
- [How Amazon Web Services Uses Formal Methods](../30-sources/newcombe-et-al-2015-aws-formal-methods.md) — Industrial model-checking experience and model/code evidence boundaries.
- [QEMU RISC-V virt platform documentation](../30-sources/qemu-project-2026-risc-v-virt-platform.md) — Candidate virtual target, generated platform data and host dependencies.
- [RISC-V supervisor binary interface specification](../30-sources/risc-v-international-2025-supervisor-binary-interface.md) — Firmware discovery and absolute supervisor timer deadlines.
- [RISC-V IOMMU architecture specification](../30-sources/risc-v-international-2026-iommu-architecture.md) — DMA translation, command completion and upstream-transaction limits.
- [The RISC-V instruction set manual, privileged architecture](../30-sources/risc-v-international-2026-privileged-architecture.md) — Trap state, protection and local versus remote translation invalidation.
- [Efficient memory management for concurrent programs that use message passing](../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md) — Private/shared heap alternatives and collection-timing evaluation scope.
- [seL4 reference manual, version 16.0.0](../30-sources/sel4-foundation-2026-reference-manual.md) — Capability objects, transport, notifications and scheduling-context mechanics.
- [Vulnerabilities in synchronous IPC designs](../30-sources/shapiro-2003-synchronous-ipc-vulnerabilities.md) — Blocking IPC, reply-path and resource-exhaustion design hazards.
- [Digital identity guidelines: authentication and authenticator management](../30-sources/temoshok-et-al-2025-authentication-and-authenticator-management.md) — Authenticator lifecycle and deployment-specific security scope.
- [The Update Framework Specification version 1.0.36](../30-sources/tuf-project-2026-specification-1-0-36.md) — Signed update metadata, trust roles, freshness and acquisition limits.
- [The Many-to-One Parallel Signal Sending Optimization](../30-sources/winblad-2021-parallel-signal-sending.md) — Concurrent signal ingress and receiver-side processing evidence.

## Threads

- [Proof-of-concept map](../10-maps/proof-of-concept.md) supplies a selective route through the requirement studies.
- [Minimal bootable-system inquiry](../40-inquiries/can-a-minimal-bootable-system-validate-the-architecture.md) remains open; writing does not close M0–M4.

## Follow-ups

1. Freeze one build/firmware/target record, native image format and minimal console/time ABI.
2. Implement the serial test harness and boot to the real native user-mode CLI.
3. Generate the smallest workload's BEAM dependency manifest and formalize the finite kernel lifecycle/accounting contract.
4. Integrate tracing GC and four-domain recovery, then run the predeclared capacity/latency campaign.
5. After M4, select one durable local-service backend; qualify other capabilities only when entering their scope.
