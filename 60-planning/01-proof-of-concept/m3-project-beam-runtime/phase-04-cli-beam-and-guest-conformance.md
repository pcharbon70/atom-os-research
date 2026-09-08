---
title: "M3 Phase 4 — CLI BEAM and guest conformance"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m3
  - proof-of-concept
aliases: []
---

# M3 Phase 4 — CLI BEAM and guest conformance

Launch the compiled workload from the real CLI and qualify the complete BEAM/GC profile with
actor and whole-runtime recovery evidence.

Back to milestone: [M3 definition and plan](README.md).

## Entry, scope, and dependencies

M3 Phase 3 guest adapter/ledger with M2 recovery and M1 CLI regressions available.

Required predecessor: [M3 Phase 3](phase-03-guest-adapter-and-runtime-accounting.md), task `m3-p03-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M3-D04 is resolved by m3-p04-decisions: Freeze the static workload launch catalog,
inspection exposure, reproducible comparison suite and acceptance envelope against the
accepted profile and M2 authority. Until resolution, downstream code and passing acceptance
claims are blocked.

The kernel enforces domain protection and backing; the interpreter, actors and tracing
collector remain ring 3. A hosted oracle supplies comparison results, not guest kernel
services.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M3-A01, M3-A02, M3-A03, M3-A04, M3-A05, M3-A06, M3-A07; its case coverage is M3-T01, M3-T02, M3-T03, M3-T04, M3-T05, M3-T06, M3-T07. Partial/model/hosted results do not close a case requiring later guest integration.

- [beam profile loader and conformance](../../../20-notes/proof-of-concept-requirements/beam-profile-loader-and-conformance.md) — contract and failure-case input for this phase.
- [supervision and independent recovery](../../../20-notes/proof-of-concept-requirements/supervision-and-independent-recovery.md) — contract and failure-case input for this phase.
- [models fault injection and measurement](../../../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m3-p04-decisions | atom-os-research | Unassigned; resolve in m3-p04-decisions | m3-p03-handoff | M3-A01, M3-A07; phase cases below | Freeze launch and conformance acceptance output and verification; not run |
| m3-p04-launch | unresolved-implementation | Unassigned; resolve in m3-p04-decisions | m3-p04-decisions | M3-A07; phase cases below | Implement CLI launch and runtime inspection output and verification; not run |
| m3-p04-conformance | unresolved-implementation | Unassigned; resolve in m3-p04-decisions | m3-p04-launch | M3-A01, M3-A02, M3-A03, M3-A04, M3-A05, M3-A06, M3-A07; phase cases below | Assemble repeatable guest qualification output and verification; not run |
| m3-p04-integration | unresolved-implementation | Unassigned test reviewer | m3-p04-conformance | M3-T01, M3-T02, M3-T03, M3-T04, M3-T05, M3-T06, M3-T07 | Registered driver, raw positive/negative results; not run |
| m3-p04-handoff | atom-os-research | Unassigned acceptance reviewer | m3-p04-integration | M3-A01, M3-A02, M3-A03, M3-A04, M3-A05, M3-A06, M3-A07; M3-T01, M3-T02, M3-T03, M3-T04, M3-T05, M3-T06, M3-T07 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 4 Phase — CLI BEAM and guest conformance.

  Launch the compiled workload from the real CLI and qualify the complete BEAM/GC profile with
  actor and whole-runtime recovery evidence. Completion requires the assembled phase gate
  below, not just its component tasks.

  - [ ] 4.1 Section — CLI integration and recovery.

    Connect the managed workload to real user-facing controls without widening the authority
    boundary.

    - [ ] 4.1.1 Task [id: m3-p04-decisions] [repo: atom-os-research] [after: m3-p03-handoff] — Freeze launch and conformance acceptance.

      Resolve M3-D04 and bind the exact profile/corpus/ABI identities used for final guest
      tests.

      - [ ] 4.1.1.1 Subtask — Define the permitted launch catalog.

        Select statically bundled module entries and honest unsupported-module errors. Specify
        beam-profile and run behavior, quota limits and visible volatile/indeterminate
        outcomes without enabling arbitrary native execution.

    - [ ] 4.1.2 Task [id: m3-p04-launch] [repo: unresolved-implementation] [after: m3-p04-decisions] — Implement CLI launch and runtime inspection.

      Deliver M3-A07 through the existing bounded CLI and service interfaces.

      - [ ] 4.1.2.1 Subtask — Expose actual profile and workload state.

        Implement beam-profile and run for admitted modules; report real compatibility
        identity, accounts and runtime generation. Compare output with the machine-readable
        manifest and kernel ledgers.

      - [ ] 4.1.2.2 Subtask — Distinguish two recovery boundaries.

        Cause actor failure and selected supervision within a surviving runtime, then fail the
        whole runtime and use the independent control domain to replace it. Verify fresh
        identities, stale-authority rejection and honest volatile loss.

    - [ ] 4.1.3 Task [id: m3-p04-conformance] [repo: unresolved-implementation] [after: m3-p04-launch] — Assemble repeatable guest qualification.

      Tie compiler/oracle inputs to every test and executed guest binary.

      - [ ] 4.1.3.1 Subtask — Compare all admitted paths.

        Compile cleanly and run all selected success, exception, receive, timer and
        supervision paths in the oracle and guest. Retain mismatches; exclusions and permitted
        resource differences must be predeclared.

      - [ ] 4.1.3.2 Subtask — Combine semantics, GC and faults.

        Run the complete loader/GC/native-call/exhaustion/recovery campaign and inherited
        M1/M2 regressions. Measure same-runtime actor/GC delay separately from
        independent-domain progress.

  - [ ] 4.2 Section — Phase 4 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 4.2.1 Task [id: m3-p04-integration] [repo: unresolved-implementation] [after: m3-p04-conformance] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 4.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Execute all M3-T01–M3-T07 against the pinned guest workload
        and oracle. Require compiled-BEAM conformance, automatic long-lived-actor GC, complete
        imports and distinct actor/domain recovery.

      - [ ] 4.2.1.2 Subtask — Exercise failures and inherited behavior.

        Repeat malformed modules, tiny quotas, failed copying/GC space, stalled services and
        old replies during the CLI workload. Do not relax the profile or treat a native
        stand-in as BEAM; rerun all required M1/M2 guest cases. Retain actual observations and
        finite watchdog outcomes, not only intended commands.

    - [ ] 4.2.2 Task [id: m3-p04-handoff] [repo: atom-os-research] [after: m3-p04-integration] — Record evidence and decide phase handoff.

      Accept M3 only with all required guest results and artifacts, then hand the profile,
      workload, fault controls and raw measurements to M4. A smoke restart is not the M4
      stress campaign.

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
