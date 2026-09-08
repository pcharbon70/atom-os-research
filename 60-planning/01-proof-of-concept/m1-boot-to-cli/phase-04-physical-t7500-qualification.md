---
title: "M1 Phase 4 — Physical T7500 qualification"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m1
  - proof-of-concept
aliases: []
---

# M1 Phase 4 — Physical T7500 qualification

Repeat the single-CPU CLI qualification on the observed T7500 without confusing emulator
evidence with physical support.

Back to milestone: [M1 definition and plan](README.md).

## Entry, scope, and dependencies

M1 Phase 3 virtual acceptance plus M0 installed-unit inventory. This is a separate physical
branch, not an added dependency on SMP or a blocker to virtual M2 work.

Required predecessor: [M1 Phase 3](phase-03-serial-cli-and-virtual-acceptance.md), task `m1-p03-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M1-D04 is resolved by m1-p04-decisions: Select safe boot media, actual firmware path,
serial/debug transport, test boundaries, and explicit permission for any media or
persistent-device writes. Until resolution, downstream code and passing acceptance claims are
blocked.

Kernel entry, protection, scheduling and bounded mechanisms are ring 0; CLI and ordinary
services are ring 3. Host tooling may build, emulate and capture but may not supply the
claimed guest kernel mechanisms.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M1-A01, M1-A04, M1-A06; its case coverage is M1-T01, M1-T02, M1-T03, M1-T04, M1-T05, M1-T06, M1-T07, M1-T08. Partial/model/hosted results do not close a case requiring later guest integration.

- [dell precision t7500 target and minimal qemu profile](../../../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md) — contract and failure-case input for this phase.
- [target firmware and boot handoff](../../../20-notes/proof-of-concept-requirements/target-firmware-and-boot-handoff.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m1-p04-decisions | atom-os-research | Unassigned; resolve in m1-p04-decisions | m1-p03-handoff | M1-A01, M1-A04, M1-A06; phase cases below | Review the physical test procedure output and verification; not run |
| m1-p04-physical | unresolved-implementation | Unassigned; resolve in m1-p04-decisions | m1-p04-decisions | M1-A01, M1-A04, M1-A06; phase cases below | Execute and retain the hardware qualification output and verification; not run |
| m1-p04-integration | unresolved-implementation | Unassigned test reviewer | m1-p04-physical | M1-T01, M1-T02, M1-T03, M1-T04, M1-T05, M1-T06, M1-T07, M1-T08 | Registered driver, raw positive/negative results; not run |
| m1-p04-handoff | atom-os-research | Unassigned acceptance reviewer | m1-p04-integration | M1-A01, M1-A04, M1-A06; M1-T01, M1-T02, M1-T03, M1-T04, M1-T05, M1-T06, M1-T07, M1-T08 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 4 Phase — Physical T7500 qualification.

  Repeat the single-CPU CLI qualification on the observed T7500 without confusing emulator
  evidence with physical support. Completion requires the assembled phase gate below, not just
  its component tasks.

  - [ ] 4.1 Section — Physical execution envelope.

    Qualify the actual machine and a recoverable test procedure before running its kernel
    image.

    - [ ] 4.1.1 Task [id: m1-p04-decisions] [repo: atom-os-research] [after: m1-p03-handoff] — Review the physical test procedure.

      Resolve M1-D04 without treating the plan as permission to overwrite a disk or change
      firmware.

      - [ ] 4.1.1.1 Subtask — Match the installed inventory.

        Compare CPU/features, firmware, boot path, serial device and memory map against
        qualified virtual assumptions. Document necessary backend differences and requalify
        changed inputs.

      - [ ] 4.1.1.2 Subtask — Approve bounded lab actions.

        Record selected media and recovery steps, keep additional CPUs unstarted or safely
        parked, and obtain authority for any destructive or persistent operation before doing
        it. Missing access keeps the physical gate blocked.

    - [ ] 4.1.2 Task [id: m1-p04-physical] [repo: unresolved-implementation] [after: m1-p04-decisions] — Execute and retain the hardware qualification.

      Produce a physical M1-A06 supplement, with separate observations and limitations.

      - [ ] 4.1.2.1 Subtask — Run the applicable CLI and protection cases.

        Use the actual boot/debug path to repeat M1-T01–T08 acceptance obligations. Identify
        how physical traces demonstrate privilege, timer, and fault results; lack of an
        emulator injection facility does not silently waive an obligation.

      - [ ] 4.1.2.2 Subtask — Compare and isolate hardware failures.

        Record serial logs, maps, device/firmware identities, and discrepancies. Return
        kernel/backend changes to their owning phase and rerun virtual regressions before
        accepting them.

  - [ ] 4.2 Section — Phase 4 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 4.2.1 Task [id: m1-p04-integration] [repo: unresolved-implementation] [after: m1-p04-physical] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 4.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. On the identified T7500, demonstrate the native prompt,
        commands, time, privilege/protection, and reproducible boot under the selected
        physical procedure. Record each case's physical result independently.

      - [ ] 4.2.1.2 Subtask — Exercise failures and inherited behavior.

        Exercise safe malformed-input and fault paths plus recovery from an unsuccessful boot.
        Do not inject hazardous firmware or storage failures; if a required case lacks a safe
        method, keep it blocked for an explicit review decision. Retain actual observations
        and finite watchdog outcomes, not only intended commands.

    - [ ] 4.2.2 Task [id: m1-p04-handoff] [repo: atom-os-research] [after: m1-p04-integration] — Record evidence and decide phase handoff.

      Record physical qualification separately from virtual M1. Do not claim hardware support
      if access, safe methods, or required results remain absent; M2–M4 virtual results cannot
      close this gate.

      - [ ] 4.2.2.1 Subtask — Record reproducible execution evidence.

        Create a dated journal record linked to the task/artifact/case IDs, full tested commit
        and dirty state, host/guest or physical configuration, tools, commands, raw logs,
        hashes, sample counts and pass/fail/blocked/not-run results. Keep failures and hosted
        versus guest evidence distinct. Index attachments and link the record from this phase
        and milestone.

      - [ ] 4.2.2.2 Subtask — Review closure and update the milestone.

        An assigned reviewer checks every child and required gate against evidence and records
        proceed, revise or blocked. Preserve unresolved decisions, limits and reopening
        conditions. Distinguish plan/tested/merge revisions; do not infer tests on a later
        merge. Update checkboxes only for verified work, keep blocked tests open, and update
        the next phase's entry state without authorizing implementation or Git actions.
