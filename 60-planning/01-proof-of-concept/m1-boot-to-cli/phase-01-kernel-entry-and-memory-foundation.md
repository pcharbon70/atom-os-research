---
title: "M1 Phase 1 — Kernel entry and memory foundation"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m1
  - proof-of-concept
aliases: []
---

# M1 Phase 1 — Kernel entry and memory foundation

Bring up the real ring-0 kernel and validated boot-memory state on the M0 fixture, with
bounded diagnostics and no host OS inside the guest.

Back to milestone: [M1 definition and plan](README.md).

## Entry, scope, and dependencies

M0 qualified virtual/build/contracts and exercised watchdog; provisional experiments cannot be
accepted M1 evidence.

Required predecessor: [M0 Phase 3](../m0-boot-inputs/phase-03-acceptance-harness-and-input-qualification.md), task `m0-p03-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M1-D01 is resolved by m1-p01-decisions: Reconcile M0 entry/feature/register policies
with the implementation; assign exception-stack and reserved-memory ownership before admitting
any user image. Until resolution, downstream code and passing acceptance claims are blocked.

Kernel entry, protection, scheduling and bounded mechanisms are ring 0; CLI and ordinary
services are ring 3. Host tooling may build, emulate and capture but may not supply the
claimed guest kernel mechanisms.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M1-A01, M1-A06; its case coverage is M1-T06, M1-T07, M1-T08. Partial/model/hosted results do not close a case requiring later guest integration.

- [target firmware and boot handoff](../../../20-notes/proof-of-concept-requirements/target-firmware-and-boot-handoff.md) — contract and failure-case input for this phase.
- [privilege entry memory and user return](../../../20-notes/proof-of-concept-requirements/privilege-entry-memory-and-user-return.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m1-p01-decisions | atom-os-research | Unassigned; resolve in m1-p01-decisions | m0-p03-handoff | M1-A01; phase cases below | Bind the exact M0 execution contract output and verification; not run |
| m1-p01-memory | unresolved-implementation | Unassigned; resolve in m1-p01-decisions | m1-p01-decisions | M1-A01, M1-A06; phase cases below | Implement boot parsing and memory reservation output and verification; not run |
| m1-p01-integration | unresolved-implementation | Unassigned test reviewer | m1-p01-memory | M1-T06, M1-T07, M1-T08 | Registered driver, raw positive/negative results; not run |
| m1-p01-handoff | atom-os-research | Unassigned acceptance reviewer | m1-p01-integration | M1-A01, M1-A06; M1-T06, M1-T07, M1-T08 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 1 Phase — Kernel entry and memory foundation.

  Bring up the real ring-0 kernel and validated boot-memory state on the M0 fixture, with
  bounded diagnostics and no host OS inside the guest. Completion requires the assembled phase
  gate below, not just its component tasks.

  - [ ] 1.1 Section — Controlled kernel startup.

    Replace contract-only fixtures with kernel-owned entry state and conservative
    physical-memory initialization.

    - [ ] 1.1.1 Task [id: m1-p01-decisions] [repo: atom-os-research] [after: m0-p03-handoff] — Bind the exact M0 execution contract.

      Resolve M1-D01 by accepting the tested predecessor revision and resolving
      implementation-specific entry ownership.

      - [ ] 1.1.1.1 Subtask — Audit startup assumptions.

        Check loader guarantees against CPU feature checks, descriptors, stacks, interrupt
        state, and preserved register components. Return incompatible assumptions to M0 rather
        than silently choosing a different ABI.

      - [ ] 1.1.1.2 Subtask — Wire bounded diagnostic failure.

        Select identifiable startup milestones and finite fault halt/reset reporting under the
        host watchdog; a repeated reboot must not be interpreted as success.

    - [ ] 1.1.2 Task [id: m1-p01-memory] [repo: unresolved-implementation] [after: m1-p01-decisions] — Implement boot parsing and memory reservation.

      Deliver kernel entry and normalized usable/reserved memory with inspectable ownership.

      - [ ] 1.1.2.1 Subtask — Initialize trusted entry state.

        Install the selected descriptor/exception setup and capture a bounded handoff
        snapshot. Validate required tables and image lifetimes before using their memory.

      - [ ] 1.1.2.2 Subtask — Construct conservative memory ownership.

        Reserve kernel, boot images, firmware, page tables, stacks, and devices; reject
        overflow/overlap or unknown regions. Check allocator totals against the normalized
        snapshot.

      - [ ] 1.1.2.3 Subtask — Exercise corrupted boot inputs.

        Feed malformed handoffs and forced initialization failure through a test boot. Confirm
        bounded diagnostics and no continued execution on ambiguous memory.

  - [ ] 1.2 Section — Phase 1 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 1.2.1 Task [id: m1-p01-integration] [repo: unresolved-implementation] [after: m1-p01-memory] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 1.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Boot the actual kernel using M0's driver and correlate serial
        startup markers with debugger state and memory ledgers. Run the startup portions of
        M1-T06/T07/T08; these are not yet full CLI acceptance.

      - [ ] 1.2.1.2 Subtask — Exercise failures and inherited behavior.

        Truncate/overlap reservations and remove required features. Confirm safe failure and
        watchdog detection; repeat M0 build/version/handoff checks so a fixture change cannot
        mask a kernel defect. Retain actual observations and finite watchdog outcomes, not
        only intended commands.

    - [ ] 1.2.2 Task [id: m1-p01-handoff] [repo: atom-os-research] [after: m1-p01-integration] — Record evidence and decide phase handoff.

      Pass a reproducible kernel-entry and memory baseline to Phase 2. Do not close M1-T01
      merely because a ring-0 banner appears.

      - [ ] 1.2.2.1 Subtask — Record reproducible execution evidence.

        Create a dated journal record linked to the task/artifact/case IDs, full tested commit
        and dirty state, host/guest or physical configuration, tools, commands, raw logs,
        hashes, sample counts and pass/fail/blocked/not-run results. Keep failures and hosted
        versus guest evidence distinct. Index attachments and link the record from this phase
        and milestone.

      - [ ] 1.2.2.2 Subtask — Review closure and update the milestone.

        An assigned reviewer checks every child and required gate against evidence and records
        proceed, revise or blocked. Preserve unresolved decisions, limits and reopening
        conditions. Distinguish plan/tested/merge revisions; do not infer tests on a later
        merge. Update checkboxes only for verified work, keep blocked tests open, and update
        the next phase's entry state without authorizing implementation or Git actions.
