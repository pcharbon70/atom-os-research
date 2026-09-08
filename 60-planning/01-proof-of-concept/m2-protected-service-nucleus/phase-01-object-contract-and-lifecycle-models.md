---
title: "M2 Phase 1 — Object contract and lifecycle models"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m2
  - proof-of-concept
aliases: []
---

# M2 Phase 1 — Object contract and lifecycle models

Make the minimal object, transport, and resource lifecycle executable before selecting kernel
data structures that depend on it.

Back to milestone: [M2 definition and plan](README.md).

## Entry, scope, and dependencies

M1 Phase 3 virtual acceptance for guest comparisons; hosted finite models may be developed
earlier if separately authorized, but do not close guest cases.

Required predecessor: [M1 Phase 3](../m1-boot-to-cli/phase-03-serial-cli-and-virtual-acceptance.md), task `m1-p03-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M2-D01 is resolved by m2-p01-decisions: Freeze minimal object/operation encodings,
rights, payers, capacities, generation/admission/terminal rules, and finite-model bounds using
the native demonstration and future nonblocking adapter as scope constraints. Until
resolution, downstream code and passing acceptance claims are blocked.

Kernel entry, protection, scheduling and bounded mechanisms are ring 0; CLI and ordinary
services are ring 3. Host tooling may build, emulate and capture but may not supply the
claimed guest kernel mechanisms.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M2-A01, M2-A02; its case coverage is M2-T01, M2-T03, M2-T06. Partial/model/hosted results do not close a case requiring later guest integration.

- [capabilities syscalls and bounded ipc](../../../20-notes/proof-of-concept-requirements/capabilities-syscalls-and-bounded-ipc.md) — contract and failure-case input for this phase.
- [domain lifecycle and safe reclamation](../../../20-notes/proof-of-concept-requirements/domain-lifecycle-and-safe-reclamation.md) — contract and failure-case input for this phase.
- [models fault injection and measurement](../../../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m2-p01-decisions | atom-os-research | Unassigned; resolve in m2-p01-decisions | m1-p03-handoff | M2-A01, M2-A02; phase cases below | Freeze the operation and model contract output and verification; not run |
| m2-p01-models | unresolved-implementation | Unassigned; resolve in m2-p01-decisions | m2-p01-decisions | M2-A01, M2-A02; phase cases below | Build finite models and fake backends output and verification; not run |
| m2-p01-integration | unresolved-implementation | Unassigned test reviewer | m2-p01-models | M2-T01, M2-T03, M2-T06 | Registered driver, raw positive/negative results; not run |
| m2-p01-handoff | atom-os-research | Unassigned acceptance reviewer | m2-p01-integration | M2-A01, M2-A02; M2-T01, M2-T03, M2-T06 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 1 Phase — Object contract and lifecycle models.

  Make the minimal object, transport, and resource lifecycle executable before selecting
  kernel data structures that depend on it. Completion requires the assembled phase gate
  below, not just its component tasks.

  - [ ] 1.1 Section — Contract and model closure.

    Translate the selected small object vocabulary into executable rules and bounded
    adversarial schedules.

    - [ ] 1.1.1 Task [id: m2-p01-decisions] [repo: atom-os-research] [after: m1-p03-handoff] — Freeze the operation and model contract.

      Resolve M2-D01 without importing the entire proposed kernel vocabulary.

      - [ ] 1.1.1.1 Subtask — Specify operations and capacities.

        For domains, slots, pages/CPU accounts, endpoints, notifications, timers and fault
        records, record rights, payer, admission, bounded work, terminal result and safe
        reuse. Cross-check the future runtime leaf-call needs.

      - [ ] 1.1.1.2 Subtask — Select finite model scope.

        Record model engine/version, state bounds, fairness, schedules and excluded behavior.
        Define conservation and single-terminal properties before running models.

    - [ ] 1.1.2 Task [id: m2-p01-models] [repo: unresolved-implementation] [after: m2-p01-decisions] — Build finite models and fake backends.

      Produce runnable construction/close/admission/completion/reclamation models and concrete
      regression traces.

      - [ ] 1.1.2.1 Subtask — Model lifecycle races.

        Explore cancellation, timeout, peer death, revocation, publication and close order.
        Retain counterexamples and show a deliberately broken transition is detected.

      - [ ] 1.1.2.2 Subtask — Cross-check fake mechanisms.

        Implement deterministic fake page/timer/endpoint backends and compare transitions with
        operation tables. Record free/owned/reserved/quarantined totals and one terminal
        transport disposition.

      - [ ] 1.1.2.3 Subtask — Export guest regression cases.

        Translate relevant counterexamples and transition fixtures into a case manifest for
        later real-kernel tests; mark model-only claims explicitly.

  - [ ] 1.2 Section — Phase 1 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 1.2.1 Task [id: m2-p01-integration] [repo: unresolved-implementation] [after: m2-p01-models] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 1.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Run contract/model checks for M2-T01 and model portions of
        T03/T06; reproduce explored bounds, invariants, and backend transition outcomes from
        clean inputs.

      - [ ] 1.2.1.2 Subtask — Exercise failures and inherited behavior.

        Exercise denied admission, double completion, interrupted construction, close races,
        and generation wrap in bounded fixtures. Deliberately violate conservation to verify
        the checker can fail. Recheck M1 ABI compatibility. Retain actual observations and
        finite watchdog outcomes, not only intended commands.

    - [ ] 1.2.2 Task [id: m2-p01-handoff] [repo: atom-os-research] [after: m2-p01-integration] — Record evidence and decide phase handoff.

      Release the versioned operation/model contract to Phase 2; M2-T01 remains pending guest
      cross-checks and model bounds are not universal proof.

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
