---
title: "M2 Phase 4 — Recovery nucleus and CLI control"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m2
  - proof-of-concept
aliases: []
---

# M2 Phase 4 — Recovery nucleus and CLI control

Run the independently funded ring-3 supervisor/registry and expose truthful CLI inspection and
authorized replacement of native children.

Back to milestone: [M2 definition and plan](README.md).

## Entry, scope, and dependencies

M2 Phase 3 accepted transport/reclamation and Phase 2 reserves/budgets.

Required predecessor: [M2 Phase 3](phase-03-bounded-transport-and-safe-reclamation.md), task `m2-p03-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M2-D04 is resolved by m2-p04-decisions: Freeze static launch/authority graph,
readiness publication, restart intensity/backoff, startup/shutdown deadlines, fault delivery
reserves and permitted operator targets before deliberate child faults. Until resolution,
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

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M2-A03, M2-A05, M2-A06, M2-A07; its case coverage is M2-T01, M2-T02, M2-T03, M2-T04, M2-T05, M2-T06, M2-T07, M2-T08. Partial/model/hosted results do not close a case requiring later guest integration.

- [supervision and independent recovery](../../../20-notes/proof-of-concept-requirements/supervision-and-independent-recovery.md) — contract and failure-case input for this phase.
- [serial console and minimal cli](../../../20-notes/proof-of-concept-requirements/serial-console-and-minimal-cli.md) — contract and failure-case input for this phase.
- [authentication and administration profile](../../../20-notes/proof-of-concept-requirements/authentication-and-administration-profile.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m2-p04-decisions | atom-os-research | Unassigned; resolve in m2-p04-decisions | m2-p03-handoff | M2-A06; phase cases below | Freeze bootstrap and recovery policy output and verification; not run |
| m2-p04-recovery | unresolved-implementation | Unassigned; resolve in m2-p04-decisions | m2-p04-decisions | M2-A03, M2-A05, M2-A06; phase cases below | Implement the ring-3 control service output and verification; not run |
| m2-p04-commands | unresolved-implementation | Unassigned; resolve in m2-p04-decisions | m2-p04-recovery | M2-A07; phase cases below | Implement bounded administrative CLI operations output and verification; not run |
| m2-p04-integration | unresolved-implementation | Unassigned test reviewer | m2-p04-commands | M2-T01, M2-T02, M2-T03, M2-T04, M2-T05, M2-T06, M2-T07, M2-T08 | Registered driver, raw positive/negative results; not run |
| m2-p04-handoff | atom-os-research | Unassigned acceptance reviewer | m2-p04-integration | M2-A03, M2-A05, M2-A06, M2-A07; M2-T01, M2-T02, M2-T03, M2-T04, M2-T05, M2-T06, M2-T07, M2-T08 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 4 Phase — Recovery nucleus and CLI control.

  Run the independently funded ring-3 supervisor/registry and expose truthful CLI inspection
  and authorized replacement of native children. Completion requires the assembled phase gate
  below, not just its component tasks.

  - [ ] 4.1 Section — Independent recovery.

    Turn protected mechanisms into a volatile service policy that survives the children it
    controls.

    - [ ] 4.1.1 Task [id: m2-p04-decisions] [repo: atom-os-research] [after: m2-p03-handoff] — Freeze bootstrap and recovery policy.

      Resolve M2-D04 without granting the CLI unrestricted root authority or promising
      recovery-root survival.

      - [ ] 4.1.1.1 Subtask — Check the static authority graph.

        Assign launch, fault, reserve, registry and restart rights. Prove each child's
        CPU/memory capacity is disjoint from the resources needed to diagnose and replace it.

      - [ ] 4.1.1.2 Subtask — Set publication and escalation rules.

        Define current-generation readiness, deadlines, backoff/intensity and reset escalation
        for kernel/root failure. Record visible volatile state loss and predeclare response
        limits.

    - [ ] 4.1.2 Task [id: m2-p04-recovery] [repo: unresolved-implementation] [after: m2-p04-decisions] — Implement the ring-3 control service.

      Launch and replace CLI/native test domains through the bounded kernel ABI.

      - [ ] 4.1.2.1 Subtask — Publish only ready current services.

        Bind registry entries to validated readiness and current generation; retire names on
        failure before replacements become visible.

      - [ ] 4.1.2.2 Subtask — Recover failed children.

        Crash, stall and loop native children and fault the CLI. Verify funded fault delivery,
        safe teardown, new generation, restart throttling and a surviving independent
        heartbeat.

  - [ ] 4.2 Section — Operator acceptance.

    Make inspection and restart report actual state and qualify the assembled service nucleus.

    - [ ] 4.2.1 Task [id: m2-p04-commands] [repo: unresolved-implementation] [after: m2-p04-recovery] — Implement bounded administrative CLI operations.

      Deliver mem, ps, services and permitted restart commands over versioned snapshots.

      - [ ] 4.2.1.1 Subtask — Expose real bounded snapshots.

        Report actual accounts, domains and service generations; compare with kernel/recovery
        traces and avoid claiming actor counts before M3.

      - [ ] 4.2.1.2 Subtask — Enforce restart permission.

        Permit only configured target names and reject unauthorized/unknown/stale requests.
        Rerun M1 parser limits and ensure inspection remains usable during child load.

  - [ ] 4.3 Section — Phase 4 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 4.3.1 Task [id: m2-p04-integration] [repo: unresolved-implementation] [after: m2-p04-commands] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 4.3.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Run every M2-T01–M2-T08 with real recovery and CLI control,
        including model/guest cross-checks, repeated native restart, CPU/serial pressure and
        each ledger-category exhaustion.

      - [ ] 4.3.1.2 Subtask — Exercise failures and inherited behavior.

        Combine full call/fault pools with child failure; send old readiness/handles and force
        cleanup interruption. Recovery reserves, ledgers and generations must remain sound.
        Rerun all M1 virtual acceptance cases. Retain actual observations and finite watchdog
        outcomes, not only intended commands.

    - [ ] 4.3.2 Task [id: m2-p04-handoff] [repo: atom-os-research] [after: m2-p04-integration] — Record evidence and decide phase handoff.

      Close M2 only with all required cases passing and deliver the versioned guest substrate
      to M3. Basic repeated recovery cannot be deferred to M4's larger campaign.

      - [ ] 4.3.2.1 Subtask — Record reproducible execution evidence.

        Create a dated journal record linked to the task/artifact/case IDs, full tested commit
        and dirty state, host/guest or physical configuration, tools, commands, raw logs,
        hashes, sample counts and pass/fail/blocked/not-run results. Keep failures and hosted
        versus guest evidence distinct. Index attachments and link the record from this phase
        and milestone.

      - [ ] 4.3.2.2 Subtask — Review closure and update the milestone.

        An assigned reviewer checks every child and required gate against evidence and records
        proceed, revise or blocked. Preserve unresolved decisions, limits and reopening
        conditions. Distinguish plan/tested/merge revisions; do not infer tests on a later
        merge. Update checkboxes only for verified work, keep blocked tests open, and update
        the next phase's entry state without authorizing implementation or Git actions.
