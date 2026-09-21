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

Deliver an exercised unattended acceptance harness, assemble the clean virtual
input bundle for M1, and enforce that physical-fixture observations are not
consumed as kernel or emulator configuration.

Back to milestone: [M0 definition and plan](README.md).

## Entry, scope, and dependencies

M0 Phase 2 contract/build bundle. Physical-fixture observation has moved to M1
Phase 4 immediately before physical execution; it neither blocks this phase nor
enters the virtual M1 bundle.

Required predecessor: [M0 Phase 2](phase-02-boot-image-and-interface-contracts.md), task `m0-p02-handoff`.

Plan state: reviewed for execution. Implementation: Section 3.1 complete at
clean Kay OS revision `8206deb`; full phase integration and handoff remain not
run. The implementation repository is the selected public
[Kay OS repository](https://pushin.eu/pcharbon70/kay-os). Codex is the Section
3.1 implementation role, the user/project owner is the decision and acceptance
reviewer. A later non-identifying lab operator role belongs to M1 Phase 4.

Decision M0-D03 was resolved by `m0-p03-decisions` on 2026-09-20. Fixed
deadlines, exact controlled-fixture assertions, complete per-run retention,
process-group cleanup and the observation-only physical collection boundary are
recorded below. On 2026-09-21 the user clarified that the T7500 is one example
physical fixture, not the target platform. The `m0-p03-inventory` identity is
retained as the completed scope-transfer record; actual collection is owned by
`m1-p04-inventory` and closes no M0 acceptance case.

The host owns build tools, validation fixtures, emulation and capture; M0 does not claim
kernel enforcement. Firmware/loader/kernel ownership is fixed in the contract.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 64 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Accepted decision record

The user/project owner selected each M0-D03 choice from four alternatives on
2026-09-20:

| Area | Accepted selection | Evidence boundary |
| --- | --- | --- |
| Harness implementation | Python standard library on the host | Does not alter Zig as the kernel language or add a guest dependency. |
| Protocol | Versioned ASCII `KAY-HARNESS/1` records over a pseudo-serial PTY | The producer is a controlled host fixture, never Kay OS, Limine, QEMU serial output or a delivered CLI. |
| Deadlines | First output 5 seconds; response 2 seconds; stall 3 seconds; total run 30 seconds; cleanup grace 5 seconds | Fixed before execution; no post-failure widening is accepted. |
| Retention | Complete evidence directory for every successful and failed run | Raw directories stay outside Git unless selected and reviewed; summaries retain exact hashes. |
| Cleanup | New process group, `SIGTERM`, five-second grace, `SIGKILL`, reap, and fail on survivors | Direct-child-only or manual cleanup is rejected. |
| Physical collection | Deferred to M1 Phase 4; lab operator, normal account, versioned read-only collector, no `sudo` | The procedure is preserved, but no physical record is required or consumed by M0. |
| Publication | Private raw capture outside Git; allowlisted and manually approved public derivative with raw SHA-256 | Unique identifiers are excluded; unexpected lines or pending review fail publication. |
| Physical preflight | Observation only | Record available boot modes/media/connectors/device permissions; retain unsafe or unverified properties as unknown for M1 Phase 4. |

The machine-readable policy and human operator procedure live in the Kay OS
implementation paths `config/m0/phase-03-acceptance.json` and
`docs/m0/phase-03-decisions.md`. Changes to any selection reopen M0-D03 and
invalidate dependent run interpretation.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M0-A01, M0-A02, M0-A03, M0-A04, M0-A05, M0-A06, M0-A07; its case coverage is M0-T01, M0-T02, M0-T03, M0-T04, M0-T05, M0-T06. Partial/model/hosted results do not close a case requiring later guest integration.

- [models fault injection and measurement](../../../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md) — contract and failure-case input for this phase.
- [serial console and minimal cli](../../../20-notes/proof-of-concept-requirements/serial-console-and-minimal-cli.md) — contract and failure-case input for this phase.
- [x86-64 compatibility envelope and test fixtures](../../../20-notes/proof-of-concept-requirements/x86-64-compatibility-envelope-and-test-fixtures.md) — makes runtime discovery primary and separates the minimal QEMU baseline from independent physical fixtures.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m0-p03-decisions | atom-os-research | Codex implementer; user/project owner decision reviewer | m0-p02-handoff | M0-A06, M0-A07; phase cases below | Accepted M0-D03 record dated 2026-09-20 and 2026-09-21 scope clarification |
| m0-p03-harness | kay-os | Codex implementer; independent final reviewer pending | m0-p03-decisions | M0-A01, M0-A06; phase cases below | Driver and nine controlled cases passed at clean `8206deb`; [Section 3.1 evidence](../../../50-journal/2026-09-21-m0-phase-03-section-31-qualification.md) |
| m0-p03-inventory | atom-os-research | Codex implementer; user/project owner scope reviewer | m0-p03-decisions | M0-A07, M0-T06 | Superseded before collection: physical observation moved to `m1-p04-inventory`; M0 non-consumption boundary recorded |
| m0-p03-qualify | kay-os | Codex implementer; independent final reviewer pending | m0-p03-harness, m0-p03-inventory | M0-A01, M0-A02, M0-A03, M0-A04, M0-A05, M0-A06, M0-A07; phase cases below | Clean `8206deb` bundle assembled without physical inventory; [Section 3.1 evidence](../../../50-journal/2026-09-21-m0-phase-03-section-31-qualification.md) |
| m0-p03-integration | kay-os | Unassigned test reviewer | m0-p03-qualify | M0-T01, M0-T02, M0-T03, M0-T04, M0-T05, M0-T06 | Registered driver, raw positive/negative results; not run |
| m0-p03-handoff | atom-os-research | Unassigned acceptance reviewer | m0-p03-integration | M0-A01, M0-A02, M0-A03, M0-A04, M0-A05, M0-A06, M0-A07; M0-T01, M0-T02, M0-T03, M0-T04, M0-T05, M0-T06 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 3 Phase — Acceptance harness and input qualification.

  Deliver an exercised unattended acceptance harness, close the virtual M0
  input gate using real build and fixture evidence, and prove that physical
  observations are deferred. Completion requires the assembled phase gate
  below, not just its component tasks.

  - [x] 3.1 Section — Harness and qualification.

    Make positive and negative run interpretation repeatable, preserve the
    physical/virtual boundary, and prepare the final virtual input bundle.

    - [x] 3.1.1 Task [id: m0-p03-decisions] [repo: atom-os-research] [after: m0-p02-handoff] — Fix the acceptance envelope.

      Resolve M0-D03 and make every assertion, timeout and qualification
      boundary a recorded input rather than a post-failure adjustment.

      - [x] 3.1.1.1 Subtask — Define harness outcomes.

        Specify success, missing prompt, wrong response, early death, watchdog timeout,
        stalled output, cleanup completion, and nonzero failure statuses. Identify which
        streams are controlled fixtures rather than OS output.

      - [x] 3.1.1.2 Subtask — Define and transfer safe physical collection prerequisites.

        Preserve the physical operator, read-only commands, redaction rules,
        removable-media and serial/debug boundaries, but transfer their actual
        use to M1 Phase 4. Explicitly prohibit firmware changes and persistent
        device writes without separate authorization.

    - [x] 3.1.2 Task [id: m0-p03-harness] [repo: kay-os] [after: m0-p03-decisions] — Implement and exercise the launch-and-capture driver.

      Deliver M0-A06 and a runnable entry point with explicit version checks, finite cleanup,
      and per-run manifests.

      - [x] 3.1.2.1 Subtask — Build the driver.

        Connect pinned launch inputs, serial send/capture, assertions, watchdog, and process
        cleanup. Register the exact executable command and arguments in the run record; no
        unspecified runner may close this task.

      - [x] 3.1.2.2 Subtask — Inject harness failures.

        Use controlled response fixtures to prove the driver detects launch failure, timeout,
        missing/incorrect prompt, stalled stream, and unexpected process exit. Preserve both
        successful and failing logs.

    - [x] 3.1.3 Task [id: m0-p03-inventory] [repo: atom-os-research] [after: m0-p03-decisions] — Transfer physical inventory to M1 qualification.

      Retain the stable task ID while recording that no physical observation is
      an M0 input. The successor task collects a named fixture immediately
      before its M1 physical qualification.

      - [x] 3.1.3.1 Subtask — Remove the virtual dependency.

        Remove installed-unit data from M0 bundle requirements, acceptance
        dependencies and blocking state. Preserve explicit evidence that M0
        neither collected nor consumed such data.

      - [x] 3.1.3.2 Subtask — Assign the successor obligation.

        Assign external observation, Kay OS discovered-hardware reporting and
        comparison to M1 Phase 4. Retain safe collection/publication tooling as
        reusable preparation, not physical evidence.

    - [x] 3.1.4 Task [id: m0-p03-qualify] [repo: kay-os] [after: m0-p03-harness, m0-p03-inventory] — Assemble the virtual M1 input bundle.

      Bind all M0 virtual artifacts and their identities so another checkout
      can repeat the qualification without a laboratory-machine record.

      - [x] 3.1.4.1 Subtask — Reconcile the full input set.

        Verify virtual pins, build closure, contract validators and authority
        are complete and mutually consistent. Reject any attempt to include
        physical observations as emulator or kernel configuration.

      - [x] 3.1.4.2 Subtask — Reproduce the handoff.

        Package manifests, symbols, fixtures, launcher, commands, hashes and
        limits at named revisions. Repeat from a clean environment and leave
        any unavailable required virtual input blocked.

  - [ ] 3.2 Section — Phase 3 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 3.2.1 Task [id: m0-p03-integration] [repo: kay-os] [after: m0-p03-qualify] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing required virtual observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 3.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Execute all M0-T01–M0-T06 on the combined bundle, including
        two clean builds and the harness success fixtures. Confirm every
        artifact has actual output, no unresolved pin is accepted, and no
        physical inventory is consumed.

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
