---
title: "M4 Phase 1 — Campaign baseline and fault workload"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m4
  - proof-of-concept
aliases: []
---

# M4 Phase 1 — Campaign baseline and fault workload

Assemble the CLI, recovery controller, BEAM runtime and native test domain into one
reproducible campaign with frozen limits and fault controls.

Back to milestone: [M4 definition and plan](README.md).

## Entry, scope, and dependencies

Accepted M1 virtual, M2 and M3 guest evidence plus the M0 fixture; missing mechanisms return
to their owning milestone.

Required predecessor: [M3 Phase 4](../m3-project-beam-runtime/phase-04-cli-beam-and-guest-conformance.md), task `m3-p04-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M4-D01 is resolved by m4-p01-decisions: Freeze exact inherited versions, workload
seeds/counts/durations, capacities and measurement clocks/targets. Adopt or revise proposed
actor/allocation/restart counts before testing, not after failure. Until resolution,
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

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M4-A01, M4-A02, M4-A05; its case coverage is M4-T01, M4-T02. Partial/model/hosted results do not close a case requiring later guest integration.

- [models fault injection and measurement](../../../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md) — contract and failure-case input for this phase.
- [supervision and independent recovery](../../../20-notes/proof-of-concept-requirements/supervision-and-independent-recovery.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m4-p01-decisions | atom-os-research | Unassigned; resolve in m4-p01-decisions | m3-p04-handoff | M4-A01; phase cases below | Freeze the campaign manifest output and verification; not run |
| m4-p01-workload | unresolved-implementation | Unassigned; resolve in m4-p01-decisions | m4-p01-decisions | M4-A02, M4-A05; phase cases below | Implement integrated workload and bounded fault controls output and verification; not run |
| m4-p01-integration | unresolved-implementation | Unassigned test reviewer | m4-p01-workload | M4-T01, M4-T02 | Registered driver, raw positive/negative results; not run |
| m4-p01-handoff | atom-os-research | Unassigned acceptance reviewer | m4-p01-integration | M4-A01, M4-A02, M4-A05; M4-T01, M4-T02 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 1 Phase — Campaign baseline and fault workload.

  Assemble the CLI, recovery controller, BEAM runtime and native test domain into one
  reproducible campaign with frozen limits and fault controls. Completion requires the
  assembled phase gate below, not just its component tasks.

  - [ ] 1.1 Section — Campaign contract and instrumentation.

    Make the environment, workload and pass/fail interpretation reproducible before collecting
    stress results.

    - [ ] 1.1.1 Task [id: m4-p01-decisions] [repo: atom-os-research] [after: m3-p04-handoff] — Freeze the campaign manifest.

      Resolve M4-D01 against accepted predecessor evidence and the actual 128 MiB single-CPU
      envelope.

      - [ ] 1.1.1.1 Subtask — Pin the inherited system.

        Bind source/dirty state, image, compiler/oracle, QEMU, versioned machine, firmware,
        ABI, profile, launch graph and authority identities. Reject missing predecessor
        results or silent fixture enlargement.

      - [ ] 1.1.1.2 Subtask — Predeclare scales and measurements.

        Select seeds, repetitions, durations, sweep points, budgets, reserves and limits.
        Explicitly adopt or revise the proposed 128 actors, million transient allocations and
        1,000 restarts. Define intervals, clocks, p99/maximum-observed targets and handling of
        warmup, timeout and missing samples.

      - [ ] 1.1.1.3 Subtask — Specify campaign controls.

        Record allowed fault triggers, readiness/restart deadlines, accepted-effect ambiguity
        and rollback/reset of each run. A fault harness must not substitute simulated
        substrate behavior.

    - [ ] 1.1.2 Task [id: m4-p01-workload] [repo: unresolved-implementation] [after: m4-p01-decisions] — Implement integrated workload and bounded fault controls.

      Deliver M4-A02 and initial raw evidence capture over the four-domain system.

      - [ ] 1.1.2.1 Subtask — Compose the real CLI-operated workload.

        Launch compiled job/counter work, inspect actual accounts and identities, and
        correlate events across CLI, outer control, runtime and native service.

      - [ ] 1.1.2.2 Subtask — Exercise distinct failures.

        Trigger CLI crash, native crash/stall, actor failure and whole-runtime death. Observe
        independent outer progress, appropriate new identities and volatile loss; root failure
        follows declared reset escalation.

      - [ ] 1.1.2.3 Subtask — Verify observation integrity.

        Preserve serial/event/timing streams and finite host watchdog outcomes. Detect lost
        samples, missing fault acknowledgements and truncated logs so incomplete evidence
        cannot pass.

  - [ ] 1.2 Section — Phase 1 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 1.2.1 Task [id: m4-p01-integration] [repo: unresolved-implementation] [after: m4-p01-workload] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 1.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Execute M4-T01 and baseline T02 with real domains and
        compiler-produced workload. Verify normal interaction and each distinct fault outcome
        under the frozen manifest; capture raw M4-A05 evidence.

      - [ ] 1.2.1.2 Subtask — Exercise failures and inherited behavior.

        Remove required evidence, mismatch a binary/profile identity, omit a fault result, and
        run invalid-profile/authority cases. The campaign must fail closed. Re-run admitted M3
        corpus and M1/M2 CLI/protection gates. Retain actual observations and finite watchdog
        outcomes, not only intended commands.

    - [ ] 1.2.2 Task [id: m4-p01-handoff] [repo: atom-os-research] [after: m4-p01-integration] — Record evidence and decide phase handoff.

      Give Phase 2 a reproducible campaign with trustworthy observations. No load, latency or
      repeated-restart capacity claim is accepted from this baseline alone.

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
