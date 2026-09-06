---
title: "Proof-of-Concept Implementation Planning"
kind: map
created: "2026-09-06"
tags:
  - archive-navigation
  - directory-index
  - implementation-planning
  - proof-of-concept
aliases:
  - "CLI-first OS planning stream"
---

# Proof-of-Concept Implementation Planning (`01-proof-of-concept`)

## Purpose

Translate the existing M0–M4 proof-of-concept roadmap into milestone-scoped
phased implementation plans. The first delivery is a bootable native user-mode
CLI; the completed PoC also demonstrates the required compiled-BEAM profile,
unprivileged process-local tracing GC, protected services, and recovery.

## What belongs here

- A subdirectory named for each milestone when its phases are actually written.
- Milestone READMEs describing scope, entry decisions, dependencies, ordered
  phases, and exit evidence.
- Phase notes using the described four-level work hierarchy and ending in
  integration tests, with links back to research and forward to evidence.

Graphical UI, desktop work, an AtomVM implementation path, and unrequested
implementation-repository scaffolding are excluded. Networking, writable
storage, SMP/NUMA, and a second ISA are later capability programs rather than
implicit requirements for the first CLI.

## Current planning state

The planning convention and this stream index are established. No milestone
directory or detailed phase plan has been authored yet. All M0–M4 evidence
gates remain open in the governing inquiry; this index closes none of them.
It neither selects the implementation language or bootloader nor initiates
implementation.

## Authoritative inputs

- [Readiness assessment](../../20-notes/proof-of-concept-research-readiness.md) —
  defines the M0–M4 outcomes, first CLI delivery, and limits of the PoC claim.
- [Minimal bootable-system inquiry](../../40-inquiries/can-a-minimal-bootable-system-validate-the-architecture.md) —
  tracks open acceptance gates and demonstrated evidence.
- [Dell Precision T7500 target and minimal QEMU profile](../../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md) —
  controls the Intel Xeon / Intel 64 target and minimum virtual fixture.
- [Requirement studies](../../20-notes/proof-of-concept-requirements/README.md) —
  supplies proposed contracts, failure cases, and remaining experiments.
- [Proof-of-concept map](../../10-maps/proof-of-concept.md) —
  connects the implementation questions to broader layer research.
- [Planning convention](../README.md) — controls directory naming, descriptions,
  phase-ending integration tests, evidence, and plan review.

## Milestone roadmap and intended directories

The directory names below are reserved naming proposals, not links to existing
plans. Phase count and task decomposition remain to be decided for each one.

| Milestone | Intended subdirectory | Required outcome | Planning dependency |
| --- | --- | --- | --- |
| M0 — Boot inputs | `m0-boot-inputs/` | Pinned build/target/firmware inputs, static CLI image contract, console/time ABI, limits, and automated check definitions/harness. | Existing target decision and research; remaining choices must be resolved explicitly. |
| M1 — Boot to CLI | `m1-boot-to-cli/` | Atom kernel launches a native user-mode CLI; `help`, `version`, `uptime`, bounded input, invalid commands, and timer progress pass. | M0 contracts and reproducible fixture. |
| M2 — Protected service nucleus | `m2-protected-service-nucleus/` | Protected domains, capabilities, accounts, bounded transport, fault delivery, independent recovery, and real CLI inspection/control. | M1 plus concrete lifecycle, authority, and budget contracts. |
| M3 — Project BEAM runtime | `m3-project-beam-runtime/` | CLI-launched compiler-produced BEAM in the unprivileged project runtime; pinned-profile conformance and automatic local tracing GC. | M2 substrate for guest integration; hosted profile experiments may run earlier when requested. |
| M4 — Integrated recovery and resource campaign | `m4-integrated-recovery-and-resource-campaign/` | Integrated CLI/actor/service/runtime failures, resource limits, reclamation, generation safety, and repeated recovery evidence. | Integrated M2 and M3 with predeclared test budgets and observables. |

M1 is the first delivery, not completion of the BEAM-capable PoC. The milestone
exit criteria remain those in the readiness assessment; writing plans must not
silently weaken them.

## Next decomposition work

First author the M0 plan and resolve its decision dependencies. Then develop
M1 against those contracts, retaining only a coarse dependency outline for
M2–M4 until their inputs support useful detail. It is possible to draft M1
conditionally while M0 is open, but not to present conditional choices as
accepted implementation facts.

The next planning pass should turn these open choices into bounded decision
tasks rather than require another broad research cycle:

- Implementation language, freestanding toolchain, linker, reproducible build
  environment, and implementation-repository location.
- Bootloader/handoff, static kernel and user image format, startup memory map,
  and pinned QEMU machine/firmware versions.
- Minimum user/kernel console and time ABI, privilege transition, exception
  handling, interrupt/timer strategy, and initial context-switch requirements.
- Serial test harness, success/failure criteria, resource bounds, and evidence
  artifacts for the first native CLI boot.
- Installed T7500 inventory and the safety/readiness criteria for a later
  physical single-CPU check. Hardware qualification remains distinct from the
  minimal virtual fixture; q35 is not a motherboard replica.

Select and close the exact BEAM workload and compatibility profile before
detailed M3 commitments; that work does not block drafting M0 or M1. Retain
the selected Intel target and start virtual tests small: one CPU, 128 MiB,
serial I/O, with the full fixture controlled by the linked target profile.
Do not enlarge QEMU topology simply because the lab machine has two packages.

## Stream completion and evidence

Each phase must end with integration tests and a truthful handoff decision.
Physical single-CPU CLI qualification can follow virtual M1 without waiting
for SMP. Do not claim physical qualification from a virtual test, or hosted
runtime conformance as guest M3 evidence.

Close the stream only when the declared M0–M4 acceptance evidence exists and
the governing inquiry records the outcome. Planning completeness, document
counts, and a privileged boot banner are not substitutes for that evidence.

## Index

### Subdirectories

- None yet; milestone directories will be created with their substantive plans.

### Documents

- None yet.

## Maintaining this index

When a milestone is decomposed, create its README and phase notes together,
replace its proposed path above with a relative README link, and inventory it
under Subdirectories. Update dependencies and planning/execution state without
implying completion. Keep this stream, the readiness assessment, inquiry,
proof-of-concept map, and journal evidence consistent when scope or acceptance
changes. Do not renumber delivered milestones or phases.
