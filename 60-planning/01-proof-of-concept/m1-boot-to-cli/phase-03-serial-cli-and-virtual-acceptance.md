---
title: "M1 Phase 3 — Serial CLI and virtual acceptance"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m1
  - proof-of-concept
aliases: []
---

# M1 Phase 3 — Serial CLI and virtual acceptance

Deliver the native user-mode atom prompt with real commands, bounded serial behavior,
advancing time, and the complete virtual M1 evidence bundle.

Back to milestone: [M1 definition and plan](README.md).

## Entry, scope, and dependencies

M1 Phase 2 protected images/entry, M0 pinned console/time contract, and reproducible driver.

Required predecessor: [M1 Phase 2](phase-02-protected-images-and-user-transitions.md), task `m1-p02-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M1-D03 is resolved by m1-p03-decisions: Select framing, line limit, overflow
resynchronization, timer source/units, interrupts/waits, and finite output behavior before
acceptance; the proposed 256-byte limit is not automatically selected. Until resolution,
downstream code and passing acceptance claims are blocked.

Kernel entry, protection, scheduling and bounded mechanisms are ring 0; CLI and ordinary
services are ring 3. Host tooling may build, emulate and capture but may not supply the
claimed guest kernel mechanisms.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M1-A03, M1-A04, M1-A05, M1-A06; its case coverage is M1-T01, M1-T02, M1-T03, M1-T04, M1-T05, M1-T06, M1-T07, M1-T08. Partial/model/hosted results do not close a case requiring later guest integration.

- [serial console and minimal cli](../../../20-notes/proof-of-concept-requirements/serial-console-and-minimal-cli.md) — contract and failure-case input for this phase.
- [time preemption and cpu budgets](../../../20-notes/proof-of-concept-requirements/time-preemption-and-cpu-budgets.md) — contract and failure-case input for this phase.
- [models fault injection and measurement](../../../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m1-p03-decisions | atom-os-research | Unassigned; resolve in m1-p03-decisions | m1-p02-handoff | M1-A03, M1-A04, M1-A05; phase cases below | Freeze CLI and timing limits output and verification; not run |
| m1-p03-io | unresolved-implementation | Unassigned; resolve in m1-p03-decisions | m1-p03-decisions | M1-A03, M1-A04; phase cases below | Implement serial and elapsed-time operations output and verification; not run |
| m1-p03-cli | unresolved-implementation | Unassigned; resolve in m1-p03-decisions | m1-p03-io | M1-A05, M1-A06; phase cases below | Implement the parser and three commands output and verification; not run |
| m1-p03-integration | unresolved-implementation | Unassigned test reviewer | m1-p03-cli | M1-T01, M1-T02, M1-T03, M1-T04, M1-T05, M1-T06, M1-T07, M1-T08 | Registered driver, raw positive/negative results; not run |
| m1-p03-handoff | atom-os-research | Unassigned acceptance reviewer | m1-p03-integration | M1-A03, M1-A04, M1-A05, M1-A06; M1-T01, M1-T02, M1-T03, M1-T04, M1-T05, M1-T06, M1-T07, M1-T08 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 3 Phase — Serial CLI and virtual acceptance.

  Deliver the native user-mode atom prompt with real commands, bounded serial behavior,
  advancing time, and the complete virtual M1 evidence bundle. Completion requires the
  assembled phase gate below, not just its component tasks.

  - [ ] 3.1 Section — Console and time mechanisms.

    Supply bounded kernel transport and timing that remain live while the user program waits.

    - [ ] 3.1.1 Task [id: m1-p03-decisions] [repo: atom-os-research] [after: m1-p02-handoff] — Freeze CLI and timing limits.

      Resolve M1-D03 and record observable targets before selecting passing runs.

      - [ ] 3.1.1.1 Subtask — Select transport and time policies.

        Compare supported timer/interrupt sources and polling/wait behavior under the pinned
        fixture. Record units, conversion, framing, buffer/line capacities, overflow, and
        halt/reset criteria.

    - [ ] 3.1.2 Task [id: m1-p03-io] [repo: unresolved-implementation] [after: m1-p03-decisions] — Implement serial and elapsed-time operations.

      Make console/time syscalls obey complete-buffer checks and bounded privileged work.

      - [ ] 3.1.2.1 Subtask — Handle readiness and backpressure.

        Implement bounded receive/transmit queues and wait/wakeup behavior. Timer progress
        must survive idle input, floods, full output queues, and lost-wakeup injection.

      - [ ] 3.1.2.2 Subtask — Expose honest elapsed time.

        Provide monotonic uptime in declared units and identify guest versus host
        measurements. Test conversion boundaries and progress across idle intervals without
        claiming CPU budget isolation.

  - [ ] 3.2 Section — Interactive delivery.

    Use the actual native CLI to expose only mechanisms that exist and qualify the assembled
    virtual system.

    - [ ] 3.2.1 Task [id: m1-p03-cli] [repo: unresolved-implementation] [after: m1-p03-io] — Implement the parser and three commands.

      Deliver M1-A05 without simulated service inspection or a privileged shell.

      - [ ] 3.2.1.1 Subtask — Build bounded command handling.

        Implement atom prompt, help, version, and uptime using real kernel/build identities.
        Bound editing, parsing, formatting, and memory usage.

      - [ ] 3.2.1.2 Subtask — Exercise input recovery.

        Specify and test CR/LF/CRLF, blanks, editing at empty input, control bytes, invalid
        arguments, exact-limit and oversized lines. An oversized prefix must not execute; the
        next valid command must work.

      - [ ] 3.2.1.3 Subtask — Register unattended guest acceptance.

        Adapt M0's runner to submit commands, verify CPL traces and canaries, and retain the
        boot image, symbols, transcripts, and negative-test outcomes from two clean builds.

  - [ ] 3.3 Section — Phase 3 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 3.3.1 Task [id: m1-p03-integration] [repo: unresolved-implementation] [after: m1-p03-cli] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 3.3.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Run every M1-T01–M1-T08 on the real serial guest. Require CPL
        3 CLI, correct help/version/uptime results, timer progress, protected memory, valid
        state preservation, and reproducible identities.

      - [ ] 3.3.1.2 Subtask — Exercise failures and inherited behavior.

        Combine malformed input, saturated serial, bad images, unsafe requests, deliberate CLI
        faults, and host timeout/early-death checks. Rerun M0 input validation; an unexpected
        reboot cannot pass as recovery. Retain actual observations and finite watchdog
        outcomes, not only intended commands.

    - [ ] 3.3.2 Task [id: m1-p03-handoff] [repo: atom-os-research] [after: m1-p03-integration] — Record evidence and decide phase handoff.

      Accept virtual M1 only with all eight cases passing. M2 may then proceed from this
      virtual gate; Phase 4 tracks physical qualification separately and remains open until
      performed.

      - [ ] 3.3.2.1 Subtask — Record reproducible execution evidence.

        Create a dated journal record linked to the task/artifact/case IDs, full tested commit
        and dirty state, host/guest or physical configuration, tools, commands, raw logs,
        hashes, sample counts and pass/fail/blocked/not-run results. Keep failures and hosted
        versus guest evidence distinct. Index attachments and link the record from this phase
        and milestone.

      - [ ] 3.3.2.2 Subtask — Review closure and update the milestone.

        An assigned reviewer checks every child and required gate against evidence and records
        proceed, revise or blocked. Preserve unresolved decisions, limits and reopening
        conditions. Distinguish plan/tested/merge revisions; do not infer tests on a later
        merge. Update checkboxes only for verified work, keep blocked tests open, and update
        the next phase's entry state without authorizing implementation or Git actions.
