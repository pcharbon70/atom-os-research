---
title: "M0 — Boot Inputs"
kind: map
created: "2026-09-08"
tags:
  - archive-navigation
  - boot
  - directory-index
  - implementation-planning
  - m0
  - proof-of-concept
aliases:
  - "M0 milestone definition"
---

# M0 — Boot Inputs

## Purpose

M0 turns the x86-64 compatibility envelope and architectural intent into concrete inputs
that someone else can build, inspect, and run. Its question is: **Do we know
exactly what will boot, how control reaches our kernel, what that kernel may
assume, and how a failed run will be detected?** A list of preferred tools or a
sample QEMU command does not answer that question.

The outcome is a versioned boot/build contract and an exercised validation
toolchain, ready for [M1's native user-mode CLI](../m1-boot-to-cli/README.md).
M0 need not already deliver that interactive CLI. It does need real artifacts
and checks rather than unresolved version placeholders or instructions that
only work in the author's shell environment.

## What belongs here

This milestone owns the initial virtual baseline, build inputs, firmware and
loader handoff, native image contract, minimal console/time interface, test
harness, and the boundary that keeps virtual evidence separate from later
physical-fixture qualification. It also makes the trusted-local-development
boundary explicit before privileged code depends on it.

M0 does not implement the protected service nucleus, complete BEAM profile,
collector, persistent filesystem, NIC stack, SMP/NUMA, human login, or GUI.
The minimum fixture remains Intel x86-64, one logical CPU, 64 MiB, and serial
I/O. A host-provided build or debugger is allowed and identified; a host OS
inside the guest supplying the claimed kernel mechanisms is not.

## Planning and delivery state

This milestone has a draft phased implementation plan. Phase 1 completed and
received a proceed decision on 2026-09-18. The public Kay OS repository, Zig 0.16.0
LLVM/LLD profile, QEMU 8.2.2 `pc-q35-8.2`/`Nehalem-v1` fixture, SeaBIOS 1.16.3,
and 64 MiB limit are selected and pass baseline identity checks. Freestanding
build qualification passed at implementation commit `be4a230`, and the clean
Phase 1 virtual integration suite passed all nine registered cases at
implementation commit `b350de9` and merged `main` revision `bc4c998`. The
former physical-inventory dependency did not block Phase 2 contract work and
has now been moved to M1 Phase 4. Phase 2 Section 2.1 and its clean 24-case integration are
complete at implementation commit `f85571e`; independent follow-up review
found no blocker, [evidence is retained](../../../50-journal/2026-09-18-m0-phase-02-contract-integration.md),
and the user/project owner selected proceed on 2026-09-19. Phase 3 M0-D03 was
resolved on 2026-09-20 with fixed harness timing, protocol, retention, cleanup
and observation-only physical-fixture collection decisions. Section 3.1 is
complete at clean Kay OS revision `8206deb`: all nine controlled harness cases
passed, the publication boundary behaved as declared, and the virtual M1 input
bundle was assembled without physical inventory. Full phase integration and
every complete milestone acceptance case remain open. Writing or reviewing a plan
neither closes a delivery gate nor substitutes for retained execution evidence.

## Authoritative inputs

These inputs define the existing scope and the research behind its tests:

- [Readiness assessment](../../../20-notes/proof-of-concept-research-readiness.md) — M0 exit criteria and work package 1.
- [Target and firmware handoff, R01](../../../20-notes/proof-of-concept-requirements/target-firmware-and-boot-handoff.md) — entry ownership, reservations, bounded handoff parsing, and failure policy.
- [Freestanding build and images, R02](../../../20-notes/proof-of-concept-requirements/freestanding-build-and-static-images.md) — compiler dependencies, image admission, and reproducibility.
- [Zig feasibility and C interoperability](../../../20-notes/proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md) — accepted language decision and research basis for the now-exercised bounded 0.16.0 freestanding profile; later interfaces still require their own qualification.
- [Kay OS implementation repository](https://github.com/pcharbon70/kay-os) — owns executable manifests, scripts, fixtures and retained implementation evidence for the selected profile.
- [Phase 1 build-closure record](../../../50-journal/2026-09-17-m0-phase-01-build-closure.md) — exact tested revision, environment, artifact hash, audits, negative cases and limitations for `m0-p01-build`.
- [Phase 1 virtual-integration record](../../../50-journal/2026-09-17-m0-phase-01-virtual-integration.md) — clean tested revision, registered cases, finite deadlines, hashes and the explicit physical-inventory boundary for `m0-p01-integration`.
- [Phase 1 merged-baseline closeout](../../../50-journal/2026-09-18-m0-phase-01-merged-baseline-closeout.md) — clean merged-main rerun, exact merge revisions and accepted proceed decision for `m0-p01-handoff`.
- [Phase 2 contract-integration record](../../../50-journal/2026-09-18-m0-phase-02-contract-integration.md) — clean `f85571e` run, all 24 registered results, exact supply-chain/tool/artifact identities, independent review and explicit hosted-only boundary.
- [Serial CLI, R04](../../../20-notes/proof-of-concept-requirements/serial-console-and-minimal-cli.md) and [time, R05](../../../20-notes/proof-of-concept-requirements/time-preemption-and-cpu-budgets.md) — interfaces that must be fixed before M1 implements them.
- [Measurement and harness, R13](../../../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md) — exact inputs, negative checks, and retained evidence.
- [x86-64 compatibility envelope](../../../20-notes/proof-of-concept-requirements/x86-64-compatibility-envelope-and-test-fixtures.md) and [configuration intent](../../../assets/qemu-minimal-x86-64.json) — generic platform boundary and minimal virtual baseline, not a claim about a physical motherboard.
- [Parent stream](../README.md) and [planning convention](../../README.md) — milestone order, evidence rules, and later phase structure.

## Entry decisions and dependencies

The generic Intel-compatible x86-64 envelope, CLI-first scope, rejection of AtomVM, Zig
kernel language, public Kay OS repository, Zig 0.16.0 LLVM/LLD profile and
initial virtual fixture are decided. M0 must finish qualifying these inputs and
resolve the remaining contracts without mistaking prior research examples for
accepted selections:

| Decision to close | What the record must establish | Downstream dependency |
| --- | --- | --- |
| Zig toolchain and source location | Preserve the selected Zig kernel language; accept repository location, compiler/backend/linker/translator versions, required host tools, and C/helper closure; qualify the freestanding link and intended ABI subset. | All subsequent native code and reproducible builds. |
| Virtual binary and device fixture | Pin QEMU, a versioned q35 machine, `Nehalem-v1`, TCG, SeaBIOS, serial backend, and boot-media configuration; verify their availability together. | M1's boot and serial tests. |
| Bootloader and handoff | Select a loader compatible with the fixture and record entry mode, long-mode ownership, retained memory, firmware tables, and additional-CPU policy. | Kernel entry and memory initialization. |
| Native execution contract | Select the static image subset, layout, calling convention, stack policy, enabled register state, and syscall mechanism. | Native loader, exception entry, and validated ring-3 return. |
| Console, time, and failures | Define bounded calls, clock units/conversion, input framing, error results, interrupts/waits, and initial fault halt/reset behavior. | CLI and unattended pass/fail interpretation. |
| Physical qualification boundary | Preserve a reusable read-only observation/publication procedure, but collect a fixture's actual inventory only in M1 Phase 4 immediately before its physical test. | Later physical-fixture qualification only; never virtual M0/M1 handoff or kernel configuration. |

The compiler profile must not inherit host-native instruction selection or
Linux syscalls accidentally. If bring-up restricts FP/SIMD, describe and check
that restricted profile; do not label it full native ABI support. Timer and
processor features must be qualified rather than inferred from a modern
manual. The selected compiler profile does not select a loader or optional CPU
mode. Phase 1 demonstrated only its declared fixed-signature qualification ABI;
later kernel interfaces and processor-state transitions require fresh evidence.

## Required artifacts

The artifacts jointly address the coverage table's missing exact VM/firmware
profile and the input side of the small executable ABI. They are inputs to
M1's running implementation, not substitutes for it.

| ID | Artifact | Required content and observable result |
| --- | --- | --- |
| M0-A01 | Pinned virtual execution manifest | Exact tool/binary identities, versioned machine and CPU features, accelerator, topology, RAM, serial and boot devices, and hashes. A launcher rejects missing pins or unsupported features instead of silently selecting defaults. |
| M0-A02 | Reproducible build and dependency closure | Source revision/dirty state, tools and flags, linker script/map, helper/import census, symbols, and repeatable clean-build commands. Minimal native fixtures actually compile/link; every guest helper is supplied or rejected. |
| M0-A03 | Boot/handoff and reservation contract | Reset-to-entry responsibility, stack/register preconditions, bounded snapshot schema, conservative usable/reserved memory rules, boot images and firmware lifetime, required table checks, and finite failure handling. Include valid and malformed test fixtures. |
| M0-A04 | Static native image and initial ABI specification | Supported headers/segments/relocations, entry and permission rules, initialized-data/BSS handling, stack/register-state policy, and minimal console/time operation definitions with bounded buffers and errors. Include machine-checkable descriptors or validation fixtures. |
| M0-A05 | Development trust and initial authority profile | Trusted host/firmware/loader/kernel, potentially faulty user domain, permitted console/time grants, private kernel state, and deliberate exclusions. Input from a trusted local operator is not authentication evidence. |
| M0-A06 | Executable host acceptance harness | Version-checking launch wrapper, serial input/capture/assertions, finite watchdog and cleanup, nonzero failure results, and per-run artifact manifest. Demonstrate both success interpretation and failure detection using explicitly labelled harness fixtures. |
| M0-A07 | Physical-fixture qualification boundary and safe-observation procedure | Versioned read-only collection/publication rules, explicit transfer to M1 Phase 4, and a prohibition on consuming physical inventory as virtual configuration. Actual fixture observations and Kay OS discovery comparison are M1 evidence. |

An image hash identifies bytes, not authority to execute them. Initial native
images and later BEAM bundles need separate authority/resource descriptors.
The JSON configuration intent must be replaced or consumed by a validated
launcher; it is not itself a QEMU configuration file or an executed-run record.

## Responsibility and trust boundary

The host owns compilation, emulation, debugger control, deadlines for a stuck
test process, and evidence capture. Firmware and the loader own the documented
pre-kernel path. The future Kay kernel owns validation and protection after
handoff; a firmware memory claim is still input to validate.

Read-only physical inventory does not authorize a firmware update, persistent
BIOS change, or disk overwrite. Unknown installed hardware must remain unknown
in a fixture record, not be filled from a product-family specification.
Physical observations are test-oracle and safety evidence for M1 Phase 4; they
are neither M0 inputs nor evidence that Kay OS discovered the same facts.

## Integration acceptance

These are milestone acceptance cases, not numbered implementation phases.
They test the consistency and executability of the combined inputs. Fixture
success at M0 must be labelled separately from a real user-mode boot at M1.

| ID | Acceptance case | Artifacts | Passing evidence |
| --- | --- | --- | --- |
| M0-T01 | Resolve the complete environment | A01, A02 | A clean environment can locate the exact inputs and execute the declared compiler/linker/launcher checks; unavailable CPU/machine/firmware identities fail clearly. |
| M0-T02 | Reproduce build outputs | A02, A04 | Two clean builds in different absolute directories reproduce fixture identities, or identify and justify narrowly permitted nondeterminism per artifact. Undefined helpers and unsupported generated instructions fail the check. |
| M0-T03 | Reconcile handoff with image layout | A03, A04 | Valid fixture reservations and segments agree; truncated records, overflow/overlap, invalid entry points, unsupported image features, and conflicting memory claims are rejected without publishing an executable image. Guest enforcement is tested in M1. |
| M0-T04 | Check interface and authority consistency | A04, A05 | Every initial operation has a bounded request/response, defined error/time semantics, a permitted caller, and an enforcing owner. No CLI grant implies arbitrary physical-memory or root authority. |
| M0-T05 | Prove the harness can detect failure | A01, A06 | Controlled prompt/response fixtures pass; missing prompt, incorrect response, launch failure, stalled serial stream, timeout, and early process death fail and leave useful logs. No hang is mistaken for success. |
| M0-T06 | Review the physical/virtual distinction | A01, A03, A07 | The M1 bundle consumes no physical inventory; q35 is not claimed as motherboard evidence; the safe observation procedure and successor M1 Phase 4 tasks are explicit. |

The required startup/link smoke tests and parser/harness fixtures must have
real outputs. If a reset-to-entry smoke image is used, state precisely which
entry stages it reaches. It must not be presented as the delivered CLI, safe
user return, or completed runtime.

## Evidence and milestone exit

M0 exits when the required artifacts exist at named revisions, decisions have
been resolved for the selected profile, and every required acceptance case
passes with retained evidence. Keep each artifact linked to its checks and
retain commands, hashes, outputs, environment, and limitations in dated
[journal evidence](../../../50-journal/README.md), with artifacts in
[assets](../../../assets/README.md) or the selected implementation repository.
A required missing virtual pin is open, not a pass. The 2026-09-21 scope
decision moves installed-unit observation and comparison to M1 Phase 4 without
waiving that later physical evidence.

The M1 handoff includes the manifests, native/boot contracts, malformed-input
fixtures, working build and harness entry points, symbol association, and
known constraints. M1 must reproduce them before claiming the interactive
delivery. Freeze no BEAM compatibility promise here beyond preserving its
later unprivileged placement and a bounded way to package modules.

## Ordered phases

3 phases separate independently verifiable outcomes; their section/task/sub-task
counts follow the work rather than a quota. Phase 1 is complete. Phase 2 has
completed its decision, executable-contract and clean integration work and
received the user's proceed decision on 2026-09-19. Phase 3 owns the unattended
harness, virtual M1 input bundle and final M0 qualification. Review
dependencies and unresolved gates before execution.

| Phase | Integrated outcome | Entry dependency | State / evidence |
| --- | --- | --- | --- |
| [Phase 1 — Target, toolchain, and build baseline](phase-01-target-toolchain-and-build-baseline.md) | Turn the generic Intel-compatible x86-64 envelope into a versioned, reproducible virtual baseline. This phase qualifies build inputs and native link fixtures, not a user-mode OS or physical machine. | accepted-scope-entry | Complete; merged-main nine-case rerun passed and user recorded proceed; [closeout](../../../50-journal/2026-09-18-m0-phase-01-merged-baseline-closeout.md) |
| [Phase 2 — Boot, image, and interface contracts](phase-02-boot-image-and-interface-contracts.md) | Specify and exercise the handoff, native image, console/time, and initial authority contracts before the guest kernel implements them. | m0-p01-handoff | Complete; clean `f85571e` integration passed 24/24 registered cases, independent review found no blocker and user selected proceed on 2026-09-19; [evidence](../../../50-journal/2026-09-18-m0-phase-02-contract-integration.md) |
| [Phase 3 — Acceptance harness and input qualification](phase-03-acceptance-harness-and-input-qualification.md) | Deliver an exercised unattended acceptance harness, assemble the virtual M1 input bundle, and prove that physical inventory is not consumed as configuration. | m0-p02-handoff | In progress; Section 3.1 passed at clean `8206deb` and assembled the inventory-free virtual bundle; [evidence](../../../50-journal/2026-09-21-m0-phase-03-section-31-qualification.md); full integration not run |

Work within each phase follows its task dependencies. The serial order provides
a conservative baseline, not authorization for parallel agents. Independent
experiments may be proposed separately; their results cannot bypass a gate.

## Decision register

Zig and the initial Phase 1 execution profile are accepted by user decision;
remaining qualification and later-phase choices stay open. Each row names its
resolution task, evaluation criteria and blocked work. Later-phase execution
and acceptance reviewers remain unassigned.
M0-D01 owns the initial implementation repository and toolchain selection.

| Decision ID | Choice and criteria | Resolution task and phase | Responsible role | Blocks | State |
| --- | --- | --- | --- | --- | --- |
| M0-D01 | Preserve Zig as the kernel language; select the implementation repository and qualify the compiler/backend/linker/translator using freestanding support, ABI/helper closure, instruction control, reproducibility, and maintenance cost; assign execution/review roles. Verify exact QEMU/firmware availability without relying on physical-family specifications. | [m0-p01-decisions](phase-01-target-toolchain-and-build-baseline.md) | Phase 1 implementation agent and user acceptance reviewer | Virtual Phase 1 and later native work | Phase 1 accepted: public `pcharbon70/kay-os`, Zig 0.16.0 LLVM/LLD, QEMU 8.2.2 and SeaBIOS 1.16.3 selected; merged-main [closeout](../../../50-journal/2026-09-18-m0-phase-01-merged-baseline-closeout.md) passed |
| M0-D02 | Choose loader/long-mode ownership, static image subset, native calling and register-state policy, syscall mechanism, console framing, clock units, and initial fault policy using bounded validation and generic x86-64/baseline compatibility. | [m0-p02-decisions](phase-02-boot-image-and-interface-contracts.md) | Codex implementation agent, independent review agent, and user acceptance reviewer | Remaining Phase 2 work and its dependent gates | Resolved 2026-09-18: Limine v12.9.0/base revision 6, fixed higher-half static ELF64, restricted System V AMD64, later DPL3 interrupt gate/TSS/`iretq`, bounded copy console, monotonic-nanosecond clock, bounded emergency serial then halt, deterministic read-only BIOS ISO |
| M0-D03 | Freeze watchdog deadlines, serial assertions, output retention, cleanup rules, and the virtual/physical qualification boundary before interpreting runs. | [m0-p03-decisions](phase-03-acceptance-harness-and-input-qualification.md) | Codex implementer and user/project owner decision reviewer | Remaining Phase 3 work and its dependent gates | Resolved 2026-09-20 and revised 2026-09-21: Python host harness; versioned ASCII PTY fixture; 5/2/3/30/5-second limits; complete per-run retention; process-group TERM/KILL cleanup; physical collection procedure transferred to M1 Phase 4 and does not gate M0 |

## Gate-to-phase and artifact mapping

Rows map contributions, not automatic acceptance. The phase task tables give
stable implementation IDs; the integration task exercises the mapped cases
and the handoff task records evidence. Shared cases retain their full definition
above and close only after all required environments and dependent portions pass.

| Phase gate | Artifact contributions | Acceptance coverage | Owning tasks | Entry dependency | Evidence / state |
| --- | --- | --- | --- | --- | --- |
| [M0-P01](phase-01-target-toolchain-and-build-baseline.md) | M0-A01, M0-A02 | M0-T01, M0-T02 virtual-input portions | m0-p01-decisions, m0-p01-build; m0-p01-integration; m0-p01-handoff | accepted-scope-entry | Complete; merged-main [closeout](../../../50-journal/2026-09-18-m0-phase-01-merged-baseline-closeout.md) passed and handoff decision is proceed |
| [M0-P02](phase-02-boot-image-and-interface-contracts.md) | M0-A03, M0-A04, M0-A05 | M0-T02, M0-T03, M0-T04 | m0-p02-decisions, m0-p02-fixtures; m0-p02-integration; m0-p02-handoff | m0-p01-handoff | Complete for the declared pre-boot phase scope: clean `f85571e` integration passed 24/24 registered cases, independent review found no blocker and user selected proceed on 2026-09-19; [evidence retained](../../../50-journal/2026-09-18-m0-phase-02-contract-integration.md) |
| [M0-P03](phase-03-acceptance-harness-and-input-qualification.md) | M0-A01, M0-A02, M0-A03, M0-A04, M0-A05, M0-A06, M0-A07 | M0-T01, M0-T02, M0-T03, M0-T04, M0-T05, M0-T06 | m0-p03-decisions, m0-p03-harness, m0-p03-qualify; m0-p03-integration; m0-p03-handoff | m0-p02-handoff | In progress: Section 3.1 passed at clean `8206deb`, including the inventory-free virtual bundle; [evidence](../../../50-journal/2026-09-21-m0-phase-03-section-31-qualification.md); full integration and handoff remain open; `m0-p03-inventory` was superseded before execution by M1 Phase 4 |

The final phase reruns all M0 acceptance cases for milestone closure.
Earlier contract, fixture, model or hosted results remain partial where guest
integration is required. Physical evidence stays visible under M1 Phase 4 but
does not gate virtual M0. An acceptance reviewer must retain failure history,
record the accepted tested revision, and reopen gates on incompatible input
changes, missing required evidence or a violated invariant.

## Index

### Subdirectories

- None yet.

### Documents

- [Phase 1 — Target, toolchain, and build baseline](phase-01-target-toolchain-and-build-baseline.md) — Turn the generic Intel-compatible x86-64 envelope into a versioned, reproducible virtual baseline and qualify native build inputs without making a physical-machine claim.
- [Phase 2 — Boot, image, and interface contracts](phase-02-boot-image-and-interface-contracts.md) — Specify and exercise the handoff, native image, console/time, and initial authority contracts before the guest kernel implements them.
- [Phase 3 — Acceptance harness and input qualification](phase-03-acceptance-harness-and-input-qualification.md) — Deliver an exercised unattended acceptance harness, assemble the virtual M1 input bundle and enforce the physical-fixture boundary.

## Maintaining this index

Inventory each phase or supporting child document when created, and keep
artifact/test IDs, resolved decisions, evidence links, and the parent stream
consistent. Preserve this milestone's distinction between qualified inputs
and M1's working OS; do not check off delivery because this definition is
written. Do not renumber accepted artifact or test identities silently.
