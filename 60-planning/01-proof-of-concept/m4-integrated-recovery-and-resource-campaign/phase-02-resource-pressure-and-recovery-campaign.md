---
title: "M4 Phase 2 — Resource pressure and recovery campaign"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m4
  - proof-of-concept
aliases: []
---

# M4 Phase 2 — Resource pressure and recovery campaign

Demonstrate bounded retention, preserved recovery reserves, charged CPU behavior and
quiescence-safe repeated replacement under combined pressure.

Back to milestone: [M4 definition and plan](README.md).

## Entry, scope, and dependencies

M4 Phase 1 manifest/workload and accepted M2/M3 mechanism evidence; limits cannot be enlarged
silently.

Required predecessor: [M4 Phase 1](phase-01-campaign-baseline-and-fault-workload.md), task `m4-p01-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M4-D02 is resolved by m4-p02-decisions: Confirm every ledger category has a
sweep/failure case or explicit profile exclusion, and freeze cleanup/quarantine/wrap
escalation plus measurement acceptance before running the campaign. Until resolution,
downstream code and passing acceptance claims are blocked.

Kernel protection and accounting remain ring 0; CLI, outer recovery, runtime and native test
service are separate ring-3 domains. Actor failure inside one runtime is distinct from domain
failure.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M4-A03, M4-A04, M4-A05; its case coverage is M4-T02, M4-T03, M4-T04, M4-T05, M4-T06. Partial/model/hosted results do not close a case requiring later guest integration.

- [resource accounting and mailbox overload](../../../20-notes/proof-of-concept-requirements/resource-accounting-and-mailbox-overload.md) — contract and failure-case input for this phase.
- [time preemption and cpu budgets](../../../20-notes/proof-of-concept-requirements/time-preemption-and-cpu-budgets.md) — contract and failure-case input for this phase.
- [domain lifecycle and safe reclamation](../../../20-notes/proof-of-concept-requirements/domain-lifecycle-and-safe-reclamation.md) — contract and failure-case input for this phase.
- [private heaps and tracing garbage collection](../../../20-notes/proof-of-concept-requirements/private-heaps-and-tracing-garbage-collection.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m4-p02-decisions | atom-os-research | Unassigned; resolve in m4-p02-decisions | m4-p01-handoff | M4-A03, M4-A04; phase cases below | Freeze the pressure and reclamation matrix output and verification; not run |
| m4-p02-pressure | unresolved-implementation | Unassigned; resolve in m4-p02-decisions | m4-p02-decisions | M4-A03, M4-A05; phase cases below | Run combined memory and CPU campaigns output and verification; not run |
| m4-p02-restarts | unresolved-implementation | Unassigned; resolve in m4-p02-decisions | m4-p02-pressure | M4-A04, M4-A05; phase cases below | Run fixed-capacity replacement and stale-state tests output and verification; not run |
| m4-p02-integration | unresolved-implementation | Unassigned test reviewer | m4-p02-restarts | M4-T02, M4-T03, M4-T04, M4-T05, M4-T06 | Registered driver, raw positive/negative results; not run |
| m4-p02-handoff | atom-os-research | Unassigned acceptance reviewer | m4-p02-integration | M4-A03, M4-A04, M4-A05; M4-T02, M4-T03, M4-T04, M4-T05, M4-T06 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 2 Phase — Resource pressure and recovery campaign.

  Demonstrate bounded retention, preserved recovery reserves, charged CPU behavior and
  quiescence-safe repeated replacement under combined pressure. Completion requires the
  assembled phase gate below, not just its component tasks.

  - [ ] 2.1 Section — Pressure and responsiveness.

    Stress managed and native resource owners together without hiding global retention or
    borrowing recovery capacity.

    - [ ] 2.1.1 Task [id: m4-p02-decisions] [repo: atom-os-research] [after: m4-p01-handoff] — Freeze the pressure and reclamation matrix.

      Resolve M4-D02 and reconcile campaign categories with every kernel/runtime ledger.

      - [ ] 2.1.1.1 Subtask — Account for every applicable category.

        Map pages/mappings/slots/calls/timers/faults/buffers/cleanup metadata and all runtime
        heaps, copying space, mailboxes, in-flight messages, global tables, continuations and
        slack to finite sweeps. Unsupported categories need profile exclusion and rejection
        tests.

      - [ ] 2.1.1.2 Subtask — Fix reuse and escalation boundaries.

        Bind cleanup batches, local execution/reference/translation quiescence, zeroing,
        generation wrap, quarantine release and exhaustion actions to M2 contracts. Record
        stop conditions before long runs.

    - [ ] 2.1.2 Task [id: m4-p02-pressure] [repo: unresolved-implementation] [after: m4-p02-decisions] — Run combined memory and CPU campaigns.

      Deliver M4-A03 with raw resource and timing observations under reproducible pressure.

      - [ ] 2.1.2.1 Subtask — Sweep allocation and messaging.

        Vary live sets, transient allocations, mailbox backlog, collection workspace and
        global retention. Reachable roots must survive movement and fixed live sets reach
        bounded post-GC retention.

      - [ ] 2.1.2.2 Subtask — Exhaust resources during failure handling.

        Combine full calls/faults/queues with child failure and cleanup. Denied admissions
        must leave no partial authority or ownership; admitted local messages cannot silently
        disappear.

      - [ ] 2.1.2.3 Subtask — Measure charged execution and progress.

        Use non-yielding children, syscall/serial floods and allocation storms, including
        replenishment-boundary bursts. Compare actual consumption plus declared overrun,
        same-runtime delay and independently funded heartbeats with frozen limits.

  - [ ] 2.2 Section — Repeated reclamation.

    Prove restart uses recovered capacity rather than consuming a continually shrinking pool.

    - [ ] 2.2.1 Task [id: m4-p02-restarts] [repo: unresolved-implementation] [after: m4-p02-pressure] — Run fixed-capacity replacement and stale-state tests.

      Deliver M4-A04 using the selected repetition count and exact fault schedules.

      - [ ] 2.2.1.1 Subtask — Interrupt construction and teardown.

        Inject failures before publication and throughout close/cleanup, with
        delayed/duplicate replies, timer cancellation and peer death. Require one terminal
        result and bounded cleanup/quarantine behavior.

      - [ ] 2.2.1.2 Subtask — Force stale generations and wrap.

        Retain handles/readiness/timers across replacement and use a tiny-generation build to
        exercise wrap. Verify stale state cannot authorize new children and zeroing follows
        quiescence.

      - [ ] 2.2.1.3 Subtask — Reconcile capacity across the campaign.

        Record free/owned/reserved/quarantined totals after each restart and compare their sum
        with fixed backing. Ever-growing allocations or quarantine accumulation fail the run.

  - [ ] 2.3 Section — Phase 2 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 2.3.1 Task [id: m4-p02-integration] [repo: unresolved-implementation] [after: m4-p02-restarts] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 2.3.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Execute M4-T02–M4-T06 across the frozen combined sweeps and
        restart campaign. Require unchanged isolation, predeclared responsiveness, finite
        retention, funded errors/recovery and conserved capacity.

      - [ ] 2.3.1.2 Subtask — Exercise failures and inherited behavior.

        Run simultaneous GC/mailbox/call/fault pressure, non-yielding children and interrupted
        cleanup with stale authority. Reproduce known model counterexamples as regressions,
        rerun Phase 1 fault/normal cases and the admitted M3 corpus. Retain actual
        observations and finite watchdog outcomes, not only intended commands.

    - [ ] 2.3.2 Task [id: m4-p02-handoff] [repo: atom-os-research] [after: m4-p02-integration] — Record evidence and decide phase handoff.

      Pass complete pressure/reclamation evidence to Phase 3 only when all required cases
      pass. Violated limits, lost samples, stale effects or unexplained ledger drift require
      correction or explicit scope review, not a retrospective pass.

      - [ ] 2.3.2.1 Subtask — Record reproducible execution evidence.

        Create a dated journal record linked to the task/artifact/case IDs, full tested commit
        and dirty state, host/guest or physical configuration, tools, commands, raw logs,
        hashes, sample counts and pass/fail/blocked/not-run results. Keep failures and hosted
        versus guest evidence distinct. Index attachments and link the record from this phase
        and milestone.

      - [ ] 2.3.2.2 Subtask — Review closure and update the milestone.

        An assigned reviewer checks every child and required gate against evidence and records
        proceed, revise or blocked. Preserve unresolved decisions, limits and reopening
        conditions. Distinguish plan/tested/merge revisions; do not infer tests on a later
        merge. Update checkboxes only for verified work, keep blocked tests open, and update
        the next phase's entry state without authorizing implementation or Git actions.
