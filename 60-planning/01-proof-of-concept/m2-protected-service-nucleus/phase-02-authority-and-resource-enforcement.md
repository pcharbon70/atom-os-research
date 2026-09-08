---
title: "M2 Phase 2 — Authority and resource enforcement"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m2
  - proof-of-concept
aliases: []
---

# M2 Phase 2 — Authority and resource enforcement

Enforce domain authority, resource ownership, and CPU budgets in the real kernel while
protecting independent recovery capacity.

Back to milestone: [M2 definition and plan](README.md).

## Entry, scope, and dependencies

M2 Phase 1 executable contract and M1 protected CLI/entry/memory baseline.

Required predecessor: [M2 Phase 1](phase-01-object-contract-and-lifecycle-models.md), task `m2-p01-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M2-D02 is resolved by m2-p02-decisions: Select replenishment, priorities,
periods/budgets, kernel and interrupt charging, boundary-burst/overrun rules, account sizes
and recovery reserves before scheduler acceptance. Until resolution, downstream code and
passing acceptance claims are blocked.

Kernel entry, protection, scheduling and bounded mechanisms are ring 0; CLI and ordinary
services are ring 3. Host tooling may build, emulate and capture but may not supply the
claimed guest kernel mechanisms.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M2-A01, M2-A03; its case coverage is M2-T01, M2-T02, M2-T04, M2-T05. Partial/model/hosted results do not close a case requiring later guest integration.

- [capabilities syscalls and bounded ipc](../../../20-notes/proof-of-concept-requirements/capabilities-syscalls-and-bounded-ipc.md) — contract and failure-case input for this phase.
- [resource accounting and mailbox overload](../../../20-notes/proof-of-concept-requirements/resource-accounting-and-mailbox-overload.md) — contract and failure-case input for this phase.
- [time preemption and cpu budgets](../../../20-notes/proof-of-concept-requirements/time-preemption-and-cpu-budgets.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m2-p02-decisions | atom-os-research | Unassigned; resolve in m2-p02-decisions | m2-p01-handoff | M2-A01, M2-A03; phase cases below | Freeze accounting and scheduling rules output and verification; not run |
| m2-p02-authority | unresolved-implementation | Unassigned; resolve in m2-p02-decisions | m2-p02-decisions | M2-A03; phase cases below | Implement checked handles and memory accounts output and verification; not run |
| m2-p02-budgets | unresolved-implementation | Unassigned; resolve in m2-p02-decisions | m2-p02-authority | M2-A03; phase cases below | Implement preemption and charged execution output and verification; not run |
| m2-p02-integration | unresolved-implementation | Unassigned test reviewer | m2-p02-budgets | M2-T01, M2-T02, M2-T04, M2-T05 | Registered driver, raw positive/negative results; not run |
| m2-p02-handoff | atom-os-research | Unassigned acceptance reviewer | m2-p02-integration | M2-A01, M2-A03; M2-T01, M2-T02, M2-T04, M2-T05 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 2 Phase — Authority and resource enforcement.

  Enforce domain authority, resource ownership, and CPU budgets in the real kernel while
  protecting independent recovery capacity. Completion requires the assembled phase gate
  below, not just its component tasks.

  - [ ] 2.1 Section — Authority and backing.

    Ensure a handle denotes current authority and every admitted resource has physical backing
    and an accountable payer.

    - [ ] 2.1.1 Task [id: m2-p02-decisions] [repo: atom-os-research] [after: m2-p01-handoff] — Freeze accounting and scheduling rules.

      Resolve M2-D02 with measurable limits, bounded failure, and an independently funded
      control path.

      - [ ] 2.1.1.1 Subtask — Allocate the resource ledger.

        Enumerate pages, page tables, execution/capability slots, calls, timers, fault
        records, console and cleanup metadata. Separate attribution from backing and reserve
        diagnostic/replacement capacity outside child ownership.

      - [ ] 2.1.1.2 Subtask — Choose CPU accounting policy.

        Record period/budget/priority selection, ownership of syscall and interrupt work,
        overrun allowance and boundary bursts. Define measurement intervals without claiming a
        sliding-window guarantee from aligned periods.

    - [ ] 2.1.2 Task [id: m2-p02-authority] [repo: unresolved-implementation] [after: m2-p02-decisions] — Implement checked handles and memory accounts.

      Enforce admission using current rights and generations, not caller-supplied object
      identity.

      - [ ] 2.1.2.1 Subtask — Check every authority transition.

        Implement grants and revocation with bounded rights checks and current generations.
        Reject guesses, stale handles, unauthorized mappings and invalid buffers without
        changing unrelated state.

      - [ ] 2.1.2.2 Subtask — Reserve before publication.

        Charge complete construction/admission costs before exposing objects. Inject each
        allocation failure and verify no orphan ownership, partial publication, or access to
        recovery reserves.

  - [ ] 2.2 Section — Temporal enforcement.

    Keep CPU-hogging children from consuming the control domain's scheduling capacity.

    - [ ] 2.2.1 Task [id: m2-p02-budgets] [repo: unresolved-implementation] [after: m2-p02-authority] — Implement preemption and charged execution.

      Deliver kernel scheduling/accounting against the frozen policy and instrument its
      observable costs.

      - [ ] 2.2.1.1 Subtask — Enforce consumption and replenishment.

        Implement account exhaustion/replenishment and context attribution, including
        interrupts and bounded kernel work. Verify non-yielding code cannot evade the budget.

      - [ ] 2.2.1.2 Subtask — Measure progress under bursts.

        Exercise syscall/serial floods and replenishment-boundary bursts. Compare charged
        usage and declared overrun with timer and independent test-domain heartbeats; final
        recovery and CLI-load tests follow Phase 4.

  - [ ] 2.3 Section — Phase 2 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 2.3.1 Task [id: m2-p02-integration] [repo: unresolved-implementation] [after: m2-p02-budgets] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 2.3.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Run real kernel authority and account tests for
        M2-T01/T02/T04/T05, including per-category failure injection and measured CPU
        attribution. Record the portions needing transport/recovery as still open.

      - [ ] 2.3.1.2 Subtask — Exercise failures and inherited behavior.

        Use stale/ungranted handles, partial page constructions, full slots, non-yielding
        children and costly valid syscalls. Verify unchanged canaries, bounded error paths and
        preserved reserves; rerun M1 protection and CLI cases. Retain actual observations and
        finite watchdog outcomes, not only intended commands.

    - [ ] 2.3.2 Task [id: m2-p02-handoff] [repo: atom-os-research] [after: m2-p02-integration] — Record evidence and decide phase handoff.

      Pass protected domains, finite accounts, and measured budget behavior to Phase 3. Do not
      claim the running recovery service exists yet.

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
