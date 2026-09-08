---
title: "Proof-of-concept requirements"
kind: map
created: "2026-09-06"
tags:
  - archive-navigation
  - directory-index
  - proof-of-concept
  - requirements
aliases:
  - "CLI-first PoC requirement research"
---

# Proof-of-concept requirements

## Purpose

Deep-dive studies of every requirement group in the [readiness assessment](../proof-of-concept-research-readiness.md). The 19 requirement reports cover the four implementation work packages, integrated acceptance criteria and all six deferred capability rows. They translate papers, specifications, implementation articles and blogs into proposed contracts, failure cases and next experiments.

Research supports starting a bounded implementation. The T7500 with Intel x86-64 is now the adopted target, but this does not supply an executable target pin, a working kernel, an executable ABI, a compiled compatibility corpus or measured containment. None of M0–M4 is closed by this writing pass.

The first delivery is a native user-mode CLI. The completed proof of concept also requires the project's compiled-BEAM profile and automatic process-local tracing GC outside the privileged kernel. AtomVM and graphical UI are excluded.

## What belongs here

Requirement-level synthesis and operational tests for the selected proof-of-concept scope. Broader layer/component reports retain alternatives and eventual-system goals. Primary-source records belong in [Sources](../../30-sources/README.md); exact new/reused provenance belongs in the [research journal](../../50-journal/2026-09-06-proof-of-concept-requirements-deep-dive.md).

Each report distinguishes source evidence, proposed Atom contracts and missing experimental evidence. Requirement numbers are navigation identifiers introduced by this research, not pre-existing specification IDs.

## Index

### Subdirectories

- None.

### Documents

The two language feasibility studies, their comparison and two target records complement the nineteen requirement reports:

- [Zig versus C for the kernel](zig-versus-c-kernel-language-comparison.md) — evidence-weighted pros/cons, conditional recommendation, fair-comparison limits and circumstances favoring C.
- [C kernel feasibility and low-level compatibility](c-kernel-language-feasibility-and-low-level-compatibility.md) — alternative/fallback assessment, C/compiler/ABI/library contracts and local research probes; preserves the selected Zig decision.
- [Zig kernel feasibility and C interoperability](zig-kernel-language-feasibility-and-c-interoperability.md) — selected kernel language, scientific/practitioner evidence, bounded local probes and remaining compiler/ABI qualification; extends R02 without closing M0.
- [Dell Precision T7500 target and minimal QEMU profile](dell-precision-t7500-target-and-minimal-qemu-profile.md) — active architecture decision, minimum configuration and prioritized remaining hardware research.
- [Dell Precision T7500 platform reference](dell-precision-t7500-platform-reference.md) — manufacturer capabilities for the selected machine; installed components still require inventory.

The table inventories all requirement reports and their traceability. M0–M4 refer to the assessment's existing milestones; “After M4” is explicitly outside the minimum proof.

| ID | Research document | Stage | Readiness requirements covered |
| --- | --- | --- | --- |
| R01 | [Target, firmware, and boot handoff](target-firmware-and-boot-handoff.md) | M0–M1 | Pinned virtual machine and feature profile; firmware/bootloader dependencies; Intel x86-64 entry, ACPI and conservative memory map; trusted boot boundary |
| R02 | [Freestanding build and static images](freestanding-build-and-static-images.md) | M0–M1 | Language/compiler/linker/ABI; startup and enabled register state; static native image and BEAM bundle; dependencies and reproducible build identities |
| R03 | [Privilege entry, memory protection, and user return](privilege-entry-memory-and-user-return.md) | M1–M2 | Entry and trap frames; kernel/user protection; page accounting and W^X; validated user buffers and return |
| R04 | [Serial console and minimal CLI](serial-console-and-minimal-cli.md) | M1–M3 | User command environment; help/version/uptime; bounded parser and errors; waits; later mem/ps/services/restart/beam-profile/run controls |
| R05 | [Time, preemption, and CPU budgets](time-preemption-and-cpu-budgets.md) | M1–M4 | Clock and deadline source; timer progress; non-yielding domain containment; budget/interrupt overrun; two-level responsiveness |
| R06 | [Capabilities, syscalls, and bounded IPC](capabilities-syscalls-and-bounded-ipc.md) | M2 | Finite object ABI; rights/payer/identity/generation; server-funded invocation; notification/event adapters; cancellation and stale completion |
| R07 | [Domain lifecycle and safe reclamation](domain-lifecycle-and-safe-reclamation.md) | M2–M4 | Closed admission; bounded destruction; terminal transport disposition; local invalidation/quiescence; generations; reservation conservation |
| R08 | [BEAM profile, loader, and conformance](beam-profile-loader-and-conformance.md) | M3 | Exact OTP/compiler/module hashes; chunks/opcodes/BIF/library closure; malformed input and transactional load; core versus genuine OTP profiles |
| R09 | [Runtime adapter, signals, and native services](runtime-adapter-signals-and-native-services.md) | M3 | Independent interpreter placement; host import audit; async actor to kernel transport; reduction safe points; signal order; native boundary |
| R10 | [Private heaps and tracing garbage collection](private-heaps-and-tracing-garbage-collection.md) | M3–M4 | Term roots and forwarding; long-lived process reclamation; collector workspace; shared binary lifetime; same-runtime delay |
| R11 | [Resource accounting and mailbox overload](resource-accounting-and-mailbox-overload.md) | M2–M4 | Physical/kernel/runtime ledger; quotas and funded failures; atoms/code/binaries/timers/mailbox/slack; ordinary send semantics; overload actions |
| R12 | [Supervision and independent recovery](supervision-and-independent-recovery.md) | M2–M4 | Static launch/registry graph; separate CLI/recovery/runtime/native domains; actor versus domain restart; independent reserves; volatile outcomes and reset escalation |
| R13 | [Models, fault injection, and measurement](models-fault-injection-and-measurement.md) | M0–M4 | Finite models/fairness; clean build and serial harness; safety negative tests; deterministic schedules; raw metrics/percentiles; campaign seeds and 1000 restarts |
| R14 | [Durable state and crash consistency](durable-state-and-crash-consistency.md) | After M4 | Block/flash backend; atomicity/ordering/flush/corruption; log/checkpoint; failure during recovery |
| R15 | [Networking and remote actor boundaries](networking-and-remote-actor-boundaries.md) | After M4 | NIC/stack; buffer/timer/entropy dependencies; peer/session identity; bounded queues; transport versus effect; interoperability |
| R16 | [DMA driver isolation and recovery](dma-driver-isolation-and-recovery.md) | After M4 | Requester and reset scope; IOMMU mappings/completion; delayed DMA/stale descriptors; quarantine/reuse |
| R17 | [Multicore and platform portability](multicore-and-platform-portability.md) | After M4 | Second Intel x86-64 CPU; stop/shootdown/publication races; socket/NUMA and later second ISA; physical single-CPU bring-up can follow M1 earlier |
| R18 | [Authentication and administration profile](authentication-and-administration-profile.md) | After M4 | Local-console threat model; human/workload authority; trusted input; entropy/keys; revocation/recovery and multi-tenant enforcement |
| R19 | [Updates and recovery-root survival](updates-and-recovery-root-survival.md) | After M4 | Image selection/authenticity/freshness; migration/rollback cutoff; prepositioned fallback; root replacement and takeover |

## Recommended reading and decision order

1. Read R01–R04 and freeze one target/build/handoff record, static native image subset and byte/time interface. Then implement and test the first real user-mode prompt.
2. Use R05–R07 and R11–R13 to define finite objects, CPU/memory funding, invocation terminal states, close/reuse and independent recovery. Write the small models before optimizing these paths.
3. Use R08–R10 to compile the smallest real workload, generate its dependency closure and implement the independent interpreter and tracing collector. Hosted semantics precede, but do not replace, guest integration.
4. Operate the four-domain demonstration through the CLI and run the M4 campaign with declared capacities and response thresholds.
5. Read R14 first for a durable local service after M4. R15–R19 are additional capability gates, not reasons to postpone the CLI.

The [T7500 / Intel x86-64 target](dell-precision-t7500-target-and-minimal-qemu-profile.md) supersedes the earlier RV64/QEMU/OpenSBI hypothesis and the corrected AMD-processor assumption. Exact binary pins, native ABI and physical inventory remain open. Fixed-period budgets require an explicit boundary-burst rule. Finite OTP calls can require aliases and monitors. Private heaps do not guarantee same-runtime latency, and a timeout does not prove absence of an accepted effect. These are cross-report constraints that implementation must preserve.

## Evidence strength and remaining artifacts

| Decision | Research result | Decisive artifact still missing |
| --- | --- | --- |
| First boot | T7500 / Intel x86-64, Zig kernel language and minimum virtual constraints adopted; responsibilities specified | Qualified Zig/build/ABI profile, exact tool/firmware/image identities and reset-to-user trace |
| Kernel contract | Bounded admission, payment, generations and reclamation have defensible precedents | Operation table, lifecycle/accounting models and negative protection tests |
| BEAM compatibility | A narrow project interpreter is a coherent route; selected OTP paths enlarge its closure | Compiler-produced corpus, generated manifest and hosted/guest differential results |
| Responsiveness and recovery | Domain protection and actor responsiveness are distinct tests | Predeclared limits, raw delay/resource traces and repeated restart results |
| Later capabilities | Storage, networking, DMA, portability, security and updates have separate failure models | Concrete backend/device/deployment selection and capability-specific experiments |

The original nineteen-report session used 36 substantive records: 12 introduced in that session and 24 reused. The [earlier retargeting journal](../../50-journal/2026-09-06-amd64-retargeting-deep-dive.md) preserves source provenance; its AMD-processor assumption is superseded by the [T7500 correction](../../50-journal/2026-09-06-t7500-target-correction.md). Search scope and retrieval limitations are recorded in the journal. This is a targeted engineering deep dive, not an exhaustive systematic review of all OS literature.

## Maintaining this index

Inventory every direct child report here and keep its requirement coverage and stage accurate. New scope requires an explicit requirement or demonstrated research need. Update the [PoC map](../../10-maps/proof-of-concept.md), readiness assessment and open inquiry when a decision changes. Do not mark a report stable or a gate complete without the required evidence.
