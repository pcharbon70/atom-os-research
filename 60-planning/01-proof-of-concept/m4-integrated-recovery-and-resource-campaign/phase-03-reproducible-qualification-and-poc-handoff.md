---
title: "M4 Phase 3 — Reproducible qualification and PoC handoff"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m4
  - proof-of-concept
aliases: []
---

# M4 Phase 3 — Reproducible qualification and PoC handoff

Independently reproduce the integrated results and issue an evidence-backed PoC acceptance or
revise/blocked decision with explicit limitations.

Back to milestone: [M4 definition and plan](README.md).

## Entry, scope, and dependencies

M4 Phases 1–2 completed campaign evidence and unchanged accepted M0–M3 interfaces; failed
required cases block closure.

Required predecessor: [M4 Phase 2](phase-02-resource-pressure-and-recovery-campaign.md), task `m4-p02-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M4-D03 is resolved by m4-p03-decisions: Select the final reviewed evidence baseline
and qualification environments; keep physical support and all deferred capability claims
separate from virtual PoC acceptance. Until resolution, downstream code and passing acceptance
claims are blocked.

Kernel protection and accounting remain ring 0; CLI, outer recovery, runtime and native test
service are separate ring-3 domains. Actor failure inside one runtime is distinct from domain
failure.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M4-A01, M4-A02, M4-A03, M4-A04, M4-A05, M4-A06; its case coverage is M4-T01, M4-T02, M4-T03, M4-T04, M4-T05, M4-T06, M4-T07. Partial/model/hosted results do not close a case requiring later guest integration.

- [models fault injection and measurement](../../../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md) — contract and failure-case input for this phase.
- [dell precision t7500 target and minimal qemu profile](../../../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m4-p03-decisions | atom-os-research | Unassigned; resolve in m4-p03-decisions | m4-p02-handoff | M4-A01, M4-A06; phase cases below | Review qualification scope and evidence ownership output and verification; not run |
| m4-p03-reproduce | unresolved-implementation | Unassigned; resolve in m4-p03-decisions | m4-p03-decisions | M4-A01, M4-A02, M4-A03, M4-A04, M4-A05; phase cases below | Repeat the full campaign from a clean build output and verification; not run |
| m4-p03-report | unresolved-implementation | Unassigned; resolve in m4-p03-decisions | m4-p03-reproduce | M4-A06; phase cases below | Write the acceptance and limitation report output and verification; not run |
| m4-p03-integration | unresolved-implementation | Unassigned test reviewer | m4-p03-report | M4-T01, M4-T02, M4-T03, M4-T04, M4-T05, M4-T06, M4-T07 | Registered driver, raw positive/negative results; not run |
| m4-p03-handoff | atom-os-research | Unassigned acceptance reviewer | m4-p03-integration | M4-A01, M4-A02, M4-A03, M4-A04, M4-A05, M4-A06; M4-T01, M4-T02, M4-T03, M4-T04, M4-T05, M4-T06, M4-T07 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 3 Phase — Reproducible qualification and PoC handoff.

  Independently reproduce the integrated results and issue an evidence-backed PoC acceptance
  or revise/blocked decision with explicit limitations. Completion requires the assembled
  phase gate below, not just its component tasks.

  - [ ] 3.1 Section — Independent reproduction and acceptance.

    Make another clean build reproduce the observations and expose every remaining claim
    boundary.

    - [ ] 3.1.1 Task [id: m4-p03-decisions] [repo: atom-os-research] [after: m4-p02-handoff] — Review qualification scope and evidence ownership.

      Resolve M4-D03 with an assigned reviewer and explicit virtual/physical closure state.

      - [ ] 3.1.1.1 Subtask — Reconcile required results.

        Map all milestone artifacts/cases to immutable evidence. Identify unrun, blocked,
        failed and superseded attempts; missing hardware evidence does not become optional
        without a recorded scope decision.

    - [ ] 3.1.2 Task [id: m4-p03-reproduce] [repo: unresolved-implementation] [after: m4-p03-decisions] — Repeat the full campaign from a clean build.

      Deliver final M4-A05 with independent build identities and repeatable semantic/fault
      outcomes.

      - [ ] 3.1.2.1 Subtask — Rebuild and rerun unattended.

        Build cleanly in a separate directory, compare hashes or declared nondeterminism, and
        rerun every M4 case plus inherited M1/M2 and admitted M3 conformance. Bind seeds,
        binary identities and commands to each result.

      - [ ] 3.1.2.2 Subtask — Review numeric observations.

        Report distributions/sample counts, CLI/heartbeat/timer/GC/fault/recovery intervals
        and maximum observed values against predeclared targets. Keep host descheduling and
        guest clocks separate; QEMU timing is not physical WCET.

    - [ ] 3.1.3 Task [id: m4-p03-report] [repo: unresolved-implementation] [after: m4-p03-reproduce] — Write the acceptance and limitation report.

      Deliver M4-A06 without turning deferred capabilities into implicit successes.

      - [ ] 3.1.3.1 Subtask — Issue the bounded PoC conclusion.

        Compare results with every exit condition, state the supported workload envelope and
        retain anomalies and failure history. Publish a proceed/revise/blocked recommendation
        in the governing inquiry with exact evidence links.

      - [ ] 3.1.3.2 Subtask — Preserve physical and later-work obligations.

        Record the M1 physical qualification state and leave unperformed required hardware
        work open. Keep durability, networking, DMA, SMP/NUMA, wider authentication,
        update/root survival and UI outside this result; proposed next work needs separate
        authorization.

  - [ ] 3.2 Section — Phase 3 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 3.2.1 Task [id: m4-p03-integration] [repo: unresolved-implementation] [after: m4-p03-report] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 3.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Execute M4-T07 and reproduce M4-T01–T06 with the final clean
        build. Require matching semantic/fault results, explained identities and all numerical
        observations within the accepted envelope.

      - [ ] 3.2.1.2 Subtask — Exercise failures and inherited behavior.

        Review omitted samples, changed pins, unexplained resource drift and missing required
        results as closure failures. Re-run inherited negative cases and ensure the report
        cannot count hosted tests or a boot prompt as full guest PoC evidence. Retain actual
        observations and finite watchdog outcomes, not only intended commands.

    - [ ] 3.2.2 Task [id: m4-p03-handoff] [repo: atom-os-research] [after: m4-p03-integration] — Record evidence and decide phase handoff.

      Update the milestone and governing inquiry only from reviewed passing evidence. Keep
      required blocked or failed gates open and identify remaining capabilities; no follow-on
      implementation, publication or device write is authorized by this plan.

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
