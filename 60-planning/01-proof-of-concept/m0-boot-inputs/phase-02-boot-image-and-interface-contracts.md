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

M0 Phase 1 accepted virtual/build inputs; unresolved physical evidence is not a successful M0
exit.

Required predecessor: [M0 Phase 1](phase-01-target-toolchain-and-build-baseline.md), task `m0-p01-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M0-D02 is resolved by m0-p02-decisions: Choose loader/long-mode ownership, static
image subset, native calling and register-state policy, syscall mechanism, console framing,
clock units, and initial fault policy using bounded validation and T7500/fixture
compatibility. Until resolution, downstream code and passing acceptance claims are blocked.

The host owns build tools, validation fixtures, emulation and capture; M0 does not claim
kernel enforcement. Firmware/loader/kernel ownership is fixed in the contract.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
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

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m0-p02-decisions | atom-os-research | Unassigned; resolve in m0-p02-decisions | m0-p01-handoff | M0-A03, M0-A04, M0-A05; phase cases below | Freeze boot and native interface choices output and verification; not run |
| m0-p02-fixtures | unresolved-implementation | Unassigned; resolve in m0-p02-decisions | m0-p02-decisions | M0-A03, M0-A04, M0-A05; phase cases below | Implement contract validators and malformed fixtures output and verification; not run |
| m0-p02-integration | unresolved-implementation | Unassigned test reviewer | m0-p02-fixtures | M0-T02, M0-T03, M0-T04 | Registered driver, raw positive/negative results; not run |
| m0-p02-handoff | atom-os-research | Unassigned acceptance reviewer | m0-p02-integration | M0-A03, M0-A04, M0-A05; M0-T02, M0-T03, M0-T04 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 2 Phase — Boot, image, and interface contracts.

  Specify and exercise the handoff, native image, console/time, and initial authority
  contracts before the guest kernel implements them. Completion requires the assembled phase
  gate below, not just its component tasks.

  - [ ] 2.1 Section — Executable contracts.

    Agree ownership and failure rules, then make contradictions executable test failures.

    - [ ] 2.1.1 Task [id: m0-p02-decisions] [repo: atom-os-research] [after: m0-p01-handoff] — Freeze boot and native interface choices.

      Resolve M0-D02 before dependent image/startup code; preserve explicit host, loader,
      kernel, and user responsibilities.

      - [ ] 2.1.1.1 Subtask — Select the entry and image contracts.

        Compare loader support and entry guarantees; record reset-to-entry ownership,
        stack/register state, memory reservations, image segments/relocations, BSS,
        permissions, and enabled register policy.

      - [ ] 2.1.1.2 Subtask — Define bounded console/time authority.

        Record operation encodings, buffer limits, errors, waits, time conversion, and
        halt/reset behavior. Assign only required console/time grants; a trusted operator does
        not grant the CLI physical-memory access.

    - [ ] 2.1.2 Task [id: m0-p02-fixtures] [repo: unresolved-implementation] [after: m0-p02-decisions] — Implement contract validators and malformed fixtures.

      Deliver M0-A03/A04 executable checks and M0-A05 authority consistency evidence without
      claiming guest protection.

      - [ ] 2.1.2.1 Subtask — Normalize handoff and image fixtures.

        Create valid and malformed snapshots/segments covering truncation, arithmetic
        overflow, overlap, invalid entry points, unsupported features, and reserved memory.
        Verify failure publishes no runnable image descriptor.

      - [ ] 2.1.2.2 Subtask — Cross-check interface ownership.

        Check every exposed operation has rights, payer/bounds, expected errors, and enforcing
        owner. Link each requirement to a validator case; reconcile generated constants with
        fixture layouts.

      - [ ] 2.1.2.3 Subtask — Rebuild under the frozen contract.

        Repeat native fixture builds using accepted layout and state policies. Verify initial
        data, zero-fill descriptions, stack alignment, and reservation rules agree with the
        linked image.

  - [ ] 2.2 Section — Phase 2 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 2.2.1 Task [id: m0-p02-integration] [repo: unresolved-implementation] [after: m0-p02-fixtures] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 2.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Combine the loader handoff schema, native image validator,
        build fixtures, and authority table. Execute M0-T02/T03/T04 against valid inputs and
        preserve validator outputs.

      - [ ] 2.2.1.2 Subtask — Exercise failures and inherited behavior.

        Cross malformed records with conflicting reservations, invalid buffer bounds,
        unsupported state, and unauthorized operations. Reject contradictions without silently
        relaxing limits. Repeat Phase 1 binary/version checks. Retain actual observations and
        finite watchdog outcomes, not only intended commands.

    - [ ] 2.2.2 Task [id: m0-p02-handoff] [repo: atom-os-research] [after: m0-p02-integration] — Record evidence and decide phase handoff.

      Give Phase 3 a versioned contract bundle and validator cases. These checks precede M1
      guest enforcement and cannot prove ring-3 execution.

      - [ ] 2.2.2.1 Subtask — Record reproducible execution evidence.

        Create a dated journal record linked to the task/artifact/case IDs, full tested commit
        and dirty state, host/guest or physical configuration, tools, commands, raw logs,
        hashes, sample counts and pass/fail/blocked/not-run results. Keep failures and hosted
        versus guest evidence distinct. Index attachments and link the record from this phase
        and milestone.

      - [ ] 2.2.2.2 Subtask — Review closure and update the milestone.

        An assigned reviewer checks every child and required gate against evidence and records
        proceed, revise or blocked. Preserve unresolved decisions, limits and reopening
        conditions. Distinguish plan/tested/merge revisions; do not infer tests on a later
        merge. Update checkboxes only for verified work, keep blocked tests open, and update
        the next phase's entry state without authorizing implementation or Git actions.
