---
title: "M0 Phase 3 — Acceptance harness and input qualification"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m0
  - proof-of-concept
aliases: []
---

# M0 Phase 3 — Acceptance harness and input qualification

Deliver an exercised unattended acceptance harness and close the complete M0 input gate using
real build and fixture evidence.

Back to milestone: [M0 definition and plan](README.md).

## Entry, scope, and dependencies

M0 Phase 2 contract/build bundle and Phase 1 inventory; missing obligations remain visible at
final review.

Required predecessor: [M0 Phase 2](phase-02-boot-image-and-interface-contracts.md), task `m0-p02-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M0-D03 is resolved by m0-p03-decisions: Freeze watchdog deadlines, serial assertions,
output retention, cleanup rules, and physical qualification prerequisites before interpreting
runs. Until resolution, downstream code and passing acceptance claims are blocked.

The host owns build tools, validation fixtures, emulation and capture; M0 does not claim
kernel enforcement. Firmware/loader/kernel ownership is fixed in the contract.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M0-A01, M0-A02, M0-A03, M0-A04, M0-A05, M0-A06, M0-A07; its case coverage is M0-T01, M0-T02, M0-T03, M0-T04, M0-T05, M0-T06. Partial/model/hosted results do not close a case requiring later guest integration.

- [models fault injection and measurement](../../../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md) — contract and failure-case input for this phase.
- [serial console and minimal cli](../../../20-notes/proof-of-concept-requirements/serial-console-and-minimal-cli.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m0-p03-decisions | atom-os-research | Unassigned; resolve in m0-p03-decisions | m0-p02-handoff | M0-A06; phase cases below | Fix the acceptance envelope output and verification; not run |
| m0-p03-harness | unresolved-implementation | Unassigned; resolve in m0-p03-decisions | m0-p03-decisions | M0-A01, M0-A06; phase cases below | Implement and exercise the launch-and-capture driver output and verification; not run |
| m0-p03-qualify | unresolved-implementation | Unassigned; resolve in m0-p03-decisions | m0-p03-harness | M0-A01, M0-A02, M0-A03, M0-A04, M0-A05, M0-A06, M0-A07; phase cases below | Assemble the M1 input bundle output and verification; not run |
| m0-p03-integration | unresolved-implementation | Unassigned test reviewer | m0-p03-qualify | M0-T01, M0-T02, M0-T03, M0-T04, M0-T05, M0-T06 | Registered driver, raw positive/negative results; not run |
| m0-p03-handoff | atom-os-research | Unassigned acceptance reviewer | m0-p03-integration | M0-A01, M0-A02, M0-A03, M0-A04, M0-A05, M0-A06, M0-A07; M0-T01, M0-T02, M0-T03, M0-T04, M0-T05, M0-T06 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 3 Phase — Acceptance harness and input qualification.

  Deliver an exercised unattended acceptance harness and close the complete M0 input gate
  using real build and fixture evidence. Completion requires the assembled phase gate below,
  not just its component tasks.

  - [ ] 3.1 Section — Harness and qualification.

    Make both positive and negative run interpretation repeatable before the real guest is
    available.

    - [ ] 3.1.1 Task [id: m0-p03-decisions] [repo: atom-os-research] [after: m0-p02-handoff] — Fix the acceptance envelope.

      Resolve M0-D03 and make every assertion and timeout a recorded input rather than a
      post-failure adjustment.

      - [ ] 3.1.1.1 Subtask — Define harness outcomes.

        Specify success, missing prompt, wrong response, early death, watchdog timeout,
        stalled output, cleanup completion, and nonzero failure statuses. Identify which
        streams are controlled fixtures rather than OS output.

    - [ ] 3.1.2 Task [id: m0-p03-harness] [repo: unresolved-implementation] [after: m0-p03-decisions] — Implement and exercise the launch-and-capture driver.

      Deliver M0-A06 and a runnable entry point with explicit version checks, finite cleanup,
      and per-run manifests.

      - [ ] 3.1.2.1 Subtask — Build the driver.

        Connect pinned launch inputs, serial send/capture, assertions, watchdog, and process
        cleanup. Register the exact executable command and arguments in the run record; no
        unspecified runner may close this task.

      - [ ] 3.1.2.2 Subtask — Inject harness failures.

        Use controlled response fixtures to prove the driver detects launch failure, timeout,
        missing/incorrect prompt, stalled stream, and unexpected process exit. Preserve both
        successful and failing logs.

    - [ ] 3.1.3 Task [id: m0-p03-qualify] [repo: unresolved-implementation] [after: m0-p03-harness] — Assemble the M1 input bundle.

      Bind all seven artifacts and their identities so another checkout can repeat the
      qualification.

      - [ ] 3.1.3.1 Subtask — Reconcile the full input set.

        Verify virtual pins, build closure, contract validators, authority, and installed
        inventory are complete and mutually consistent. Keep physical observations separate
        from emulator assumptions.

      - [ ] 3.1.3.2 Subtask — Reproduce the handoff.

        Package manifests, symbols, fixtures, launcher, commands, hashes, and limits at named
        revisions. Repeat from a clean environment and leave any unavailable required input
        blocked.

  - [ ] 3.2 Section — Phase 3 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 3.2.1 Task [id: m0-p03-integration] [repo: unresolved-implementation] [after: m0-p03-qualify] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 3.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Execute all M0-T01–M0-T06 on the combined bundle, including
        two clean builds and the harness success fixtures. Confirm every artifact has actual
        output and no unresolved pin is accepted.

      - [ ] 3.2.1.2 Subtask — Exercise failures and inherited behavior.

        Repeat invalid handoff/image/authority and harness-death cases with the final pins.
        Verify logs identify the exact failure and that a smoke image or simulated prompt
        cannot be labelled a delivered native CLI. Retain actual observations and finite
        watchdog outcomes, not only intended commands.

    - [ ] 3.2.2 Task [id: m0-p03-handoff] [repo: atom-os-research] [after: m0-p03-integration] — Record evidence and decide phase handoff.

      Close M0 only after required decisions and tests pass. Hand the immutable input bundle
      to M1; no compiled-BEAM profile or physical OS boot is claimed.

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
