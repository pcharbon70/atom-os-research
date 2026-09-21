---
title: "M1 Phase 4 — Physical fixture qualification"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m1
  - proof-of-concept
aliases: []
---

# M1 Phase 4 — Physical fixture qualification

Qualify one observed physical fixture at a time by comparing an external
observation record with Kay OS runtime discovery and repeating applicable
single-CPU CLI checks without confusing emulator evidence with physical support.

Back to milestone: [M1 definition and plan](README.md).

## Entry, scope, and dependencies

M1 Phase 3 virtual acceptance. This phase collects its own just-in-time fixture
record; it has no M0 installed-unit dependency. It is a separate physical
branch, not an added dependency on SMP or a blocker to virtual M2 work.

Required predecessor: [M1 Phase 3](phase-03-serial-cli-and-virtual-acceptance.md), task `m1-p03-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M1-D04 is resolved by m1-p04-decisions: assign a fixture ID; select
safe observation, boot media, actual firmware path, serial/debug transport and
comparison boundaries; and obtain explicit permission for any persistent-device
write. Until resolution, downstream work and physical claims are blocked.

Kernel entry, protection, scheduling and bounded mechanisms are ring 0; CLI and ordinary
services are ring 3. Host tooling may build, emulate and capture but may not supply the
claimed guest kernel mechanisms.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 64 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full obligation
wording. This optional physical branch owns M1-P04-A01, M1-P04-A02,
M1-P04-T01 and M1-P04-T02. It may reuse applicable M1-T01–M1-T09 methods, but
virtual or hosted results do not close a physical-fixture claim.

- [x86-64 compatibility envelope and test fixtures](../../../20-notes/proof-of-concept-requirements/x86-64-compatibility-envelope-and-test-fixtures.md) — generic target, runtime-discovery and qualification-ladder input for this phase.
- [Dell Precision T7500 platform reference](../../../20-notes/proof-of-concept-requirements/dell-precision-t7500-platform-reference.md) — candidate P1 family context only; it is not an installed-unit record.
- [target firmware and boot handoff](../../../20-notes/proof-of-concept-requirements/target-firmware-and-boot-handoff.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m1-p04-decisions | atom-os-research | Unassigned; resolve in m1-p04-decisions | m1-p03-handoff | M1-P04-A01; phase cases below | Fixture identity, procedure, permissions and comparison contract; not run |
| m1-p04-inventory | kay-os plus private lab evidence | Lab operator and publication reviewer; resolve in m1-p04-decisions | m1-p04-decisions | M1-P04-A01, M1-P04-T02 | Just-in-time read-only external observation and reviewed public derivative; not run |
| m1-p04-physical | kay-os | Unassigned; resolve in m1-p04-decisions | m1-p04-inventory | M1-P04-A02, M1-P04-T01, M1-P04-T02 | Kay OS discovery report, comparison and applicable physical checks; not run |
| m1-p04-integration | kay-os | Unassigned test reviewer | m1-p04-physical | M1-P04-T01, M1-P04-T02 | Registered physical driver/checklist and raw results; not run |
| m1-p04-handoff | atom-os-research | Unassigned acceptance reviewer | m1-p04-integration | M1-P04-A01, M1-P04-A02, M1-P04-T01, M1-P04-T02 | Dated evidence and per-fixture support decision; not run |

## Planned work

- [ ] 4 Phase — Physical fixture qualification.

  Qualify one named fixture without confusing that result with generic x86-64
  or emulator support. Completion requires external observation, Kay OS
  discovery, comparison and applicable physical tests.

  - [ ] 4.1 Section — Physical execution envelope.

    Assign a fixture identity, qualify a recoverable procedure and collect
    just-in-time external observations before running the Kay OS image.

    - [ ] 4.1.1 Task [id: m1-p04-decisions] [repo: atom-os-research] [after: m1-p03-handoff] — Review the physical test procedure.

      Resolve M1-D04 without treating the plan as permission to overwrite a
      disk or change firmware, and without making the chosen machine the
      architecture definition.

      - [ ] 4.1.1.1 Subtask — Assign the fixture and comparison contract.

        Give the machine a stable fixture ID, record why it adds useful
        coverage, and define which external and Kay OS-discovered fields must
        agree. The T7500 may be P1 but is not automatically selected by this plan.

      - [ ] 4.1.1.2 Subtask — Approve bounded lab actions.

        Record selected media and recovery steps, keep additional CPUs unstarted or safely
        parked, and obtain authority for any destructive or persistent operation before doing
        it. Missing access keeps the physical gate blocked.

    - [ ] 4.1.2 Task [id: m1-p04-inventory] [repo: kay-os plus private lab evidence] [after: m1-p04-decisions] — Collect and review the external fixture record.

      Observe the machine immediately before its test using the versioned
      normal-user, read-only procedure. This record supports safety and
      comparison but is never an input consumed by Kay OS.

      - [ ] 4.1.2.1 Subtask — Capture and redact installed-unit facts.

        Record CPU identity/features/topology, memory, firmware, ACPI table
        identities, relevant PCI devices and console/debug access. Keep the raw
        record private and reject unique identifiers from the reviewed copy.

      - [ ] 4.1.2.2 Subtask — Preserve unknowns and approve publication.

        Do not fill unavailable facts from a product-family specification. A
        designated reviewer approves the allowlisted derivative and its raw
        hash before the boot image is exercised.

    - [ ] 4.1.3 Task [id: m1-p04-physical] [repo: kay-os] [after: m1-p04-inventory] — Execute and retain the hardware qualification.

      Produce the phase-scoped discovery, comparison and physical test records
      with separate observations and limitations.

      - [ ] 4.1.3.1 Subtask — Boot and retain Kay OS discovery.

        Boot the same accepted image without injecting external inventory
        values. Retain the bounded Kay OS CPU, memory, ACPI/APIC, console and
        timer discovery report, then compare it field by field with the external
        record and explain every discrepancy.

      - [ ] 4.1.3.2 Subtask — Run the applicable CLI and protection cases.

        Use the actual boot/debug path to repeat applicable M1 acceptance obligations. Identify
        how physical traces demonstrate privilege, timer, and fault results; lack of an
        emulator injection facility does not silently waive an obligation.

      - [ ] 4.1.3.3 Subtask — Isolate hardware-specific failures.

        Record serial logs, maps, device/firmware identities and discrepancies.
        Return generic kernel/backend changes to their owning phase and rerun
        virtual regressions before accepting them.

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
        limits before execution. On the named fixture, demonstrate the native
        prompt, commands, time, privilege/protection, reproducible boot and
        discovery comparison under the selected physical procedure. Record
        each physical result independently.

      - [ ] 4.2.1.2 Subtask — Exercise failures and inherited behavior.

        Exercise safe malformed-input and fault paths plus recovery from an unsuccessful boot.
        Do not inject hazardous firmware or storage failures; if a required case lacks a safe
        method, keep it blocked for an explicit review decision. Retain actual observations
        and finite watchdog outcomes, not only intended commands.

    - [ ] 4.2.2 Task [id: m1-p04-handoff] [repo: atom-os-research] [after: m1-p04-integration] — Record evidence and decide phase handoff.

      Record qualification separately for the named fixture. Do not generalize
      one pass to all x86-64 PCs or claim support if comparison, safe methods or
      required results remain absent; M2–M4 virtual results cannot close this gate.

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
