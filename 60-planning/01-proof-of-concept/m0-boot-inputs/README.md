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

M0 turns the selected machine and architectural intent into concrete inputs
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

This milestone owns the initial virtual fixture, build inputs, firmware and
loader handoff, native image contract, minimal console/time interface, test
harness, and installed-unit inventory needed to relate the virtual work to the
Dell Precision T7500. It also makes the trusted-local-development boundary
explicit before privileged code depends on it.

M0 does not implement the protected service nucleus, complete BEAM profile,
collector, persistent filesystem, NIC stack, SMP/NUMA, human login, or GUI.
The minimum fixture remains Intel x86-64, one logical CPU, 128 MiB, and serial
I/O. A host-provided build or debugger is allowed and identified; a host OS
inside the guest supplying the claimed kernel mechanisms is not.

## Planning and delivery state

This milestone now has a draft phased implementation plan. The detailed outcome,
artifact IDs and acceptance criteria below remain authoritative. All tasks are
unchecked, implementation has not started, and every acceptance case is not run.
Open decisions must be resolved before dependent execution; writing or reviewing
a plan neither closes a delivery gate nor authorizes implementation or publication.

## Authoritative inputs

These inputs define the existing scope and the research behind its tests:

- [Readiness assessment](../../../20-notes/proof-of-concept-research-readiness.md) — M0 exit criteria and work package 1.
- [Target and firmware handoff, R01](../../../20-notes/proof-of-concept-requirements/target-firmware-and-boot-handoff.md) — entry ownership, reservations, bounded handoff parsing, and failure policy.
- [Freestanding build and images, R02](../../../20-notes/proof-of-concept-requirements/freestanding-build-and-static-images.md) — compiler dependencies, image admission, and reproducibility.
- [Zig feasibility and C interoperability](../../../20-notes/proof-of-concept-requirements/zig-kernel-language-feasibility-and-c-interoperability.md) — accepted language decision, researched 0.16.0 candidate and remaining executable qualification; research probes do not close M0 tasks.
- [Serial CLI, R04](../../../20-notes/proof-of-concept-requirements/serial-console-and-minimal-cli.md) and [time, R05](../../../20-notes/proof-of-concept-requirements/time-preemption-and-cpu-budgets.md) — interfaces that must be fixed before M1 implements them.
- [Measurement and harness, R13](../../../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md) — exact inputs, negative checks, and retained evidence.
- [T7500 target profile](../../../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md) and [configuration intent](../../../assets/qemu-minimal-x86-64.json) — adopted constraints, not qualified binaries or a working launcher.
- [Parent stream](../README.md) and [planning convention](../../README.md) — milestone order, evidence rules, and later phase structure.

## Entry decisions and dependencies

The T7500 / Intel Xeon target, CLI-first scope, rejection of AtomVM and Zig
kernel language are already decided. M0 must resolve the following implementation inputs without
mistaking prior research examples for accepted selections:

| Decision to close | What the record must establish | Downstream dependency |
| --- | --- | --- |
| Zig toolchain and source location | Preserve the selected Zig kernel language; accept repository location, compiler/backend/linker/translator versions, required host tools, and C/helper closure; qualify the freestanding link and intended ABI subset. | All subsequent native code and reproducible builds. |
| Virtual binary and device fixture | Pin QEMU, a versioned q35 machine, `Nehalem-v1`, TCG, SeaBIOS, serial backend, and boot-media configuration; verify their availability together. | M1's boot and serial tests. |
| Bootloader and handoff | Select a loader compatible with the fixture and record entry mode, long-mode ownership, retained memory, firmware tables, and additional-CPU policy. | Kernel entry and memory initialization. |
| Native execution contract | Select the static image subset, layout, calling convention, stack policy, enabled register state, and syscall mechanism. | Native loader, exception entry, and validated ring-3 return. |
| Console, time, and failures | Define bounded calls, clock units/conversion, input framing, error results, interrupts/waits, and initial fault halt/reset behavior. | CLI and unattended pass/fail interpretation. |
| Physical qualification prerequisites | Record the installed T7500 configuration and identify safe boot/debug media and transport. | Later physical M1 qualification, not a demand for a two-CPU QEMU test. |

The compiler profile must not inherit host-native instruction selection or
Linux syscalls accidentally. If bring-up restricts FP/SIMD, describe and check
that restricted profile; do not label it full native ABI support. Timer and
processor features must be qualified rather than inferred from a modern
manual. The language decision does not select a compiler pin, loader or optional CPU mode.

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
| M0-A07 | T7500 installed-unit and qualification record | Observed CPU SKUs/steppings/features, enabled topology, board/firmware, RAM, relevant devices, and debug path; separate observed facts from unknowns and document boot-media prerequisites. Redact unique service identifiers from public records. |

An image hash identifies bytes, not authority to execute them. Initial native
images and later BEAM bundles need separate authority/resource descriptors.
The JSON configuration intent must be replaced or consumed by a validated
launcher; it is not itself a QEMU configuration file or an executed-run record.

## Responsibility and trust boundary

The host owns compilation, emulation, debugger control, deadlines for a stuck
test process, and evidence capture. Firmware and the loader own the documented
pre-kernel path. The future Atom kernel owns validation and protection after
handoff; a firmware memory claim is still input to validate.

Read-only physical inventory does not authorize a firmware update, persistent
BIOS change, or disk overwrite. Unknown installed hardware must remain unknown
in the record, not be filled from the product family specification. Exploratory
virtual work may use its independently qualified fixture while physical
inventory is pending, but that does not close the missing M0 obligation or
establish T7500 qualification.

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
| M0-T06 | Review the physical/virtual distinction | A01, A03, A07 | Installed-unit evidence and boot/debug prerequisites are documented; q35 assumptions are not claimed as T7500 wiring or timing evidence, and additional physical CPUs have an explicit later bring-up policy. |

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
A required missing pin or inventory is open, not a pass; moving an obligation
requires an explicit reviewed scope decision.

The M1 handoff includes the manifests, native/boot contracts, malformed-input
fixtures, working build and harness entry points, symbol association, and
known constraints. M1 must reproduce them before claiming the interactive
delivery. Freeze no BEAM compatibility promise here beyond preserving its
later unprivileged placement and a bounded way to package modules.

## Ordered phases

3 phases separate independently verifiable outcomes; their section/task/sub-task
counts follow the work rather than a quota. All are draft/not started, with no
execution evidence. Review dependencies and resolve decisions before execution.

| Phase | Integrated outcome | Entry dependency | State / evidence |
| --- | --- | --- | --- |
| [Phase 1 — Target, toolchain, and build baseline](phase-01-target-toolchain-and-build-baseline.md) | Turn the selected Intel target into a versioned, reproducible development fixture and installed-unit record. This phase qualifies inputs and native link fixtures, not a user-mode OS. | accepted-scope-entry | Draft; not started; tests not run |
| [Phase 2 — Boot, image, and interface contracts](phase-02-boot-image-and-interface-contracts.md) | Specify and exercise the handoff, native image, console/time, and initial authority contracts before the guest kernel implements them. | m0-p01-handoff | Draft; not started; tests not run |
| [Phase 3 — Acceptance harness and input qualification](phase-03-acceptance-harness-and-input-qualification.md) | Deliver an exercised unattended acceptance harness and close the complete M0 input gate using real build and fixture evidence. | m0-p02-handoff | Draft; not started; tests not run |

Work within each phase follows its task dependencies. The serial order provides
a conservative baseline, not authorization for parallel agents. Independent
experiments may be proposed separately; their results cannot bypass a gate.

## Decision register

Zig is accepted by user decision; the remaining entry choices stay open. Each row names its resolution task,
evaluation criteria and blocked work; responsible individuals are unassigned.
M0-D01 owns the initial implementation repository and toolchain selection.

| Decision ID | Choice and criteria | Resolution task and phase | Responsible role | Blocks | State |
| --- | --- | --- | --- | --- | --- |
| M0-D01 | Preserve Zig as the kernel language; select the implementation repository and qualify the compiler/backend/linker/translator using freestanding support, ABI/helper closure, instruction control, reproducibility, and maintenance cost; assign execution/review roles. Verify exact QEMU/firmware availability and installed-unit inventory rather than relying on family specifications. | [m0-p01-decisions](phase-01-target-toolchain-and-build-baseline.md) | Unassigned implementer/reviewer; assign before dependent execution | Remaining Phase 1 work and its dependent gates | Partially decided: Zig selected by user on 2026-09-08; toolchain/repository/roles and complete decision acceptance remain open |
| M0-D02 | Choose loader/long-mode ownership, static image subset, native calling and register-state policy, syscall mechanism, console framing, clock units, and initial fault policy using bounded validation and T7500/fixture compatibility. | [m0-p02-decisions](phase-02-boot-image-and-interface-contracts.md) | Unassigned implementer/reviewer; assign before dependent execution | Remaining Phase 2 work and its dependent gates | Open; no decision evidence |
| M0-D03 | Freeze watchdog deadlines, serial assertions, output retention, cleanup rules, and physical qualification prerequisites before interpreting runs. | [m0-p03-decisions](phase-03-acceptance-harness-and-input-qualification.md) | Unassigned implementer/reviewer; assign before dependent execution | Remaining Phase 3 work and its dependent gates | Open; no decision evidence |

## Gate-to-phase and artifact mapping

Rows map contributions, not automatic acceptance. The phase task tables give
stable implementation IDs; the integration task exercises the mapped cases
and the handoff task records evidence. Shared cases retain their full definition
above and close only after all required environments and dependent portions pass.

| Phase gate | Artifact contributions | Acceptance coverage | Owning tasks | Entry dependency | Evidence / state |
| --- | --- | --- | --- | --- | --- |
| [M0-P01](phase-01-target-toolchain-and-build-baseline.md) | M0-A01, M0-A02, M0-A07 | M0-T01, M0-T02, M0-T06 | m0-p01-decisions, m0-p01-inventory, m0-p01-build; m0-p01-integration; m0-p01-handoff | accepted-scope-entry | Not run; evidence absent |
| [M0-P02](phase-02-boot-image-and-interface-contracts.md) | M0-A03, M0-A04, M0-A05 | M0-T02, M0-T03, M0-T04 | m0-p02-decisions, m0-p02-fixtures; m0-p02-integration; m0-p02-handoff | m0-p01-handoff | Not run; evidence absent |
| [M0-P03](phase-03-acceptance-harness-and-input-qualification.md) | M0-A01, M0-A02, M0-A03, M0-A04, M0-A05, M0-A06, M0-A07 | M0-T01, M0-T02, M0-T03, M0-T04, M0-T05, M0-T06 | m0-p03-decisions, m0-p03-harness, m0-p03-qualify; m0-p03-integration; m0-p03-handoff | m0-p02-handoff | Not run; evidence absent |

The final phase reruns all M0 acceptance cases for milestone closure.
Earlier contract, fixture, model or hosted results remain partial where guest
integration is required. Scope exclusions and physical obligations in this
definition are unchanged. An acceptance reviewer must retain failure history,
record the accepted tested revision, and reopen gates on incompatible input
changes, missing required evidence or a violated invariant.

## Index

### Subdirectories

- None yet.

### Documents

- [Phase 1 — Target, toolchain, and build baseline](phase-01-target-toolchain-and-build-baseline.md) — Turn the selected Intel target into a versioned, reproducible development fixture and installed-unit record. This phase qualifies inputs and native link fixtures, not a user-mode OS.
- [Phase 2 — Boot, image, and interface contracts](phase-02-boot-image-and-interface-contracts.md) — Specify and exercise the handoff, native image, console/time, and initial authority contracts before the guest kernel implements them.
- [Phase 3 — Acceptance harness and input qualification](phase-03-acceptance-harness-and-input-qualification.md) — Deliver an exercised unattended acceptance harness and close the complete M0 input gate using real build and fixture evidence.

## Maintaining this index

Inventory each phase or supporting child document when created, and keep
artifact/test IDs, resolved decisions, evidence links, and the parent stream
consistent. Preserve this milestone's distinction between qualified inputs
and M1's working OS; do not check off delivery because this definition is
written. Do not renumber accepted artifact or test identities silently.
