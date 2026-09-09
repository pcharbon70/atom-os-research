---
title: "Kernel architecture internal-service decomposition deep dive"
kind: journal
created: "2026-09-08"
tags:
  - architecture-support
  - kernel-architecture
  - literature-review
aliases: []
---

# Kernel architecture internal-service decomposition deep dive

## Context and scope

Expand components 0, 1, 2, 4, 5, 6, 7, 8 and 10 of the [kernel architecture component corpus](../20-notes/kernel-hardware-and-architecture-components/README.md), following the existing internal-service decompositions of components 3 and 9.

The user explicitly clarified that this is full-system architecture research, not proof-of-concept research or QEMU qualification. No laboratory board, emulator configuration, milestone or implementation acceptance defines the scope. Preserve comparative x86-64, AArch64 and RISC-V mechanism reasoning. Zig remains selected, with language capabilities separated from architectural guarantees.

The question is whether each remaining component can be decomposed into reviewable service contracts without losing its integrated ownership, failure and completion semantics. The operational standard is an explicit owner, state/protocol, boundary, alternatives, source constraints, negative cases and falsification criteria for every proposed service—not evidence that those services already exist.

## Method

1. Read the repository conventions, schema, templates, eleven-component directory inventory, existing service examples and relevant parent component protocols.
2. Apply the deep-research skill's evidence workflow. Three independent evidence reviews covered boot/execution, ordering/events/time, and CPU/I/O/facade contracts. They gathered evidence without editing the archive; the main synthesis reconciled boundaries and retained responsibility for the documents.
3. Search primary specifications, scholarly papers and first-party engineering articles. Search families included relaxed exception semantics and NMI handling; posted device writes and NAPI; sequence-counter lifetime and timekeeping; CPU admission and stop; DMA transfer, IOMMU groups and maintenance; and typed asynchronous interfaces in Tock.
4. Prefer actual sections and full papers over abstracts or snippets. Reuse existing bibliographic records instead of creating duplicates for the same work. Distinct newly examined API documents receive separate records.
5. Prepare one canonical report source and a claim/source ledger before rendering the Markdown bundle. Distinguish source claims, inherited parent contracts and our unverified service proposals.
6. Review cross-service identity, lifetime, acceptance, completion and recovery composition. Preserve the parent protocols where local state sketches omit detail.

No local kernel, compiler, model-checking, emulator or hardware experiment was performed. Proposed tests in the reports are falsifiers, not executed evidence. Scientific publications inform mechanisms and failure models; none validates the proposed combined architecture.

## Reading depth and access limitations

Fresh section-level review included the new Arm exception paper and tutorial, the Arm NMI article, the Tock deployment retrospective, and the Linux device-I/O, NAPI, sequence-counter and VFIO documents. The new notes record the inspected sections and each source's limits.

Revisited primary material included OSKit's environment dependencies, CertiKOS's refinement boundaries, CleanQ's cooperative ownership model, Thunderclap's DMA attacks, Tock HIL submission/completion rules, Zig's lifetime/atomic/assembly contracts, Linux entry and CPU-hotplug guidance, PSCI start/stop semantics, and research on instruction publication, kernel memory models and timekeeping. The evidence reviews also compared LazyFP, Multikernel and the polling study against their actual evaluation scope. Sources used only through existing archive analysis remain reused evidence, not newly replicated results.

Important version/read boundaries:

- UEFI 2.11 retrieval was blocked. The retry/service-lifetime check used the official [UEFI 2.10_A boot-services chapter](https://uefi.org/specs/UEFI/2.10_A/07_Services_Boot_Services.html), especially §§7.2.3 and 7.4.6. This is explicitly a fallback, not a claim to have re-read those sections in 2.11. After the first ExitBootServices attempt, only the specified restricted retry services remain admissible; generic cleanup rollback is unsafe.
- ACPI 6.6 table handling was checked in §5.2.6 of the [official PDF](https://uefi.org/sites/default/files/resources/ACPI_Spec_6.6.pdf). Devicetree checks used the tagged v0.4 source chapters, not a misleading unversioned/stable documentation label.
- Intel system-programming and VT-d landing pages were available, but fresh full chapter validation was not obtained. The current Arm architecture-manual landing page did not provide readable manual content. Existing archive readings remain the basis for those normative claims, supplemented by the explicitly identified Arm tutorial and research.
- RISC-V supervisor and instruction-fetch checks used v20260120; the timekeeping review used the separately identified v20250508 Sstc text, and SBI checks used version 3.0. The current IOMMU documentation reader failed, so no new chapter-level IOMMU validation is claimed.
- SMMUv3 G.b §§4.7.3–4.8 were freshly inspected for synchronization, error and command-consumption distinctions. Equivalent fresh validation was not obtained for every other remapper.
- Linux latest documentation is a moving target accessed on this date, not a pinned source checkout. These API contracts cannot be imported as Zig's memory model.
- Older published experimental results remain tied to their processors, workloads and implementations. They are not measurements of this system, universal latency bounds or evidence of current vulnerabilities in every system.

The source manifest below records substantive source-note use, including archived readings. It is not a claim that every source was freshly read cover to cover. Publication metadata is recorded only where known.

## Resulting decomposition

- [0. Normalized boot handoff and feature discovery](../20-notes/kernel-hardware-and-architecture-components/normalized-boot-handoff-and-feature-discovery/README.md) — 6 service reports. Separate provider lifetime, parsing, physical-resource reconciliation, discovery, and final publication. These six boundaries prevent a successful provider transaction from being mistaken for validated kernel facts.
- [1. Unsafe architecture-primitives capsule](../20-notes/kernel-hardware-and-architecture-components/unsafe-architecture-primitives-capsule/README.md) — 5 service reports. Separate the contract inventory, privileged state, memory effects, device/wait effects and binary boundary. These are private mechanism services, never a second capability or policy layer.
- [2. Privileged entry, exit and execution context](../20-notes/kernel-hardware-and-architecture-components/privileged-entry-exit-and-execution-context/README.md) — 6 service reports. Separate early admission, semantic frames, return authority, context ownership, nested failure and transition security. All six share the parent entry state; none duplicates component 9's capture or disposition owner.
- [4. Ordering, coherence and code publication](../20-notes/kernel-hardware-and-architecture-components/ordering-coherence-and-code-publication/README.md) — 7 service reports. Seven distinct services separate ordinary synchronization, device completion, maintenance planning, sealing, publication, membership catch-up and retirement. Visibility, execution eligibility and reclamation are deliberately not one notion of completion.
- [5. Interrupt event fabric](../20-notes/kernel-hardware-and-architecture-components/interrupt-event-fabric/README.md) — 6 service reports. Six services separate source identity, electrical/controller flow, bounded evidence, binding lifetime, accounting and polling handoff. Kernel IPI transport remains owned by component 7 and consumes this fabric rather than duplicating a second request protocol.
- [6. Raw time and deadline programming](../20-notes/kernel-hardware-and-architecture-components/raw-time-and-deadline-programming/README.md) — 6 service reports. Six services distinguish source quality, arithmetic, snapshot lifetime, continuity, hardware programming and terminal outcomes. Diagnostic sampling and delay bounds are part of source qualification; timer queues, civil time and scheduling policy remain above this component.
- [7. Logical-CPU coordination and lifecycle](../20-notes/kernel-hardware-and-architecture-components/logical-cpu-coordination-and-lifecycle/README.md) — 6 service reports. Separate CPU identity, admission, bounded remote work, removal, policy eligibility and uncertain recovery. The six services share one lifecycle authority; none independently declares a CPU safely stopped.
- [8. Protected I/O and DMA ownership](../20-notes/kernel-hardware-and-architecture-components/protected-io-and-dma-ownership/README.md) — 7 service reports. Separate device identity, memory authority, transfer, maintenance, revocation, reset and fault custody. These seven services refine one protected-I/O lifecycle rather than inventing independent buffer or device owners.
- [10. Typed kernel-facing architecture facade](../20-notes/kernel-hardware-and-architecture-components/typed-kernel-facing-architecture-facade/README.md) — 6 service reports. Separate object identity, admission, asynchronous custody, backend profiles, completion composition and conformance. These six services expose existing component authority rather than introducing a second hardware-management layer.

This adds 55 service reports in nine directories. Together with the existing nine component-3 and six component-9 reports, all eleven parent components now have internal-service research decompositions: 70 service reports in total. This is coverage of documented contracts, not closure of the research questions.

## Cross-service findings and claim ledger

| Boundary | Source constraint or negative evidence | Proposed architectural consequence | Remaining decisive evidence |
| --- | --- | --- | --- |
| Boot custody | Provider service lifetime and validated data lifetime differ | Own inputs and legal post-exit resources before sealing facts | Parser bounds and partial-exit recovery model |
| Privileged leaves | Source structure does not establish compiler or machine effects | Per-operation effect schemas plus generated-code checks | Versioned binary/ABI validation |
| Entry and return | Exceptions are not universal barriers; hardware saves only selected state | Separate context preservation, synchronization and hostile-return validation | Nested-event and extended-state refinement |
| Code publication | Local synchronization and remote readiness differ | Incarnation-bound membership and publication completion | Concurrent writer/admission/retirement proof |
| Interrupts | Masking, device service, acknowledgement and ownership differ | Flow-specific state machines and bounded recording | Lost-wakeup, teardown and overload exploration |
| Time | Consistency, storage lifetime and bounded retry differ | Protected snapshots, explicit continuity eras and sticky terminal ownership | Wrap, source change and cancellation traces |
| CPUs | Start requests and online admission differ; timeout is not stop | Dependency-ledger admission and irreversible stop commitment | Complete multi-owner drain proof |
| DMA | Cooperative ownership does not stop a hostile device | Explicit enforced/shared/trusted profiles and joined revocation | Alias closure, remapper completion and device-drain proof |
| Facade | Typed interfaces still need runtime boundary checks | Canonical protected state, context admission and scoped joins | Zig handle adversarial tests and backend conformance |

These consequences are our synthesis. Across the protocols, an acknowledgement is evidence only for its exact operation, range, generation, profile and participant set. Uncertainty retains custody; it does not automatically authorize reclamation. At-most-once completion safety is not a promise of eventual delivery after arbitrary failure.

The facade parent contained an obsolete Rust recommendation. It is reconciled with the selected Zig language: structs, tagged results, opaque boundaries and static binding can express the design, but copied handles require protected-state generation and authority validation. This change does not claim that Zig supplies a borrow checker or linear types.

## Confidence and remaining work

Confidence is strongest in the identified distinctions and published counterexamples. Confidence in the proposed decomposition is provisional: it has been reasoned through against the parent models, not mechanically refined or implemented.

The next architecture research should prioritize compositional proofs at the joins: publication against CPU admission/removal; mapping restriction against every privileged CPU alias; device revocation against translated and already-issued traffic; and split-phase ownership after caller or recovery failure. Qualification must state the execution environment, trust base, privilege level, failure model and specification version.

Additional open questions include bounded quarantine capacity, generation exhaustion, progress under interrupted writers or unresponsive participants, availability of independent recovery authority, and whether every advertised cross-ISA profile has a genuine semantic refinement. Keep the [architecture inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) open.

## Verification and handoff

`python3 validate_archive.py` passed: 666 completed documents, 38 directories, 6,531 local links and 369 source notes checked. Its 24 deep-dive manifests classify 357 introduced and 431 reused source uses; 12 source notes retain their documented pre-manifest provenance. `git diff --check` passed, and a separate whitespace scan of untracked files found no trailing whitespace. The new service set was checked for missing contract fields and accidental milestone/emulator scope; none was found. The tracked changes were reviewed for stale paths and unrelated rewrites.

No implementation tests were run. Validator code and schema were unchanged, so validator unit tests were not required. Research changes remain uncommitted; no push or pull request is authorized by this request.

## Source manifest

### Newly introduced sources

- [AArch64 Exception Model](../30-sources/arm-2025-aarch64-exception-model.md) — Hardware exception capture is only part of software context preservation.
- [Linux device-I/O contracts](../30-sources/linux-kernel-community-2026-device-io-contracts.md) — Posted-write receipt differs from CPU-side ordering.
- [Relaxed exception semantics for Arm-A](../30-sources/simner-et-al-2024-relaxed-exception-semantics.md) — Precise exception transitions are not general memory barriers.
- [Linux NAPI](../30-sources/linux-kernel-community-2026-napi-contracts.md) — Budgeted processing and explicit masking/ownership handoff.
- [A-profile non-maskable interrupts](../30-sources/dall-2022-a-profile-non-maskable-interrupts.md) — NMI masking and stack-state behavior are feature-specific.
- [Sequence counters and sequential locks](../30-sources/linux-kernel-community-2026-sequence-counter-contracts.md) — Reader consistency does not establish pointer lifetime or bounded progress.
- [Tock deployment retrospective](../30-sources/schuermann-et-al-2025-tock-decade.md) — Typed interfaces still require sound ABI and runtime validation.
- [VFIO isolation groups](../30-sources/linux-kernel-community-2026-vfio-isolation-groups.md) — Device functions do not necessarily form independent isolation units.

### Reused sources

- [ACPI 6.6](../30-sources/uefi-forum-2025-acpi-6-6.md) — Structured discovery with explicit table validation.
- [Arm A-profile architecture](../30-sources/arm-2026-a-profile-system-architecture-documentation.md) — Architecture-specific exception, ordering and state contracts.
- [BootStomp](../30-sources/redini-et-al-2017-bootstomp.md) — Empirical motivation for adversarial early-input analysis.
- [Arm threaded code-publication article](../30-sources/bramley-2025-arm-self-modifying-code-threads.md) — Writer-side synchronization does not synchronize every executing core.
- [CertiKOS](../30-sources/gu-et-al-2016-certikos.md) — Observable refinement with explicit machine-model exclusions.
- [CleanQ](../30-sources/haecki-et-al-2019-cleanq.md) — Transfer-set conservation under cooperative ownership assumptions.
- [Devicetree 0.4](../30-sources/devicetree-org-2023-devicetree-specification-0-4.md) — Bounded blob structure and reserved-memory descriptions.
- [Linux entry/exit handling](../30-sources/linux-kernel-community-2026-entry-exit-handling.md) — Ordering and instrumentation restrictions in partial entry states.
- [Intel system-programming documentation](../30-sources/intel-2026-system-programming-documentation.md) — ISA-specific privileged state and completion requirements.
- [Timecounters](../30-sources/kamp-2002-timecounters.md) — Wrap-aware conversion and matched source/anchor publication.
- [LazyFP](../30-sources/stecklina-prescher-2018-lazyfp.md) — Negative evidence for fault-triggered extended-state isolation.
- [Limine boot protocol](../30-sources/limine-project-2026-limine-boot-protocol.md) — Versioned provider handoff, not a kernel ABI.
- [Linux low-level core APIs](../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.
- [Concurrency in the Linux kernel](../30-sources/alglave-et-al-2018-linux-kernel-concurrency.md) — Executable litmus models and reclamation reasoning.
- [Meltdown](../30-sources/lipp-et-al-2018-meltdown.md) — Architectural access denial is not a complete transient-execution boundary.
- [The Multikernel](../30-sources/baumann-et-al-2009-multikernel.md) — Explicit inter-core protocols and replicated-state tradeoffs.
- [Flux OSKit](../30-sources/ford-et-al-1997-flux-oskit.md) — Component dependencies include their execution environment.
- [When poll is better than interrupt](../30-sources/yang-et-al-2012-when-poll-is-better-than-interrupt.md) — Workload-dependent evidence, not a universal polling advantage.
- [Time protection](../30-sources/ge-et-al-2019-time-protection.md) — Temporal isolation exceeds timer precision.
- [Arm PSCI 1.3](../30-sources/arm-2024-power-state-coordination-interface.md) — Firmware CPU requests and OS admission have different states.
- [RISC-V IOMMU architecture](../30-sources/risc-v-international-2026-iommu-architecture.md) — A distinct device-translation and command-completion profile.
- [RISC-V privileged architecture](../30-sources/risc-v-international-2026-privileged-architecture.md) — Privilege and trap semantics qualified by extensions.
- [RISC-V unprivileged architecture](../30-sources/risc-v-international-2026-unprivileged-architecture.md) — Local instruction-fetch synchronization scope.
- [RISC-V SBI](../30-sources/risc-v-international-2025-supervisor-binary-interface.md) — Separate higher-privilege start and remote-operation contracts.
- [seL4 reference manual](../30-sources/sel4-foundation-2026-reference-manual.md) — Capability-mediated authority and distinct kernel object kinds.
- [Serval](../30-sources/nelson-et-al-2019-serval.md) — Symbolic machine-code analysis within a declared model.
- [Arm SMMUv3 architecture](../30-sources/arm-2025-smmuv3-architecture.md) — IOMMU command and translation-cache synchronization scope.
- [Thunderclap](../30-sources/markettos-et-al-2019-thunderclap.md) — DMA spatial and temporal exposure despite translation protection.
- [High-resolution timekeeping research](../30-sources/terraneo-cattaneo-2026-high-resolution-timekeeping.md) — Separating shared timekeeping from per-CPU preemption.
- [Tock HIL design](../30-sources/tock-project-2026-hil-design.md) — Submission, returned ownership and asynchronous completion contracts.
- [Translation validation for a verified OS kernel](../30-sources/sewell-et-al-2013-translation-validation.md) — Checking compiler output rather than trusting source structure.
- [x86-TSO](../30-sources/sewell-et-al-2010-x86-tso.md) — Store buffering within a deliberately limited formal domain.
- [UEFI specification](../30-sources/uefi-forum-2024-uefi-2-11.md) — Provider memory-map and service-lifetime contracts.
- [Intel VT-d architecture](../30-sources/intel-2024-vt-d-architecture.md) — I/O translation and invalidation completion are separate mechanisms.
- [Zig language reference](../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.

## Follow-ups

Use the service-specific falsifiers to choose subsequent architecture experiments. Do not mark the inquiry resolved or the proposed contracts verified from this writing pass.
