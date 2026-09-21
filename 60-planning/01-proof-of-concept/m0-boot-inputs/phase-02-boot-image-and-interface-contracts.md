---
title: "M0 Phase 2 — Boot, image, and interface contracts"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m0
  - proof-of-concept
aliases: []
---

# M0 Phase 2 — Boot, image, and interface contracts

Specify and exercise the handoff, native image, console/time, and initial authority contracts
before the guest kernel implements them.

Back to milestone: [M0 definition and plan](README.md).

## Entry, scope, and dependencies

M0 Phase 1 accepted its virtual/build inputs on 2026-09-18; unresolved physical
evidence is not a successful M0 exit.

Required predecessor: [M0 Phase 1](phase-01-target-toolchain-and-build-baseline.md), task `m0-p01-handoff`.

Plan state: complete. Section 2.1 decisions and executable contract work are
implemented in the selected public [Kay OS repository](https://github.com/pcharbon70/kay-os).
Clean commit `f85571e2f2bb036c258fd596552731422cb41b38` passed all 24
registered cases on 2026-09-18, and independent follow-up review found no
remaining implementation blocker. The [execution record](../../../50-journal/2026-09-18-m0-phase-02-contract-integration.md)
retains exact identities and limitations. The user/project owner accepted the
handoff with a **proceed** decision on 2026-09-19.

Decision M0-D02 was resolved by the user on 2026-09-18. Limine v12.9.0 owns the
BIOS-to-long-mode path; Kay validates and copies a bounded handoff. The selected
native image is a fixed higher-half static ELF64 `ET_EXEC` with a narrow load
subset and no relocations. Native calls use a restricted integer-only System V
AMD64 profile without red zone or FP/SIMD state. The later user transition uses
a dedicated DPL3 interrupt gate, TSS kernel stack and `iretq`. Console transfers
are copy-based byte streams capped at 256 bytes with separate endpoint grants;
time is checked `u64` monotonic nanoseconds with absolute waits and separate
read/wait grants. Fatal faults emit a bounded emergency serial record then halt.
Boot media is a deterministic read-only BIOS ISO. These selections do not claim
guest enforcement.

## Accepted decision record

| Contract area | Accepted selection | Implementation record |
| --- | --- | --- |
| Loader and supply chain | Limine v12.9.0, protocol base revision 6; exact archive/signature hashes, signing-key fingerprint and protocol-header revision/hash | `config/m0/phase-02-contracts.json`, `src/m0/limine.zig`, `scripts/m0/verify-limine-release.sh` in Kay OS |
| Boot ownership | Limine establishes long mode; Kay bounds, validates and copies its normalized snapshot; no borrowed pointers survive | `src/m0/contracts.zig` boot-snapshot cases |
| Native image | Higher-half static ELF64 `ET_EXEC`; maximum eight page-aligned segments; no dynamic linking, relocations or write-execute mapping | `linker/x86_64-m0-higher-half.ld` and ELF audit driver |
| Native/user entry | Restricted integer-only System V AMD64, no red zone/FP/SIMD; later DPL3 interrupt gate with TSS stack and `iretq` | Build contract now; ring-3 mechanism explicitly deferred to M1 |
| Console and time | Copy-based 1–256 byte stream with separate read/write grants; checked monotonic `u64` nanoseconds and absolute waits with separate grants | Authority and conversion cases in `src/m0/contracts.zig` |
| Fatal failure | Bounded emergency serial record then stable halt | Policy selected; guest path remains unimplemented |
| Media | Deterministic read-only BIOS ISO | `scripts/m0/build-boot-image.sh`; clean two-build match at `f85571e` on 2026-09-18 |

The host owns build tools, validation fixtures, emulation and capture; M0 does not claim
kernel enforcement. Firmware/loader/kernel ownership is fixed in the contract.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 64 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M0-A03, M0-A04, M0-A05; its case coverage is M0-T02, M0-T03, M0-T04. Partial/model/hosted results do not close a case requiring later guest integration.

- [target firmware and boot handoff](../../../20-notes/proof-of-concept-requirements/target-firmware-and-boot-handoff.md) — contract and failure-case input for this phase.
- [freestanding build and static images](../../../20-notes/proof-of-concept-requirements/freestanding-build-and-static-images.md) — contract and failure-case input for this phase.
- [serial console and minimal cli](../../../20-notes/proof-of-concept-requirements/serial-console-and-minimal-cli.md) — contract and failure-case input for this phase.
- [time preemption and cpu budgets](../../../20-notes/proof-of-concept-requirements/time-preemption-and-cpu-budgets.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.
The clean Phase 2 [execution record](../../../50-journal/2026-09-18-m0-phase-02-contract-integration.md)
and [retained transcript](../../../assets/m0-phase-02-contract-integration/raw-transcript.txt)
distinguish hosted contract/image evidence from unrun guest and physical work.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m0-p02-decisions | atom-os-research | Codex implementation agent; user decision owner | m0-p01-handoff | M0-A03, M0-A04, M0-A05; phase cases below | Accepted selections above and Kay OS machine-readable record; complete 2026-09-18 |
| m0-p02-fixtures | kay-os | Codex implementation agent | m0-p02-decisions | M0-A03, M0-A04, M0-A05; phase cases below | Complete at clean implementation commit `f85571e`; independent follow-up review found no blocker; [evidence](../../../50-journal/2026-09-18-m0-phase-02-contract-integration.md) |
| m0-p02-integration | kay-os | Codex execution agent; independent review agent | m0-p02-fixtures | M0-T02, M0-T03, M0-T04 | Complete for declared pre-boot scope: 24/24 registered cases passed clean at `f85571e`; guest/ring-3/physical fixtures explicitly not tested; [evidence](../../../50-journal/2026-09-18-m0-phase-02-contract-integration.md) |
| m0-p02-handoff | atom-os-research | User acceptance reviewer | m0-p02-integration | M0-A03, M0-A04, M0-A05; M0-T02, M0-T03, M0-T04 | Complete: evidence retained and user/project owner selected proceed on 2026-09-19 |

## Planned work

- [x] 2 Phase — Boot, image, and interface contracts.

  Specify and exercise the handoff, native image, console/time, and initial authority
  contracts before the guest kernel implements them. Completion requires the assembled phase
  gate below, not just its component tasks.

  - [x] 2.1 Section — Executable contracts.

    Agree ownership and failure rules, then make contradictions executable test failures.

    - [x] 2.1.1 Task [id: m0-p02-decisions] [repo: atom-os-research] [after: m0-p01-handoff] — Freeze boot and native interface choices.

      Resolve M0-D02 before dependent image/startup code; preserve explicit host, loader,
      kernel, and user responsibilities.

      - [x] 2.1.1.1 Subtask — Select the entry and image contracts.

        Compare loader support and entry guarantees; record reset-to-entry ownership,
        stack/register state, memory reservations, image segments/relocations, BSS,
        permissions, and enabled register policy.

      - [x] 2.1.1.2 Subtask — Define bounded console/time authority.

        Record operation encodings, buffer limits, errors, waits, time conversion, and
        halt/reset behavior. Assign only required console/time grants; a trusted operator does
        not grant the CLI physical-memory access.

    - [x] 2.1.2 Task [id: m0-p02-fixtures] [repo: kay-os] [after: m0-p02-decisions] — Implement contract validators and malformed fixtures.

      Deliver M0-A03/A04 executable checks and M0-A05 authority consistency evidence without
      claiming guest protection.

      - [x] 2.1.2.1 Subtask — Normalize handoff and image fixtures.

        Create valid and malformed snapshots/segments covering truncation, arithmetic
        overflow, overlap, invalid entry points, unsupported features, and reserved memory.
        Verify failure publishes no runnable image descriptor.

      - [x] 2.1.2.2 Subtask — Cross-check interface ownership.

        Check every exposed operation has rights, payer/bounds, expected errors, and enforcing
        owner. Link each requirement to a validator case; reconcile generated constants with
        fixture layouts.

      - [x] 2.1.2.3 Subtask — Rebuild under the frozen contract.

        Repeat native fixture builds using accepted layout and state policies. Verify initial
        data, zero-fill descriptions, stack alignment, and reservation rules agree with the
        linked image.

  - [x] 2.2 Section — Phase 2 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [x] 2.2.1 Task [id: m0-p02-integration] [repo: kay-os] [after: m0-p02-fixtures] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [x] 2.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Combine the loader handoff schema, native image validator,
        build fixtures, and authority table. Execute M0-T02/T03/T04 against valid inputs and
        preserve validator outputs.

      - [x] 2.2.1.2 Subtask — Exercise failures and inherited behavior.

        Cross malformed records with conflicting reservations, invalid buffer bounds,
        unsupported state, and unauthorized operations. Reject contradictions without silently
        relaxing limits. Repeat Phase 1 binary/version checks. Retain actual observations and
        finite watchdog outcomes, not only intended commands.

    - [x] 2.2.2 Task [id: m0-p02-handoff] [repo: atom-os-research] [after: m0-p02-integration] — Record evidence and decide phase handoff.

      Give Phase 3 a versioned contract bundle and validator cases. These checks precede M1
      guest enforcement and cannot prove ring-3 execution.

      - [x] 2.2.2.1 Subtask — Record reproducible execution evidence.

        Create a dated journal record linked to the task/artifact/case IDs, full tested commit
        and dirty state, host/guest or physical configuration, tools, commands, raw logs,
        hashes, sample counts and pass/fail/blocked/not-run results. Keep failures and hosted
        versus guest evidence distinct. Index attachments and link the record from this phase
        and milestone.

      - [x] 2.2.2.2 Subtask — Review closure and update the milestone.

        An assigned reviewer checks every child and required gate against evidence and records
        proceed, revise or blocked. Preserve unresolved decisions, limits and reopening
        conditions. Distinguish plan/tested/merge revisions; do not infer tests on a later
        merge. Update checkboxes only for verified work, keep blocked tests open, and update
        the next phase's entry state without authorizing implementation or Git actions.
