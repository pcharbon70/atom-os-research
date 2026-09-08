---
title: "M3 Phase 3 — Guest adapter and runtime accounting"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m3
  - proof-of-concept
aliases: []
---

# M3 Phase 3 — Guest adapter and runtime accounting

Replace host dependencies with the bounded guest substrate and finish runtime accounting
without blocking the sole actor scheduler on native work.

Back to milestone: [M3 definition and plan](README.md).

## Entry, scope, and dependencies

M3 Phase 2 interpreter/GC and accepted M2 guest substrate including independently funded
recovery.

Required predecessor: [M3 Phase 2](phase-02-actor-interpreter-and-tracing-gc.md), task `m3-p02-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M3-D03 is resolved by m3-p03-decisions: Bind M2 ABI/lifecycle versions, asynchronous
continuation/reply rules, capacities, mailbox overload semantics, complete global accounting
and responsiveness targets. Until resolution, downstream code and passing acceptance claims
are blocked.

The kernel enforces domain protection and backing; the interpreter, actors and tracing
collector remain ring 3. A hosted oracle supplies comparison results, not guest kernel
services.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M3-A05, M3-A06; its case coverage is M3-T02, M3-T03, M3-T04, M3-T05, M3-T07. Partial/model/hosted results do not close a case requiring later guest integration.

- [runtime adapter signals and native services](../../../20-notes/proof-of-concept-requirements/runtime-adapter-signals-and-native-services.md) — contract and failure-case input for this phase.
- [resource accounting and mailbox overload](../../../20-notes/proof-of-concept-requirements/resource-accounting-and-mailbox-overload.md) — contract and failure-case input for this phase.
- [capabilities syscalls and bounded ipc](../../../20-notes/proof-of-concept-requirements/capabilities-syscalls-and-bounded-ipc.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m3-p03-decisions | atom-os-research | Unassigned; resolve in m3-p03-decisions | m3-p02-handoff | M3-A05, M3-A06; phase cases below | Freeze adapter and overload contracts output and verification; not run |
| m3-p03-adapter | unresolved-implementation | Unassigned; resolve in m3-p03-decisions | m3-p03-decisions | M3-A05; phase cases below | Implement asynchronous native requests output and verification; not run |
| m3-p03-ledger | unresolved-implementation | Unassigned; resolve in m3-p03-decisions | m3-p03-adapter | M3-A06; phase cases below | Enforce full runtime resource ownership output and verification; not run |
| m3-p03-integration | unresolved-implementation | Unassigned test reviewer | m3-p03-ledger | M3-T02, M3-T03, M3-T04, M3-T05, M3-T07 | Registered driver, raw positive/negative results; not run |
| m3-p03-handoff | atom-os-research | Unassigned acceptance reviewer | m3-p03-integration | M3-A05, M3-A06; M3-T02, M3-T03, M3-T04, M3-T05, M3-T07 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 3 Phase — Guest adapter and runtime accounting.

  Replace host dependencies with the bounded guest substrate and finish runtime accounting
  without blocking the sole actor scheduler on native work. Completion requires the assembled
  phase gate below, not just its component tasks.

  - [ ] 3.1 Section — Guest boundary and accounting.

    Make every runtime resource and substrate operation explicit before declaring guest
    compatibility.

    - [ ] 3.1.1 Task [id: m3-p03-decisions] [repo: atom-os-research] [after: m3-p02-handoff] — Freeze adapter and overload contracts.

      Resolve M3-D03, including complete capacity categories and accepted-message failure
      semantics.

      - [ ] 3.1.1.1 Subtask — Audit imports and choose replacements.

        Enumerate direct and linked helper dependencies for allocation, clocks, waits,
        synchronization, entropy, static images, logging and termination. Map supported
        operations to M2; disable unsupported filesystems, sockets, host threads and dynamic
        libraries.

      - [ ] 3.1.1.2 Subtask — Set all runtime capacities.

        Account for heaps/workspace, mailbox/in-flight copies, binaries/sub-binaries, atoms,
        code/literals, actor records, aliases/monitors, timers, continuations and allocator
        slack. Define admission failure without silent loss of admitted local messages.

    - [ ] 3.1.2 Task [id: m3-p03-adapter] [repo: unresolved-implementation] [after: m3-p03-decisions] — Implement asynchronous native requests.

      Connect actor waits to bounded continuations, preserving unrelated actor and
      outer-domain progress.

      - [ ] 3.1.2.1 Subtask — Suspend only the waiting actor.

        Bind requests to actor/request/service generation and resume at a safe point. Stall
        the native peer while another actor allocates and advances a heartbeat.

      - [ ] 3.1.2.2 Subtask — Retire delivery authority exactly once.

        Exercise completion versus timeout/cancel/death races, duplicate and malformed
        replies, and old generations. Preserve indeterminate accepted effects rather than
        treating timeout as rollback.

    - [ ] 3.1.3 Task [id: m3-p03-ledger] [repo: unresolved-implementation] [after: m3-p03-adapter] — Enforce full runtime resource ownership.

      Make runtime-local and global ledgers reconcile with domain backing and preserve outer
      recovery capacity.

      - [ ] 3.1.3.1 Subtask — Charge before admission.

        Reserve copying, mailbox, continuation and error capacity before exposing work.
        Compare logical ownership with physical backing and fail without partial ownership.

      - [ ] 3.1.3.2 Subtask — Exercise tiny capacities.

        Exhaust heap, mailbox, global tables, timers and continuations while collecting and
        handling faults. Verify funded diagnostics, ledger conservation, explicit overload and
        independent recovery heartbeat.

  - [ ] 3.2 Section — Phase 3 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 3.2.1 Task [id: m3-p03-integration] [repo: unresolved-implementation] [after: m3-p03-ledger] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 3.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Run M3-T04/T05 and adapter/accounting portions of T02/T03/T07
        in the real guest. Require actor progress during a stalled native request, finite
        charged retention, complete import inventory and intact M2 reserves.

      - [ ] 3.2.1.2 Subtask — Exercise failures and inherited behavior.

        Race late replies, peer death and generation changes with GC and exhausted queues. No
        misdelivery, dangling root, silent admitted-message loss or scheduler-wide block is
        acceptable. Rerun Phase 1 loader and Phase 2 root/conformance cases plus M2 boundary
        tests. Retain actual observations and finite watchdog outcomes, not only intended
        commands.

    - [ ] 3.2.2 Task [id: m3-p03-handoff] [repo: atom-os-research] [after: m3-p03-integration] — Record evidence and decide phase handoff.

      Deliver the audited guest runtime to Phase 4 with all imports replaced or explicitly
      rejected and quota behavior pinned.

      - [ ] 3.2.2.1 Subtask — Record reproducible execution evidence.

        Create a dated journal record linked to the task/artifact/case IDs, full tested commit
        and dirty state, host/guest or physical configuration, tools, commands, raw logs,
        hashes, sample counts and pass/fail/blocked/not-run results. Keep failures and hosted
        versus guest evidence distinct. Index attachments and link the record from this phase
        and milestone.

      - [ ] 3.2.2.2 Subtask — Review closure and update the milestone.

        An assigned reviewer checks every child and required gate against evidence and records
        proceed, revise or blocked. Preserve unresolved decisions, limits and reopening
        conditions. Distinguish plan/tested/merge revisions; do not infer tests on a later
        merge. Update checkboxes only for verified work, keep blocked tests open, and update
        the next phase's entry state without authorizing implementation or Git actions.
