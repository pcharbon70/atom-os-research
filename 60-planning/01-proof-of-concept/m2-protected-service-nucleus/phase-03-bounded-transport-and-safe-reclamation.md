---
title: "M2 Phase 3 — Bounded transport and safe reclamation"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m2
  - proof-of-concept
aliases: []
---

# M2 Phase 3 — Bounded transport and safe reclamation

Join funded request/completion handling to close, stop, quiescence, and safe resource reuse in
the guest.

Back to milestone: [M2 definition and plan](README.md).

## Entry, scope, and dependencies

M2 Phase 2 authority/accounts and Phase 1 lifecycle models.

Required predecessor: [M2 Phase 2](phase-02-authority-and-resource-enforcement.md), task `m2-p02-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M2-D03 is resolved by m2-p03-decisions: Select cleanup batch bounds, local
translation/reference quiescence checks, generation-wrap and quarantine release/exhaustion
rules, and terminal request semantics before allowing replacement. Until resolution,
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

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M2-A02, M2-A04, M2-A05; its case coverage is M2-T01, M2-T03, M2-T04, M2-T06. Partial/model/hosted results do not close a case requiring later guest integration.

- [capabilities syscalls and bounded ipc](../../../20-notes/proof-of-concept-requirements/capabilities-syscalls-and-bounded-ipc.md) — contract and failure-case input for this phase.
- [domain lifecycle and safe reclamation](../../../20-notes/proof-of-concept-requirements/domain-lifecycle-and-safe-reclamation.md) — contract and failure-case input for this phase.
- [runtime adapter signals and native services](../../../20-notes/proof-of-concept-requirements/runtime-adapter-signals-and-native-services.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m2-p03-decisions | atom-os-research | Unassigned; resolve in m2-p03-decisions | m2-p02-handoff | M2-A02, M2-A04, M2-A05; phase cases below | Freeze completion and reclamation rules output and verification; not run |
| m2-p03-transport | unresolved-implementation | Unassigned; resolve in m2-p03-decisions | m2-p03-decisions | M2-A04; phase cases below | Implement bounded server-funded requests output and verification; not run |
| m2-p03-reclaim | unresolved-implementation | Unassigned; resolve in m2-p03-decisions | m2-p03-transport | M2-A02, M2-A05; phase cases below | Implement stop, quiescence, and safe reuse output and verification; not run |
| m2-p03-integration | unresolved-implementation | Unassigned test reviewer | m2-p03-reclaim | M2-T01, M2-T03, M2-T04, M2-T06 | Registered driver, raw positive/negative results; not run |
| m2-p03-handoff | atom-os-research | Unassigned acceptance reviewer | m2-p03-integration | M2-A02, M2-A04, M2-A05; M2-T01, M2-T03, M2-T04, M2-T06 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 3 Phase — Bounded transport and safe reclamation.

  Join funded request/completion handling to close, stop, quiescence, and safe resource reuse
  in the guest. Completion requires the assembled phase gate below, not just its component
  tasks.

  - [ ] 3.1 Section — Transport lifecycle.

    Reserve enough capacity to finish every accepted request and retire its delivery authority
    exactly once.

    - [ ] 3.1.1 Task [id: m2-p03-decisions] [repo: atom-os-research] [after: m2-p02-handoff] — Freeze completion and reclamation rules.

      Resolve M2-D03 and cross-check it against the executable lifecycle model.

      - [ ] 3.1.1.1 Subtask — Specify terminal and cleanup outcomes.

        Record admission, cancel/timeout/death handling, cleanup work bounds,
        stop/invalidation/ref quiescence, wrap, quarantine release and exhaustion escalation.
        Accepted effects may remain indeterminate; timeout is not undo.

    - [ ] 3.1.2 Task [id: m2-p03-transport] [repo: unresolved-implementation] [after: m2-p03-decisions] — Implement bounded server-funded requests.

      Deliver finite payload/copy work and reserved completion/error storage without blocking
      the future actor scheduler contract.

      - [ ] 3.1.2.1 Subtask — Reserve transport state before admission.

        Fund request, reply and error paths, define notification coalescing and uncollected
        replies, and reject full pools atomically.

      - [ ] 3.1.2.2 Subtask — Resolve races without stale delivery.

        Correlate peer/request/generation and choose one terminal result under
        timeout/cancel/revocation/death races. Delay and duplicate replies to confirm
        replacements receive no old effects or authority.

    - [ ] 3.1.3 Task [id: m2-p03-reclaim] [repo: unresolved-implementation] [after: m2-p03-transport] — Implement stop, quiescence, and safe reuse.

      Retire resources only after the conditions needed for trustworthy new ownership hold.

      - [ ] 3.1.3.1 Subtask — Close and stop boundedly.

        Deny new admission, stop execution, retire timers/endpoints, and unwind failed
        construction in bounded steps. Interruption must not turn a partially closed object
        back into callable state.

      - [ ] 3.1.3.2 Subtask — Prove safe transfer.

        Check execution/reference and local x86 translation quiescence before zeroing and
        reassignment. Test small-width generation wrap and enforce bounded quarantine rather
        than reusing uncertain resources.

      - [ ] 3.1.3.3 Subtask — Reconcile the capacity ledger.

        Compare model traces and guest free/owned/reserved/quarantined totals over repeated
        close/reuse sequences. Inject failure at each cleanup stage and preserve
        counterexample traces.

  - [ ] 3.2 Section — Phase 3 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 3.2.1 Task [id: m2-p03-integration] [repo: unresolved-implementation] [after: m2-p03-reclaim] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 3.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Execute M2-T03/T06 and transport/reclamation portions of
        T01/T04 with the actual kernel and deterministic delayed peers. Require conservation
        and exactly one terminal disposition.

      - [ ] 3.2.1.2 Subtask — Exercise failures and inherited behavior.

        Race post-revocation admission, peer death, duplicated completions and interrupted
        cleanup; force wrap and quarantine exhaustion. Recheck Phase 2 authority/budgets and
        M1 entry/protection so passing reuse never hides corruption. Retain actual
        observations and finite watchdog outcomes, not only intended commands.

    - [ ] 3.2.2 Task [id: m2-p03-handoff] [repo: atom-os-research] [after: m2-p03-integration] — Record evidence and decide phase handoff.

      Provide a tested bounded transport/reuse substrate to Phase 4, with model-to-guest trace
      links and no unresolved stale-authority or conservation failures.

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
