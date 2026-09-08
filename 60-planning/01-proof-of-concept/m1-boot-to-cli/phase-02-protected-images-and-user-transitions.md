---
title: "M1 Phase 2 — Protected images and user transitions"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - implementation-planning
  - m1
  - proof-of-concept
aliases: []
---

# M1 Phase 2 — Protected images and user transitions

Install validated native images and demonstrate safe ring-3 execution, traps, and return with
kernel-owned context and protected memory.

Back to milestone: [M1 definition and plan](README.md).

## Entry, scope, and dependencies

M1 Phase 1 accepted kernel/memory baseline.

Required predecessor: [M1 Phase 1](phase-01-kernel-entry-and-memory-foundation.md), task `m1-p01-handoff`.

Plan state: draft, requiring decision review before execution. Implementation: not started.
All tests: not run. Implementation repository and individual owners remain unassigned; M0-D01
resolves the source location and initial roles, and this phase's decisions task assigns its
execution/review roles before dependent work. The label unresolved-implementation is a
recorded blocker, not a selected repository.

Decision M1-D02 is resolved by m1-p02-decisions: Freeze image permissions, state preservation,
syscall buffer rules, and return validation against M0; restricted FP/SIMD remains explicit
rather than full ABI support. Until resolution, downstream code and passing acceptance claims
are blocked.

Kernel entry, protection, scheduling and bounded mechanisms are ring 0; CLI and ordinary
services are ring 3. Host tooling may build, emulate and capture but may not supply the
claimed guest kernel mechanisms.

Unless explicitly identified as the physical qualification phase, guest checks use the
M0-pinned QEMU/SeaBIOS, versioned q35, Nehalem-v1, TCG, one CPU, 128 MiB and serial fixture.
Do not add writable storage, networking, SMP/NUMA or graphical UI to satisfy a failing case.
AtomVM remains excluded. No command, commit, PR, installation or device write is authorized by
this plan.

## Research and acceptance traceability

The governing [milestone definition](README.md) retains the full artifact and acceptance wording. This phase contributes to M1-A02, M1-A03, M1-A06; its case coverage is M1-T01, M1-T05, M1-T06, M1-T07. Partial/model/hosted results do not close a case requiring later guest integration.

- [privilege entry memory and user return](../../../20-notes/proof-of-concept-requirements/privilege-entry-memory-and-user-return.md) — contract and failure-case input for this phase.
- [freestanding build and static images](../../../20-notes/proof-of-concept-requirements/freestanding-build-and-static-images.md) — contract and failure-case input for this phase.

Follow the [planning convention](../../README.md). Retain results in [dated journal evidence](../../../50-journal/README.md), using the optional [execution-record template](../../../templates/phase-execution-record.md), with indexed [assets](../../../assets/README.md) or exact artifacts in the selected implementation repository.

## Task identity, ownership, and dependencies

IDs below are symbolic, not Markdown anchors. The predecessor document above resolves cross-phase dependencies. Each task's output must be linked to the listed artifact/case obligations and exact run evidence; no row records a pass.

| Task ID | Repository/location | Responsible role | Requires | Artifact / acceptance contribution | Completion evidence |
| --- | --- | --- | --- | --- | --- |
| m1-p02-decisions | atom-os-research | Unassigned; resolve in m1-p02-decisions | m1-p01-handoff | M1-A02, M1-A03; phase cases below | Resolve user-context enforcement details output and verification; not run |
| m1-p02-images | unresolved-implementation | Unassigned; resolve in m1-p02-decisions | m1-p02-decisions | M1-A02; phase cases below | Implement atomic static-image admission output and verification; not run |
| m1-p02-transitions | unresolved-implementation | Unassigned; resolve in m1-p02-decisions | m1-p02-images | M1-A03, M1-A06; phase cases below | Implement entry, copying, and safe return output and verification; not run |
| m1-p02-integration | unresolved-implementation | Unassigned test reviewer | m1-p02-transitions | M1-T01, M1-T05, M1-T06, M1-T07 | Registered driver, raw positive/negative results; not run |
| m1-p02-handoff | atom-os-research | Unassigned acceptance reviewer | m1-p02-integration | M1-A02, M1-A03, M1-A06; M1-T01, M1-T05, M1-T06, M1-T07 | Dated evidence and proceed/revise/blocked review; not run |

## Planned work

- [ ] 2 Phase — Protected images and user transitions.

  Install validated native images and demonstrate safe ring-3 execution, traps, and return
  with kernel-owned context and protected memory. Completion requires the assembled phase gate
  below, not just its component tasks.

  - [ ] 2.1 Section — User protection boundary.

    Join loader validation, mappings, and control transfer into one testable boundary.

    - [ ] 2.1.1 Task [id: m1-p02-decisions] [repo: atom-os-research] [after: m1-p01-handoff] — Resolve user-context enforcement details.

      Resolve M1-D02 before installing executable user mappings.

      - [ ] 2.1.1.1 Subtask — Define invalid-context handling.

        Document address-space identity, PC/stack range, privilege/interrupt flags, enabled
        registers, and exception-stack ownership. Associate each invalid condition with a
        rejection or fault test.

    - [ ] 2.1.2 Task [id: m1-p02-images] [repo: unresolved-implementation] [after: m1-p02-decisions] — Implement atomic static-image admission.

      Load the chosen image subset without exposing partially validated executable state.

      - [ ] 2.1.2.1 Subtask — Validate and reserve the complete image.

        Check lengths, segment destinations, entry, permissions, unsupported relocations, and
        overlap before publication. Roll back reservations on injected allocation or parsing
        failure.

      - [ ] 2.1.2.2 Subtask — Install protected mappings.

        Set kernel/user access, text/data/stack permissions, guards, zero-fill, and
        page-accounting ownership. Verify text writes, data execution, kernel access, and
        stack overflow follow the declared fault policy.

    - [ ] 2.1.3 Task [id: m1-p02-transitions] [repo: unresolved-implementation] [after: m1-p02-images] — Implement entry, copying, and safe return.

      Deliver the selected syscall/exception path without trusting user-supplied context.

      - [ ] 2.1.3.1 Subtask — Preserve and validate context.

        Enter on kernel-owned stacks, preserve every enabled state component, and validate
        return state and address-space association. Use register-pattern fixtures to detect
        corruption or leakage.

      - [ ] 2.1.3.2 Subtask — Check complete user buffers.

        Validate direction, length, arithmetic, and all pages before copies or privileged
        effects. Exercise invalid opcodes, zero/maximum lengths, cross-page holes, and
        privileged instructions in replaceable test images.

  - [ ] 2.2 Section — Phase 2 Integration Tests.

    Test the assembled outputs and inherited behavior using the exact entry fixture, declared
    case envelope and finite failure policy. These tests control handoff; required failures,
    missing inputs and unrun cases remain open.

    - [ ] 2.2.1 Task [id: m1-p02-integration] [repo: unresolved-implementation] [after: m1-p02-transitions] — Verify the integrated outcome and regressions.

      Create or extend the executable phase driver, bind its invocation to a versioned case
      manifest, and run positive and negative cases. The driver must return failure for
      missing observations or watchdog expiry; an unspecified future command cannot close this
      task.

      - [ ] 2.2.1.1 Subtask — Register and run the acceptance path.

        Record exact setup, command, binary/fixture hashes, case IDs, seeds and numerical
        limits before execution. Run native test images at CPL 3 and handlers at CPL 0;
        capture traces, mapping permissions, stack alignment, data/BSS, and register
        preservation. Execute M1-T05/T06 and transition portions of T01/T07; the final CLI
        round trip is Phase 3.

      - [ ] 2.2.1.2 Subtask — Exercise failures and inherited behavior.

        Inject malformed images, unsafe return state, guessed kernel pointers, cross-page
        buffers, and privileged user operations. Protected canaries must remain unchanged;
        rerun Phase 1 boot and bounded-failure behavior. Retain actual observations and finite
        watchdog outcomes, not only intended commands.

    - [ ] 2.2.2 Task [id: m1-p02-handoff] [repo: atom-os-research] [after: m1-p02-integration] — Record evidence and decide phase handoff.

      Release protected native execution and the narrow syscall skeleton to Phase 3. A test
      program is not yet the interactive CLI delivery.

      - [ ] 2.2.2.1 Subtask — Record reproducible execution evidence.

        Create a dated journal record linked to the task/artifact/case IDs, full tested commit
        and dirty state, host/guest or physical configuration, tools, commands, raw logs,
        hashes, sample counts and pass/fail/blocked/not-run results. Keep failures and hosted
        versus guest evidence distinct. Index attachments and link the record from this phase
        and milestone.

      - [ ] 2.2.2.2 Subtask — Review closure and update the milestone.

        An assigned reviewer checks every child and required gate against evidence and records
        proceed, revise or blocked. Preserve unresolved decisions, limits and reopening
        conditions. Distinguish plan/tested/merge revisions; do not infer tests on a later
        merge. Update checkboxes only for verified work, keep blocked tests open, and update
        the next phase's entry state without authorizing implementation or Git actions.
